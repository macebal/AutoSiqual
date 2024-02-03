import datetime
import logging
import pyautogui
from src import CONFIG
from utils import click_image, qt_sleep


def paste_data(data, material_name):
    config = CONFIG
    logger = logging.getLogger("ui_logger")

    DELAY_BETWEEN_COMMANDS = config.delay_between_commands
    DELAY_BETWEEN_SCREENS = config.delay_between_screens

    material_data = config.active_plant.materials.get_material_data_from_name(material_name)
    position_in_generic_list = material_data.generic_position_in_list

    for date_data in data:
        current_date = datetime.datetime.strftime(date_data["DATE"], "%Y-%m-%d")

        logger.info(f"Pegando datos de {current_date}")

        click_image("copiarRIC.png", confidence=0.95)

        pyautogui.typewrite(["tab", "tab", "tab", "tab", "tab"], interval=DELAY_BETWEEN_COMMANDS)
        pyautogui.hotkey("shiftleft", "end")
        pyautogui.typewrite(["del"])

        pyautogui.typewrite(current_date)
        pyautogui.typewrite(["tab"])

        click_image(image_name="grabar.png", confidence=0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        # close the "success" sign
        pyautogui.typewrite(["enter"])
        qt_sleep(DELAY_BETWEEN_SCREENS)

        # click the RIE image
        click_image(image_name="RIE.png", confidence=0.9)
        qt_sleep(1.5 * DELAY_BETWEEN_SCREENS)  # For the system's delay

        # click the Ensayos/Resultados button
        click_image("ensayosResultados.png", confidence=0.9)
        qt_sleep(3 * DELAY_BETWEEN_SCREENS)  # 3 times the delay because of the slowness of the system

        pyautogui.click()
        click_image("cuadroseleccionado.png", index=1, confidence=0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        for _ in range(position_in_generic_list):
            pyautogui.typewrite(["down"])

        qt_sleep(DELAY_BETWEEN_SCREENS)

        pyautogui.typewrite(["enter"])
        qt_sleep(DELAY_BETWEEN_SCREENS)

        pyautogui.typewrite(["tab"] * 6, interval=DELAY_BETWEEN_COMMANDS)
        pyautogui.typewrite(["pageup"] * 5, interval=DELAY_BETWEEN_COMMANDS)

        # This loops needs the dictionary to be in order of appearence
        for key, value in date_data.items():
            if key == "DATE":
                continue  # skip the date
            else:
                if value is None:
                    pyautogui.typewrite(["down"])  # If there is no value for that parameter, skip it
                else:
                    pyautogui.typewrite(str(value).replace(".", ","))
                    pyautogui.typewrite(["down"])

        qt_sleep(DELAY_BETWEEN_SCREENS)

        # click the Save button
        click_image(image_name="grabarDatos.png", confidence=0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        # Accept all the following pop up messages
        for _ in range(6):
            pyautogui.typewrite(["enter"])
            qt_sleep(DELAY_BETWEEN_SCREENS)

        qt_sleep(6)
        # click the close button
        click_image(image_name="cerrar.png", confidence=0.9)
        qt_sleep(DELAY_BETWEEN_SCREENS)

        # clickea en el boton de Cerrar
        click_image(image_name="cerrar.png", confidence=0.9, index=1)

    logger.info("Se ha finalizado la carga con éxito")
    qt_sleep(DELAY_BETWEEN_SCREENS)

    # close the RIC window to return to the start
    click_image(image_name="cerrar.png", confidence=0.9)
