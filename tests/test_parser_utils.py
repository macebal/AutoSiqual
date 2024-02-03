import pytest
from datetime import datetime
from src.exceptions import DateNotFoundError, ParameterNotFoundError
from src.parsers.utils import find_date_row, find_nearest_date, find_parameter_column


@pytest.mark.parametrize(
    "target_date, expected_row",
    [
        (datetime(2023, 1, 4), 8),
        (datetime(2023, 1, 30), 34),
        (datetime(2023, 11, 16), 47),
        pytest.param(
            datetime(2023, 2, 3),
            None,
            marks=pytest.mark.xfail(raises=DateNotFoundError),
        ),
    ],
)
def test_find_date_row(load_dates_sheet, target_date, expected_row):
    ws, dates_column, _ = load_dates_sheet
    row = find_date_row(target_date, ws, dates_column)
    assert row == expected_row


@pytest.mark.parametrize(
    "target_date, expected_row, search_previous",
    [
        (datetime(2023, 1, 4), 8, False),  # exact match
        (datetime(2023, 1, 4), 8, True),  # exact match
        (datetime(2023, 2, 4), 40, False),
        (datetime(2023, 2, 4), 34, True),
        (datetime(2023, 11, 15), 46, True),
        (datetime(2023, 11, 15), 47, False),
    ],
)
def test_find_nearest_date_row(load_dates_sheet, target_date, expected_row, search_previous):
    ws, dates_column, _ = load_dates_sheet
    row = find_nearest_date(target_date, ws, dates_column, search_previous)
    assert row == expected_row


@pytest.mark.parametrize(
    "parameter_name, expected_column",
    [
        ("Dates", 3),
        ("Parameter 6", 9),
        ("Foo", 14),
        ("Baz", 16),
        pytest.param(
            "non existing parameter",
            None,
            marks=pytest.mark.xfail(raises=ParameterNotFoundError),
        ),
    ],
)
def test_find_parameter_column(load_dates_sheet, parameter_name, expected_column):
    ws, _, header_row = load_dates_sheet
    col = find_parameter_column(parameter_name, ws, header_row)
    assert col == expected_column
