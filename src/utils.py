import ctypes
import logging
import pyautogui
from PyQt5.QtCore import QEventLoop, QTimer
from src import HEADLESS_MODE
from typing import SupportsFloat, SupportsInt


def numlock_is_active() -> bool:
    """Returns a boolean indicating whether the num lock key is pressed or not

    Returns
    -------
    bool
        True if the numlock key is pressed, False otherwise

    """
    dll = ctypes.WinDLL("User32.dll")
    VK_NUMLOCK = 0x90
    return bool(dll.GetKeyState(VK_NUMLOCK))


def qt_sleep(seconds: SupportsInt) -> None:
    """Create a sleep period that doesn't freeze the UI.

    Parameters
    ----------
    seconds : SupportsInt
        The number of seconds to sleep.
    """
    loop = QEventLoop()
    QTimer.singleShot(int(seconds * 1000), loop.quit)
    loop.exec_()


def click_image(image_name: str, index: int = 0, confidence: SupportsFloat = 0.999) -> None:
    """Clicks the region onscreen that is equal to the image in `image_name`.

    Parameters
    ----------
    image_name : str
        The name and extension of an image located in the img folder
    index : int, optional
         If there is more than one result for that image, the index in the resulting list, by default 0
    confidence : SupportsFloat, optional
        The confidence of the found region (1 means an exact match), by default 0.999

    """

    logger = logging.getLogger("ui_logger")
    path = f"img/{image_name}"

    if HEADLESS_MODE:
        logger.debug(f"HEADLESS MODE: Skipping click of {path} with confidence={confidence}")
        return

    results = list(pyautogui.locateAllOnScreen(path, confidence=confidence))

    if len(results) == 0:
        logger.critical(f"No se encuentra el boton {image_name}. ¿La ventana está cerrada?")
        logger.critical("El programa terminó abruptamente.")
        qt_sleep(5)
        exit(1)

    coords_x, coords_y = pyautogui.center(results[index])
    pyautogui.click(coords_x, coords_y)
