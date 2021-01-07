import os

from dotenv import load_dotenv, find_dotenv
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

    if find_dotenv():
        load_dotenv()

    # Logger
    LOGURU_FORMAT: str = DEFAULT_FORMAT

    # GCP
    API_BASE_URL = os.environ.get('API_BASE_URL', '')
    
    # Requests
    CURRENT_PRICE_ENDPOINT = os.environ.get(
        'CURRENT_PRICE_ENDPOINT', '/send/current_price')
    IF_TARGET_PRICE_ENDPOINT = os.environ.get(
        'IF_TARGET_PRICE_ENDPOINT', '/send/if_target_price')

    # Telegram
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    LOGGER_CHAT_ID = os.environ.get('LOGGER_CHAT_ID', '')
    TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID', '')


envs = EnvironmentVariables()
