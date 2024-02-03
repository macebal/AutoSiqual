import os
from models.user_config import UserConfig

__version__ = "2.4.7"


try:
    CONFIG = UserConfig.from_json()
except Exception:
    CONFIG = None


HEADLESS_MODE = os.environ.get("AUTOSIQUAL_HEADLESS_MODE", "").lower() == "true"
