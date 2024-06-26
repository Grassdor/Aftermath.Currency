from functools import lru_cache

from .settings.base import Settings


@lru_cache()
def get_settings(env_name: str = '') -> Settings:
    """Settings dependency."""
    env_file = Settings.Config.env_file

    if env_name:
        env_file += f'.{env_name}'

    return Settings(_env_file=env_file)


settings = get_settings()
