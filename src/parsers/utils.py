from datetime import datetime, timedelta
from typing import Any

from src.exceptions import DateNotFoundError, ParameterNotFoundError


def find_date_row(date: datetime, worksheet: Any, column: int) -> int:
    """Attempts to find the row in which a `date` is located in an openpyxl `worksheet`.

    Parameters
    ----------
    date : datetime
        The target date.
    worksheet : Any
        The worksheet to search.
    column : int
        The column that holds the date inside the worksheet.

    Returns
    -------
    int
        The row where the date is located.

    Raises
    ------
    DateNotFoundError
        If the provided date is not found.

    """

    for row in worksheet.iter_rows(min_col=column, max_col=column):
        for cell in row:
            if isinstance(cell.value, datetime) and cell.value == date:
                return cell.row
    else:
        raise DateNotFoundError(
            f"La fecha {date.strftime('%d/%m/%Y')} no se encuentra en la columna {column} de la hoja {worksheet.title}"
        )


def find_nearest_date(
    date: datetime, worksheet: Any, column: int, search_previous: bool = False
) -> int:
    """Recursively find the nearest date in the worksheet.

    Parameters
    ----------
    date : datetime
        The target date.
    worksheet : Any
        The worksheet to search.
    column : int
        The column that holds the date inside the worksheet.
    search_previous : bool, optional
        True if the algorithm should look for previous dates to find the nearest,
        otherwise it will look for posterior dates, by default False.

    Returns
    -------
    int
        The row number of the nearest date.

    """

    date_current = date

    try:
        result = find_date_row(date, worksheet, column)
    except DateNotFoundError:
        if search_previous:
            date_current -= timedelta(days=1)
        else:
            date_current += timedelta(days=1)

        return find_nearest_date(date_current, worksheet, column, search_previous)

    return result


def find_parameter_column(parameter: str, worksheet: Any, header_row: int) -> int:
    """Finds the column for a given parameter cell name

    Parameters
    ----------
    parameter : str
        The name of the parameter
    worksheet : Any
        The worksheet to search into
    header_row : int
        The row to iterate over

    Returns
    -------
    int
        The column where that parameter is located. 1-based index.

    Raises
    ------
    ParameterNotFoundError
        If the parameter is not found in the worksheet
    """

    for row in worksheet.iter_rows(min_row=header_row, max_row=header_row):
        for cell in row:
            if cell.value == parameter:
                return cell.column  # cell.column is 1-based index.
    else:
        raise ParameterNotFoundError(
            f"El parametro {parameter} no se encuentra en la fila {header_row} de la hoja {worksheet.title}"
        )
