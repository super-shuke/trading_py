from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    SECRET_KEY: str
    TG_TOKEN: str
    TG_CHANNEL_ID: str
    TG_CHAT_ID: list[str]

    model_config = ConfigDict(env_file="setting.env")


settings = Settings()
