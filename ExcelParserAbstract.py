from abc import ABC, abstractmethod
import datetime

class ExcelParserInterface(ABC):
    
    def find_date(self, date, worksheet, column) -> int:
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

    def find_nearest_date(self,date, search_previous, worksheet, column) -> int:
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
        result = self.find_date(date, worksheet, column)

        if result == -1:
            if search_previous:
                date_current -= datetime.timedelta(days=1)
            else:
                date_current += datetime.timedelta(days=1)

            return self.find_nearest_date(date_current, search_previous, worksheet, column)
        else:
            return result

    def find_parameter_column(parameter, worksheet, header_row) -> int:
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
                    return cell.column - 1 #TODO it's -1 porque la columna 4 se convierte en 3 cuando la utilizas en el array de filas
        else:
            return -1

    @abstractmethod
    def parse_products(start_date, material) -> list:
        """
        TODO:
        Parses the corresponding excel file looking for the 
        """
        pass

