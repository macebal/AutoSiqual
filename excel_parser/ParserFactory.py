from excel_parser.CAT import ExcelParserCAT

class ParserFactory():
    def getParser(self, plant_code):
        if plant_code == "CAT":
            return ExcelParserCAT()