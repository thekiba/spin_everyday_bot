from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str
    superuser: int
