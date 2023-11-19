from datetime import datetime
from typing import Callable

from src.config import ConfigParser

STOP_DAYS_FROM_NOW = 10  # stop parsing when the date is X days from now (To account from missing data in the workbook)


def get_excel_parser(plant_code: str) -> Callable[[datetime, str], list[dict]]:
    parser = None
    match plant_code:
        case "CAT":
            parser = excel_parser_cat

    if parser is None:
        raise ValueError(f"Codigo de planta invalido {plant_code}")

    return parser


def excel_parser_cat(start_date: datetime, material: str):
    conf = ConfigParser()
    material_data = conf.get_material_data(material)
    columns_dict = material_data["columnsToInput"]
