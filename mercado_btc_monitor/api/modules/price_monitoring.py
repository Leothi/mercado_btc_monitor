from ast import literal_eval

from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs

def send_current_price(parse_mode: str) -> dict:
    logger.info("Obtendo valores BTC")
    ticker = BTCDataAPI.get_ticker()['ticker']
    
    logger.info("Enviando mensagem para Telegram")
    mensagem = f"Último: {ticker['last']} - Venda: {ticker['sell']} - Compra: {ticker['buy']}"
    response = TelegramAPI.send_message(chat_id=envs.CHAT_ID, message=mensagem, parse_mode=parse_mode)
    
    return response['ok']


def send_if_gt_target_price(target_price: float, parse_mode: str) -> dict:
    logger.info("Obtendo valores BTC")
    ticker_price = float(BTCDataAPI.get_ticker()['ticker']['last'])
    
    mensagem = f"Target: {target_price}. Atual: {ticker_price} - Preço menor que target."
    
    if ticker_price >= target_price:    
        logger.info("Enviando mensagem para Telegram")
        mensagem = f"Target: {target_price}. Atual: {ticker_price} - Preço MAIOR que target."
        TelegramAPI.send_message(chat_id=envs.CHAT_ID, message=mensagem, parse_mode=parse_mode)
        
    return mensagem