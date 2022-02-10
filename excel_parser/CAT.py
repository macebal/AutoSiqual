from datetime import datetime, timedelta
import openpyxl
from excel_parser.ExcelParserAbstract import ExcelParserAbstract
from config import ConfigParser

class ExcelParserCAT(ExcelParserAbstract):
    
    HEADER_ROW = 4
    STOP_DAYS_FROM_NOW = 10 #stop parsing when the date is X days from now (To account from missing data in the workbook)
    DATES_COLUM_INDEX = 2 #the index of the dates column in the worksheet

    def __init__(self):
        pass        

    def parse_products(self, start_date, material) -> list:
        conf = ConfigParser()
        material_data = conf.get_material_data(material)
        columns_dict =  material_data["columnsToInput"]

        wb_path = conf.get_wb_path(material)
        sheet_name = material_data["worksheetName"]

        try:
            wb = openpyxl.load_workbook(wb_path, read_only=True)
            ws = wb[sheet_name]
        except:
            raise Exception(f"No se encuentra el archivo {wb_path} o no existe una hoja con el nombre {sheet_name} allí.")

        column_numbers = {}

        for k,v in material_data["columnsToInput"].items():
            if v != "":
                column = super()._find_parameter_column(parameter=v,worksheet=ws,header_row=self.HEADER_ROW)
                
                if column != -1: #if the parameter is found
                    column_numbers[k] = column

        end_date =  datetime(datetime.now().year, 
                            datetime.now().month, 
                            datetime.now().day) \
                    - timedelta(days=self.STOP_DAYS_FROM_NOW)

        start_row = super()._find_nearest_date(start_date, search_previous= True, column= self.DATES_COLUM_INDEX, worksheet= ws) + 1 #The row following the last available data in siqual
        end_row = super()._find_nearest_date(end_date, search_previous= True, column= self.DATES_COLUM_INDEX, worksheet= ws) 

        if end_row > start_row:
            parsed_data = []

            #only iterate over the needed range to accelerate the algorithm
            index = 0
            for row in ws.iter_rows(min_row = start_row, max_row = end_row):
                
                row_data = {}

                #iterate over all the available keys in the `columns_dict`. If that key also exists in `column_numbers` it means that there is a value for that parameter
                #if it doesn't, add a None to that position. There should be a value for each key provided in the config file
                
                for key in columns_dict.keys():
                    if key in column_numbers.keys():
                        cell_value = row[column_numbers.get(key)].value

                        if (key == "IP" or key == "FP") and cell_value != None: #for the setting times, transform from hh:mm format to mm
                            row_data[key] = cell_value.hour * 60 + cell_value.minute

                        elif key == "BARI":
                            row_data[key] = cell_value / 1000

                        elif key == "SBA":
                            row_data[key] = round(cell_value)
                            
                        else:
                            if str(cell_value).strip() != '*': #The * is sometimes used in the workbook to signal purposely missing data.
                                row_data[key] = row[column_numbers.get(key)].value
                            else:
                                row_data[key] = None
                    else:
                        row_data[key] = None


                parsed_data.append(row_data)  

        else:
            raise Exception(f"No hay valores de {material} para cargar")

        wb.close()
        return parsed_data    