import os

from pydantic import BaseSettings
from enum import Enum

from api.utils.logger import DEFAULT_FORMAT


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
        
    # FastAPI
    FASTAPI_HOST: str = '0.0.0.0'
    FASTAPI_PORT: int = 8080
    FASTAPI_RELOAD: bool = False
    FASTAPI_ACCESS_LOG: bool = False
   
    # Logger
    LOGGER_SWAGGER: bool = False
    LOGGER_IGNORE: str = '/docs /redoc /openapi.json /metrics /health /favicon.ico / /# /_static/perfil_ico.png /_static/perfil.png'
    LOGURU_FORMAT: str = DEFAULT_FORMAT
    LOG_LOCAL: bool = False
    
    # Telegram
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    LOGGER_CHAT_ID = os.environ.get('LOGGER_CHAT_ID', '')
    TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID', '')
    BOT_API_URL: str = 'https://api.telegram.org/bot'
    PARSE_MODE: str = 'MarkdownV2'    
    
    # Mercado BTC
    DATA_API_URL: str = "https://www.mercadobitcoin.net/api/BTC"

envs = EnvironmentVariables()

# Envs Gunicorn
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')
workers = os.environ.get('GUNICORN_WORKERS', '1')
reload = os.environ.get('GUNICORN_RELOAD', False)
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
timeout = os.environ.get('GUNICORN_TIMEOUT', 30)
graceful_timeout = os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', 30)
