import logging
import openpyxl
from datetime import datetime, timedelta
from typing import Callable
from src.exceptions import ParameterNotFoundError
from src.models.user_config import UserConfig
from src.parsers.utils import find_nearest_date, find_parameter_column

STOP_DAYS_FROM_NOW = 10  # stop parsing when the date is X days from now (To account from missing data in the workbook)

LOGGER = logging.getLogger("ui_logger")


def get_excel_parser(plant_code: str) -> Callable[[datetime, str], list[dict]]:
    parser = None
    match plant_code:
        case "CAT":
            parser = excel_parser_cat

    if parser is None:
        raise ValueError(f"Codigo de planta invalido {plant_code}")

    return parser


def excel_parser_cat(start_date: datetime, material: str):
    config = UserConfig.from_json()
    material_data = config.active_plant.materials.get_material_data_from_name(material)
    is_raw_material = material_data.is_raw_material

    wb_file = (
        config.active_plant.materials.workbooks.raw_materials
        if is_raw_material
        else config.active_plant.materials.workbooks.products
    )
    sheet_name = material_data.worksheet_name

    try:
        wb = openpyxl.load_workbook(wb_file.path_abs, read_only=True, data_only=True)
        ws = wb[sheet_name]
    except Exception as e:
        raise IOError(
            f"No se encuentra el archivo {wb_file.path_abs} o no existe una hoja con el nombre {sheet_name} allí."
        )

    columns_to_input = material_data.columns_to_input.model_dump()

    column_numbers = {}
    # If there is a constant instead of a column name, add it to the following dictionary to treat it accordingly
    constant_parameters = {}

    for k, v in columns_to_input.items():
        if v != "":
            if type(v) == str:
                try:
                    column_index = find_parameter_column(
                        parameter=v, worksheet=ws, header_row=wb_file.header_row
                    )
                    column_numbers[k] = column_index
                except ParameterNotFoundError:
                    LOGGER.critical(
                        f"No se puede encontrar el parametro {v} en la fila {wb_file.header_row} de la hoja {ws.title}."
                    )
            else:
                # if there is a number, add it as a constant to input that instead of the would be cell value later on
                constant_parameters[k] = v

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if is_raw_material:
        # end date is the last day of last month
        end_date = today.replace(day=1) - timedelta(days=1)
    else:
        end_date = today - timedelta(days=STOP_DAYS_FROM_NOW)

    # The starting row is the one following the last available data in siqual
    start_row = find_nearest_date(start_date, ws, column=column_numbers["DATE"]) + 1
    end_row = find_nearest_date(
        end_date, ws, column=column_numbers["DATE"], search_previous=True
    )

    if start_row > end_row:
        raise Exception(f"No hay valores de {material} para cargar")

    parsed_data = []

    # only iterate over the needed range to accelerate the algorithm
    for row in ws.iter_rows(min_row=start_row, max_row=end_row):
        row_data = {}

        # iterate over all the available keys in the `columns_dict`. If that key also exists in `column_numbers` it means that there is a value for that parameter
        # if it doesn't, add a None to that position. There should be a value for each key provided in the config file

        # The following flag remains False until it finds a value besides the date
        is_valid_row = False

        for key in columns_to_input:
            if key in column_numbers:
                cell_value = row[column_numbers[key] - 1].value

                if cell_value is not None:
                    if key in ["IP", "FP"]:
                        # for the setting times, transform from hh:mm format to mm
                        row_data[key] = cell_value.hour * 60 + cell_value.minute

                    elif key == "BARI":
                        row_data[key] = cell_value / 1000

                    elif key in ["SBA", "CC3S", "CO2"]:
                        decimals = 0 if key == "SBA" else 2
                        row_data[key] = round(cell_value, decimals)
                    else:
                        # The * is sometimes used in the workbook to signal purposely missing data.
                        if str(cell_value).strip() != "*":
                            row_data[key] = cell_value
                        else:
                            row_data[key] = None

                if key != "DATE" and row_data.get(key) is not None:
                    # This is True with at least 1 value besides the date in row_data
                    is_valid_row = True

        if is_valid_row:
            parsed_data.append(row_data)

    wb.close()
    return parsed_data
