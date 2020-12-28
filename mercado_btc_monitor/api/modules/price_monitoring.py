from ast import literal_eval

from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs

def send_current_prince(parse_mode: str) -> dict:
    logger.info("Obtendo valores BTC")
    ticker = BTCDataAPI.get_ticker()['ticker']
    
    logger.info("Enviando mensagem para Telegram")
    response = TelegramAPI.send_message(chat_id=envs.CHAT_ID, message=ticker, parse_mode=None)
    
    return literal_eval(response['result']['text'])