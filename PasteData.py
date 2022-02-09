import datetime
import logging, pyautogui
from config import ConfigParser
from PyQt5 import QtCore

def qt_sleep(seconds):
    """
    Create a sleep period that doesn't freeze the UI.
    \n
    Params:
    \tseconds: the amount of seconds to sleep.
    """
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(seconds*1000, loop.quit)
    loop.exec_()

def click_image(image_name, index = 0, confidence=1):
    """
    Clicks the region onscreen that is equal to the provided one.
    \n
    Params:
    \timage_name: The name and extension of an image located in the img folder
    \tindex: If there is more than one result for that image, the index in the resulting list
    """
    logger = logging.getLogger('ui_logger')

    path = 'img\\' + image_name

    if confidence < 1:
        results = list(pyautogui.locateAllOnScreen(path, confidence=confidence)) 
    else:
        results = list(pyautogui.locateAllOnScreen(path))

    if len(results) == 0:
            logger.critical(f'No se encuentra el boton {image_name}. ¿La ventana está cerrada?')
            logger.critical('El programa terminó abruptamente.')
            qt_sleep(5)
            exit(1)

    coords = pyautogui.center(results[index])  # find the coordinates
    pyautogui.click(coords[0], coords[1]) # click the image

def paste_data(data, material):
    config = ConfigParser()
    logger = logging.getLogger('ui_logger')

    #These variables are defined in the config file and are used to configure how much time should the robot wait between input
    #commands and how much time should it wait for the dialogs to open (in seconds) to account for the delay in the connection
    DELAY_BETWEEN_COMMANDS, DELAY_BETWEEN_SCREENS = config.get_delay_times()

    for date_data in data:
        current_date = datetime.datetime.strftime(date_data['DATE'], '%Y-%m-%d')
        
        logger.info(f"Pegando datos de {current_date}")

        click_image('copiarRIC.png')

        pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab'], interval=DELAY_BETWEEN_COMMANDS)
        pyautogui.hotkey('shiftleft','end')
        pyautogui.typewrite(['del'])

        pyautogui.typewrite(current_date)
        pyautogui.typewrite(['tab'])

        click_image(image_name = 'grabar.png', confidence= 0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        #close the "success" sign
        pyautogui.typewrite(['enter'])
        qt_sleep(DELAY_BETWEEN_SCREENS)
        
        # click the RIE image
        click_image(image_name = 'RIE.png', confidence = 0.9)
        qt_sleep(1.5 * DELAY_BETWEEN_SCREENS) #For the system's delay

        # click the Ensayos/Resultados button
        click_image('ensayosResultados.png')
        qt_sleep(3 * DELAY_BETWEEN_SCREENS) # 3 times the delay because of the slowness of the system

        pyautogui.click()
        click_image('cuadroseleccionado_test.png', index = 1, confidence= 0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        for i in range(7):
            pyautogui.typewrite(['down']) #TODO: make this available in config.json

        qt_sleep(DELAY_BETWEEN_SCREENS)

        pyautogui.typewrite(['enter'])
        qt_sleep(DELAY_BETWEEN_SCREENS)

        pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab', 'tab'], interval=DELAY_BETWEEN_COMMANDS)
        pyautogui.typewrite(['pageup', 'pageup', 'pageup', 'pageup', 'pageup'], interval=DELAY_BETWEEN_COMMANDS)

        #This loops needs the dictionary to be in order of appearence
        for key, value in date_data.items():
            if key == "DATE":
                continue #skip the date
            else:
                if value == None:
                    pyautogui.typewrite(['down']) #If there is no value for that parameter, skip it
                else:
                    pyautogui.typewrite(str(value).replace('.',','))
                    pyautogui.typewrite(['down'])

        qt_sleep(DELAY_BETWEEN_SCREENS)

        # click the Save button
        click_image(image_name = 'grabarDatos.png', confidence= 0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        #Accept all the following pop up messages
        for i in range(6):
            pyautogui.typewrite(['enter'])
            qt_sleep(DELAY_BETWEEN_SCREENS)

        qt_sleep(6)
        # click the close button
        click_image(image_name= 'cerrar1.png', confidence = 0.8)
        qt_sleep(DELAY_BETWEEN_SCREENS)
       
        # clickea en el boton de Cerrar
        click_image(image_name = 'cerrar2.png', confidence = 0.9)

    logger.info("Se ha finalizado la carga con éxito")
    qt_sleep(DELAY_BETWEEN_SCREENS)
       
    # close the RIC window to return to the start
    click_image(image_name = 'cerrar.png', confidence = 0.8)
