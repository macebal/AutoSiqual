from datetime import datetime, timedelta, time
import openpyxl
from src.excel_parser.ExcelParserAbstract import ExcelParserAbstract
from src.config import ConfigParser

class ExcelParserCAT(ExcelParserAbstract):
    
    STOP_DAYS_FROM_NOW = 10 #stop parsing when the date is X days from now (To account from missing data in the workbook)

    def __init__(self):
        pass        

    def parse_materials(self, start_date, material) -> list:
        conf = ConfigParser()
        material_data = conf.get_material_data(material)
        columns_dict =  material_data["columnsToInput"]

        wb_data = conf.get_wb_data(material)
        wb_path = wb_data["pathAbs"]
        HEADER_ROW = wb_data["headerRow"]

        sheet_name = material_data["worksheetName"]
        isRawMaterial = material_data["isRawMaterial"]

        try:
            wb = openpyxl.load_workbook(wb_path, read_only=True, data_only = True)
            ws = wb[sheet_name]
        except:
            raise Exception(f"No se encuentra el archivo {wb_path} o no existe una hoja con el nombre {sheet_name} allí.")

        column_numbers = {}
        constant_parameters = {} #If there is a constant instead of a column name, add it to this dictionary to treat it accordingly 

        for k,v in material_data["columnsToInput"].items():
            if v != "":
                if type(v) == str:
                    column = super()._find_parameter_column(parameter=v,worksheet=ws,header_row=HEADER_ROW)
                    
                    if column != -1: #if the parameter is found
                        column_numbers[k] = column
                else:
                    constant_parameters[k] = v #if there is a number, add it as a constant to input that instead of the would be cell value later on

        date_column_index = super()._find_parameter_column(parameter=material_data["columnsToInput"]["DATE"],worksheet=ws, header_row=HEADER_ROW) + 1

        if isRawMaterial:
            first_day_of_this_month = datetime.combine(datetime.today().replace(day=1), time())
            last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
            end_date = last_day_of_last_month
        else:
            end_date =  datetime(datetime.now().year, datetime.now().month, datetime.now().day) - timedelta(days=self.STOP_DAYS_FROM_NOW)

        start_row = super()._find_nearest_date(start_date, search_previous= True, column= date_column_index, worksheet= ws) + 1 #The row following the last available data in siqual
        end_row = super()._find_nearest_date(end_date, search_previous= True, column= date_column_index, worksheet= ws) 

        if end_row > start_row:
            parsed_data = []

            #only iterate over the needed range to accelerate the algorithm
            for row in ws.iter_rows(min_row = start_row, max_row = end_row):
                
                row_data = {}

                #iterate over all the available keys in the `columns_dict`. If that key also exists in `column_numbers` it means that there is a value for that parameter
                #if it doesn't, add a None to that position. There should be a value for each key provided in the config file
                
                is_valid_row = False #this variable remains False until it finds a value besides the date
                for key in columns_dict.keys():
                    if key in column_numbers.keys():
                        cell_value = row[column_numbers.get(key)].value

                        if (key == "IP" or key == "FP") and cell_value != None: #for the setting times, transform from hh:mm format to mm
                            row_data[key] = cell_value.hour * 60 + cell_value.minute

                        elif key == "BARI" and cell_value != None:
                            row_data[key] = cell_value / 1000

                        elif (key == "SBA" or key == "CC3S") and cell_value != None:
                            decimals = 0 if key == "SBA" else 2
                            row_data[key] = round(cell_value, decimals)
                            
                        else:
                            if str(cell_value).strip() != '*': #The * is sometimes used in the workbook to signal purposely missing data.
                                row_data[key] = row[column_numbers.get(key)].value
                            else:
                                row_data[key] = None

                    elif key in constant_parameters.keys():
                        row_data[key] = constant_parameters[key]
                    else:
                        row_data[key] = None

                    if key != "DATE" and row_data[key] != None: 
                        is_valid_row = True #This is True with at least 1 value besides the date

                if is_valid_row:        
                    parsed_data.append(row_data)  

        else:
            raise Exception(f"No hay valores de {material} para cargar")

        wb.close()
        return parsed_data    
