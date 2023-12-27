import pytest
import os
from unittest.mock import patch
from PIL import Image

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

TEST_IMG_FOLDER_PATH = "tests/data/siqual_screenshots"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Can't run pyautogui in headless systems")
@pytest.mark.parametrize(
    "needle, haystack, expected_coords, params",
    [
        (
            "puntosSuspensivos.png",
            "1.png",
            (796, 328),
            {"index": 1, "confidence": 0.95},
        ),
        (
            "flecha.png",
            "2.png",
            (451, 275),
            {"index": 2, "confidence": 1},
        ),
        (
            "CIMALV.png",
            "3.png",
            (401, 335),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "CLK1.png",
            "3.png",
            (401, 348),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "CPC30.png",
            "3.png",
            (401, 361),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "CPC40.png",
            "3.png",
            (401, 374),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "CPN40.png",
            "3.png",
            (401, 387),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "CPN40ARS.png",
            "3.png",
            (401, 400),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "FAR.png",
            "3.png",
            (401, 413),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "casilleroSeleccionado.png",
            "4.png",
            (219, 511),
            {"index": 0, "confidence": 1},
        ),
        (
            "cargarDatos.png",
            "5.png",
            (732, 254),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "copiarRIC.png",
            "5.png",
            (839, 248),
            {"index": 0, "confidence": 0.95},
        ),
        (
            "grabar.png",
            "5.png",
            (952, 254),
            {"index": 0, "confidence": 0.90},
        ),
        (
            "RIE.png",
            "6.png",
            (1058, 254),
            {"index": 0, "confidence": 0.90},
        ),
        (
            "ensayosResultados.png",
            "7.png",
            (970, 350),
            {"index": 0, "confidence": 0.90},
        ),
        (
            "cuadroseleccionado.png",
            "8.png",
            (1310, 324),
            {"index": 1, "confidence": 0.90},
        ),
        (
            "grabarDatos.png",
            "9.png",
            (514, 254),
            {"index": 0, "confidence": 0.90},
        ),
        (
            "cerrar.png",
            "9.png",
            (1346, 254),
            {"index": 0, "confidence": 0.90},
        ),
        (
            "cerrar.png",
            "7.png",
            (1198, 350),
            {"index": 1, "confidence": 0.90},
        ),
        (
            "cerrar.png",
            "6.png",
            (1287, 254),
            {"index": 0, "confidence": 0.90},
        ),
    ],
)
def test_clicks_images(monkeypatch, needle, haystack, expected_coords, params):
    def fake_screenshot(*args, **kwargs):
        # Fake the pyscreeze screenshot function so it returns the previously saved image
        # instead of taking a screenshot
        im = Image.open(f"{TEST_IMG_FOLDER_PATH}/{haystack}")
        im.load()
        return im

    monkeypatch.setattr("pyscreeze.screenshot", fake_screenshot)

    with patch("pyautogui.click") as mocked_pyautogui_click:
        from paste_data import click_image

        click_image(needle, **params)

        # If click_image is called, it means that pyautogui found the image at the expected
        # coords
        mocked_pyautogui_click.assert_called_once_with(*expected_coords)
