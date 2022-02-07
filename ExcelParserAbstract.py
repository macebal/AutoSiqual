from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class ExcelParserAbstract(ABC):
    
    def _find_date(self, date, worksheet, column) -> int:
        """
        Params:
        \tdate: The date to search for
        \tworksheet: The worksheet to search into
        \tcolumn: the column that has the dates in worksheet
        \n
         Returns:
        \tThe row number of the given date. Returns -1 if it doesn't exist.
        """
        for row in worksheet.iter_rows(min_col=column, max_col=column):
            for cell in row:
                if isinstance(cell.value, datetime):
                    if cell.value == date:
                        return cell.row
        else:
            return -1

    def _find_nearest_date(self,date, search_previous, worksheet, column) -> int:
        """
        Recursively find the nearest date in the worksheet.

        Params:
        \tdate: The date to search for
        \tsearch_previous: true if the algorithm should look for previous dates to find the nearest, otherwise it will look for posterior dates
        \tworksheet: The worksheet to search into
        \tcolumn: the column that has the dates in worksheet
        \n
        Returns:
        \tThe row number of the nearest date as an integer
        """

        date_current = date
        result = self._find_date(date, worksheet, column)
        
        if result == -1:
            if search_previous:
                date_current -= timedelta(days=1)
            else:
                date_current += timedelta(days=1)

            return self._find_nearest_date(date_current, search_previous, worksheet, column)
        else:
            return result

    def _find_parameter_column(self, parameter, worksheet, header_row) -> int:
        """
        Find the column for a given parameter cell name
        \n
        Params:
        \tparameter: The name of the parameter
        \tworksheet: The worksheet to search into
        \theader_row: The row to iterate over
        \n
        Returns
        \tThe column where that parameter is located in the header_row as an integer.
        """

        for row in worksheet.iter_rows(min_row=header_row, max_row=header_row):
            for cell in row:
                if cell.value == parameter:
                    return cell.column - 1 # it's -1 because cell.column is 1-based index.
        else:
            return -1

    @abstractmethod
    def parse_products(self, start_date, material) -> list:
        """
        Parses the corresponding excel file looking for the material data provided in the config.json file. It parses onwards from start_date
        \n
        Returns a list of dicts where each item is one day and each key:value pair is the siqual code and the cell value respectively.
        """
        pass

