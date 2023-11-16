import openpyxl
import pytest

DATES_WORKBOOK_PATH = "tests/data/dates.xlsx"


@pytest.fixture(scope="function")
def load_dates_sheet():
    wb = openpyxl.load_workbook(DATES_WORKBOOK_PATH, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    dates_column = 3  # 1-based index
    headers_row = 4
    yield ws, dates_column, headers_row
    wb.close()
