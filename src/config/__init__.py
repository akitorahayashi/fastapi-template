from .app_settings import AppSettings
from .db_settings import DBSettings

db_settings = DBSettings()
app_settings = AppSettings()

__all__ = ["db_settings", "app_settings"]
