from datetime import timedelta, timezone

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Application settings
    """

    debug: bool = Field(False, env="DEBUG")
    timezone_offset: int = Field(3, env="TIMEZONE_OFFSET")

    def get_tz(self):
        return timezone(timedelta(hours=self.timezone_offset))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
