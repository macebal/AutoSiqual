import pytest
from datetime import datetime
from models.user_config import UserConfig
from parsers.excel_parsers import excel_parser_cat


@pytest.mark.parametrize(
    "material_name, start_date, end_date, expected_items",
    [
        ("Clinker", datetime(2023, 6, 7), datetime(2023, 7, 26), 24),
        pytest.param(
            "Clinker",
            datetime(2023, 7, 26),
            datetime(2023, 6, 7),
            99999,
            marks=pytest.mark.xfail(reason="No hay valores de Clinker para cargar"),
            id="Fecha de inicio mayor a fecha de fin",
        ),
        ("Harina", datetime(2023, 9, 18), datetime(2023, 10, 31), 40),
        ("CPC40", datetime(2023, 1, 2), datetime(2023, 2, 22), 44),
        ("CPC30", datetime(2023, 7, 12), datetime(2023, 7, 31), 16),
        ("Plasticor", datetime(2023, 3, 8), datetime(2023, 6, 9), 75),
        ("CPN40", datetime(2023, 7, 12), datetime(2023, 7, 24), 10),
    ],
)
def test_parser_cat(material_name, start_date, end_date, expected_items):
    config = UserConfig.from_json(filename="tests/data/cat/sample_config.json")
    material_data = config.active_plant.materials.get_material_data_from_name(material_name)
    expected_keys = list(material_data.columns_to_input.model_dump().keys())

    parsed_data = excel_parser_cat(start_date, end_date, material_name, config)

    assert isinstance(parsed_data, list)
    assert all([isinstance(item, dict) for item in parsed_data])
    assert all([sorted(list(item.keys())) == sorted(expected_keys) for item in parsed_data])
    assert len(parsed_data) == expected_items
