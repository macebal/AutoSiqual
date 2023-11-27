import logging
import pyautogui
import ctypes
from datetime import datetime, time, timedelta
from src.paste_data import paste_data, qt_sleep, click_image
from src.config import ConfigParser
from parsers.excel_parsers import get_excel_parser

STOP_DAYS_FROM_NOW = 10  # stop parsing when the date is X days from now (To account from missing data in the workbook)


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

    click_image(image_name="puntosSuspensivos.png", index=1, confidence=0.95)
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
    click_image(image_name = f"{material_data['siqualName']}.png", confidence=0.95)
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
    # pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab'], interval=DELAY_BETWEEN_COMMANDS)

    # #select and copy the date
    # pyautogui.hotkey('shiftleft','end')
    # qt_sleep(DELAY_BETWEEN_COMMANDS)

    # pyautogui.hotkey('ctrl','c') #copy the date
    # qt_sleep(DELAY_BETWEEN_COMMANDS)
    
    # clipboard_text = pyclip.paste(text=True)
    # if clipboard_text:
    #     date = datetime.strptime(clipboard_text, '%Y-%m-%d')
    # else:
    #     logger.info("No se pudo copiar la fecha, no hay datos en el portapapeles.")
    #     qt_sleep(5)
    #     exit(1)
    try:
        str_date = pyautogui.prompt(
            text="Introduzca la fecha inicial de toma de muestra de este RIC. El formato debe ser igual al que aparece en pantalla: YYYY-MM-DD",
            title="Introduzca la fecha",
            default="",
        )
        date = datetime.strptime(str_date, "%Y-%m-%d")
        logger.info(f"Ha seleccionado la fecha {date}")
        if numlock_is_active():
            logger.info("Tecla Bloq Num desactivada")
            pyautogui.press("numlock")
    except Exception as e:
        logger.info(
            f"No se buscar la fecha. {str_date} no es una fecha valida o tiene el formato incorrecto"
        )
        qt_sleep(5)
        exit(1)

    logger.info("Cargando datos desde el archivo Excel")

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if is_raw_mat:
        # end date is the last day of last month
        end_date = today.replace(day=1) - timedelta(days=1)
    else:
        end_date = today - timedelta(days=STOP_DAYS_FROM_NOW)

    parser = get_excel_parser(plant_code)
    data = parser.parse_materials(date, end_date, material)

    paste_data(data, material)
