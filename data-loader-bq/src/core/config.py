import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BQ_PROJECT: str
    BQ_DATASET: str

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
