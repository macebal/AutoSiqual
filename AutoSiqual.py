# import datetime
from datetime import datetime, date, time, timedelta
import logging
import pyautogui,ctypes
import pyperclip
from PasteData import paste_data, qt_sleep, click_image
from config import ConfigParser
from excel_parser.ParserFactory import ParserFactory

def numlock_is_active():
    """
    Returns a boolean indicating whether the num lock key is pressed (true) or not (false)
    """
    #returns True if the NumLock key is activated
    dll = ctypes.WinDLL ("User32.dll")
    VK_NUMLOCK = 0x90
    return bool(dll.GetKeyState(VK_NUMLOCK))

def start_robot(material):
    """
    Starts the robot from the Siqual's homescreen
    \n
    Params:
    \tmaterial: the name of the material to input its data into Siqual
    """
    config = ConfigParser()
    logger = logging.getLogger('ui_logger')

    #These variables are defined in the config file and are used to configure how much time should the robot wait between input
    #commands and how much time should it wait for the dialogs to open (in seconds) to account for the delay in the connection
    DELAY_BETWEEN_COMMANDS, DELAY_BETWEEN_SCREENS = config.get_delay_times()
    material_data = config.get_material_data(material)
    plant_code, _ = config.get_active_plant_names()
    is_raw_mat = material_data["isRawMaterial"]

    logger.info('Programa Iniciado - Tiene 10 segundos para hacer foco (maximizar la pantalla de SIQUAL)')
    
    for i in range(10,0,-1):
        logger.info(f'{i}...')
        qt_sleep(1)

    pyautogui.click #To ensure focus

    #if numlock key is active, the following block disables it because otherwise the program won't input
    #the commands correctly (it's a known bug atm)
    if numlock_is_active():
        logger.info('Tecla Bloq Num desactivada')
        pyautogui.press('numlock')

    logger.info('Abriendo pantalla de Creación/Modificación de RIC')
    qt_sleep(DELAY_BETWEEN_COMMANDS)
    
    pyautogui.hotkey('alt', 'e')
    pyautogui.typewrite(['c', 'c', 'm'], interval=DELAY_BETWEEN_COMMANDS)
    qt_sleep(DELAY_BETWEEN_SCREENS)

    logger.info('Abriendo ventana de selección de RIC')
    qt_sleep(DELAY_BETWEEN_COMMANDS)
    
    click_image(image_name = 'puntosSuspensivos.png', index = 1)
    qt_sleep(DELAY_BETWEEN_SCREENS)

    logger.info(f'Buscando ultimo RIC de {material}')
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    pyautogui.typewrite(['tab', 'tab'], interval=DELAY_BETWEEN_COMMANDS)
    pyautogui.hotkey('shiftleft','end') #select the date
    pyautogui.press('del') # delete it
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    # Define the start date as 60 days before today
    start_date = datetime.now() - timedelta(days=60)
    pyautogui.typewrite(start_date.strftime('%Y-%m-%d'))  
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=DELAY_BETWEEN_COMMANDS)  # Press the search button
    qt_sleep(DELAY_BETWEEN_SCREENS)

    # find the button with the arrow facing down with the Product header and click it.
    click_image(image_name = 'flecha.png', index = 2)
    qt_sleep(DELAY_BETWEEN_SCREENS)

    # find the item of the material (the image is called like that aswell)
    click_image(image_name = f"{material_data['siqualName']}.png")
    qt_sleep(DELAY_BETWEEN_SCREENS)

    # Press 5 times the pagedwn key to go to the end of the table
    pyautogui.typewrite(['pagedown', 'pagedown', 'pagedown', 'pagedown', 'pagedown', 'pagedown'], interval=DELAY_BETWEEN_COMMANDS)

    # Click in the yellow square to select the last RIC
    click_image(image_name ='casilleroSeleccionado.png')
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'enter'], interval=DELAY_BETWEEN_COMMANDS)  # Press the ok button
    
    click_image(image_name ='cargarDatos.png',confidence=0.95)
    logger.info(f'Cargado el ultimo RIC de {material}')
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    #Position the cursor over the date
    pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab'], interval=DELAY_BETWEEN_COMMANDS)

    #select and copy the date
    pyautogui.hotkey('shiftleft','end')
    qt_sleep(DELAY_BETWEEN_COMMANDS)

    pyautogui.hotkey('ctrl','c') #copy the date
    qt_sleep(DELAY_BETWEEN_COMMANDS)
    
    date = datetime.strptime(pyperclip.paste(), '%Y-%m-%d')

    logger.info("Cargado datos desde el archivo Excel")
    qt_sleep(0)

    if is_raw_mat:
        #Since raw materials are loaded once every month, on the first days, one of two situations may arise:
        # 1.- The last data point found is the last day of the month before last month (i.e. if we're in february, the last data point should be 31/12 before we enter the new data)
        # 2.- The last data point found belongs to the last month (for example if we're in february and the last data point is 10/01). This means that the robot failed previously to input all data and must resume

        now = datetime.now()

        first_day_of_this_month = datetime.combine(datetime.today().replace(day=1), time())
        last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)


        time_from_last_data = now - date
        expected_time_from_last_data = now - first_day_of_last_month - timedelta(days=1) #I would expect that the last data point found was the last day of 2 months ago
        
        if time_from_last_data.days < expected_time_from_last_data.days:
            #if the robot stopped midway from the month, continue inputting data from there
            pass
        else:
            #if not, start inputting on the first day of last month (by passing the previous day to the algorithm, hence the -1 days part)
            date = first_day_of_last_month - timedelta(days=1)

    factory = ParserFactory()
    parser = factory.getParser(plant_code)
    data = parser.parse_materials(date, material)

    paste_data(data, material)

