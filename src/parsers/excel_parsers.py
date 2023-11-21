from datetime import datetime, timedelta, time
from typing import Callable
import logging
import openpyxl

from src.config import ConfigParser
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
    start_row = (
        find_nearest_date(
            start_date,
            search_previous=True,
            column=column_numbers["DATE"],
            worksheet=ws,
        )
        + 1
    )
    end_row = find_nearest_date(
        end_date, search_previous=True, column=column_numbers["DATE"], worksheet=ws
    )

    wb.close()


if __name__ == "__main__":
    excel_parser_cat(None, "Clinker")
