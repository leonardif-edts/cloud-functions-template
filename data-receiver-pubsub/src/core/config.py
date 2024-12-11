import os

from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PUBSUB_PROJECT: str
    PUBSUB_TOPIC: str
    API_KEY: Optional[SecretStr] = None

    class Config:
        env_file = None
        extra = "allow"


def get_config():
    """
    Get Config

    Get config from env variables. Specify `env_file` for local .env files
    and 'ENV' as environment variable to read environment variables from
    locals.
    """
    env = os.getenv("ENV", "dev")
    env_file = {
        "dev": ".env.dev"
    }.get(env, None)

    filepath = os.path.join("envs", env_file) if (env_file) else None
    return Config(_env_file=filepath)
