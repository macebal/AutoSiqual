from models.user_config import UserConfig

__version__ = "2.4.6"


try:
    CONFIG = UserConfig.from_json()
except Exception:
    CONFIG = None
