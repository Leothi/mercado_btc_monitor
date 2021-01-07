import os

from pydantic import BaseSettings
from enum import Enum

from project.utils.logger import DEFAULT_FORMAT


class EnvironmentEnum(Enum):
    LOCAL = 'LOCAL'
    DESENV = 'DESENV'
    HM = 'HM'
    SERVICE = 'SERVICE'


class EnvironmentVariables(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = 'LOCAL'

    if ENVIRONMENT == EnvironmentEnum.LOCAL.name:
        from dotenv import load_dotenv  # noqa
        load_dotenv()
    else:
        pass

    # Logger
    LOGGER_SWAGGER: bool = False
    LOGGER_IGNORE: str = '/docs /redoc /openapi.json /metrics /health /favicon.ico / /# /_static/perfil_ico.png /_static/perfil.png'
    LOGURU_FORMAT: str = DEFAULT_FORMAT
    LOG_LOCAL: bool = False

    # GCP
    API_BASE_URL = os.environ.get('API_BASE_URL', '')
    CURRENT_PRICE_ENDPOINT = os.environ.get(
        'CURRENT_PRICE_ENDPOINT', '/send/current_price')
    IFT_TARGET_PRICE_ENDPOINT = os.environ.get(
        'IF_TARGET_PRICE_ENDPOINT', '/send/if_target_price')

    # Telegram
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    LOGGER_CHAT_ID = os.environ.get('LOGGER_CHAT_ID', '')
    TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID', '')
    BOT_API_URL: str = 'https://api.telegram.org/bot'
    PARSE_MODE: str = 'Markdown'


envs = EnvironmentVariables()
