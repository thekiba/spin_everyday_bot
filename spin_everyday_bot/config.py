from contextvars import ContextVar

from pydantic import BaseSettings


class Settings(BaseSettings):  # todo: import settings from .ini
    token: str
    superuser: int


config_ctx: ContextVar[Settings] = ContextVar('settings_ctx')

__all__ = ('Settings', 'config_ctx')
