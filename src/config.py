import json

class ConfigParser(object):

    CONFIG_DATA = ""

    DEFAULT_TIME_BETWEEN_SCREENS = 2.5
    DEFAULT_TIME_BETWEEN_COMMANDS = 0.5

    def __init__(self):

        try:
            with open('config.json', 'r', encoding='utf-8') as file:
                self.CONFIG_DATA = json.load(file)
        except:
            raise Exception("No existe el archivo config.json.")

    def get_active_plant_names(self):
        """ 
        Get the active plant's code and full name
        \n
        Returns:
        \tcode: the Siqual code (str)
        \tfull_name: the complete plant's name (str)
        """
        full_name = ""
        
        code = self.CONFIG_DATA['activePlantCode']

        for plant in self.CONFIG_DATA["plants"]:
            if plant["code"] == code:
                full_name = plant["name"]

        if len(full_name) > 0 and len(code) > 0:
            return code , full_name
        else:
            raise Exception("La planta seleccionada en el archivo config.json no existe o esta mal codificada.")

    def get_materials(self):
        """ 
        Get the active plant's list of products and raw materials
        \n
        Returns:
        \tproducts: a list containing all the product names defined or an empty list if there are none
        \traw_materials: a list containing all the raw_material names defined or an empty list if there are none
        """
        full_name = ""
        products = []
        raw_materials = []

        for plant in self.CONFIG_DATA["plants"]:
            if plant["code"] == self.CONFIG_DATA['activePlantCode']:
                for material in plant["materials"]["data"]:
                    if material["isRawMaterial"]:
                        raw_materials.append(material["name"])        
                    else:
                        products.append(material["name"])                      

        if len(products) > 0 and len(raw_materials) > 0:
            return products, raw_materials
        else:
            raise Exception("No se han definido materiales en el archivo config.json para esta planta.")
    
    def get_delay_times(self):
        """
        Get the delay times provided in config.json
        \n
        Returns:
        \tbetween_commands: The delay between commands (float)
        \tbetween_screens: the delay between screens (float)
        """

        between_commands = self.CONFIG_DATA['delayBetweenCommands']
        between_screens = self.CONFIG_DATA['delayBetweenScreens']

        if between_commands == 0:
            between_commands = self.DEFAULT_TIME_BETWEEN_COMMANDS

        if between_screens == 0:
            between_screens = self.DEFAULT_TIME_BETWEEN_COMMANDS

        return between_commands, between_screens

    def get_material_data(self, material):
        """
        Given a material, get its data for the current plant
        \n
        Params
        \tmaterial (str): the name of the material
        \n
        Returns
        \tdictionary with the following keys:
        \t\tname (str): the full name\n
        \t\tsiqualName (str): the Siqual name\n
        \t\tworksheetName (str): the name of the worksheet containing the data to input for that material\n
        \t\tisRawMaterial (bool): if the material is a product or a raw material\n
        \t\tgenericPositionInList (int): the position of the generic form from the list in the "Creacion de Ensayo" window\n
        \t\tcolumnsToInput (dict): an object with key:value pairs of equivalencies between siqual codes and column names of the workbook
        """
        for plant in self.CONFIG_DATA["plants"]:
            if plant["code"] == self.CONFIG_DATA['activePlantCode']:
                for index, product in enumerate(plant["materials"]["data"]):
                    if product["name"] == material:
                        return plant["materials"]["data"][index]

    def get_wb_data(self, material) -> str:
        """
        Given a material, get its workbook data
        \n
        Params
        \tmaterial (str): the name of the material
        \n
        Returns
        \t\t data (dict): A dictionary with a key "pathAbs" for the path and a key "headerRow" for the row of the headers
        """
        is_raw_material = self.get_material_data(material)['isRawMaterial']
        
        for plant in self.CONFIG_DATA["plants"]:
            if plant["code"] == self.CONFIG_DATA['activePlantCode']:
                if is_raw_material:
                    return plant["materials"]["workbooks"]["rawMaterials"]
                else:
                    return plant["materials"]["workbooks"]["products"]
