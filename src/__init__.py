import os

__version__ = "2.4.6"

HEADLESS_MODE = os.environ.get("AUTOSIQUAL_HEADLESS_MODE","").lower() == "true"