import pytest
from datetime import datetime
from src.exceptions import DateNotFoundError
from src.parsers.utils import find_date_row


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
    ws, *_ = load_dates_sheet
    row = find_date_row(target_date, ws, 3)
    assert row == expected_row
