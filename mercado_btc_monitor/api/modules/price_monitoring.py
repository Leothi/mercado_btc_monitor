from ast import literal_eval

from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs

def send_current_price(parse_mode: str, disable_notifications: bool) -> dict:
    logger.info("Obtendo valores BTC")
    ticker = BTCDataAPI.get_ticker()['ticker']
    
    logger.info("Enviando mensagem para Telegram")
    mensagem = f"Último: {ticker['last']} \nVenda: {ticker['sell']} \nCompra: {ticker['buy']}"
    response = TelegramAPI.send_message(chat_id=envs.LOGGER_CHAT_ID, message=mensagem, parse_mode=parse_mode, disable_notifications=disable_notifications)
    
    return response['ok']


def send_if_gt_target_price(target_price: float, parse_mode: str, disable_notifications: bool) -> dict:
    logger.info("Obtendo valores BTC")
    ticker_price = float(BTCDataAPI.get_ticker()['ticker']['last'])
    
    mensagem = f"VENDA\nTarget: {target_price}\tAtual: {ticker_price}\nPreço menor que target."
    
    if ticker_price >= target_price:    
        logger.info("Enviando mensagem para Telegram")
        mensagem = f"VENDA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço MAIOR que target."
        response = TelegramAPI.send_message(chat_id=envs.TARGET_CHAT_ID, message=mensagem, parse_mode=parse_mode, disable_notifications=disable_notifications)
        
    return response['ok']

def send_if_lt_target_price(target_price: float, parse_mode: str, disable_notifications: bool) -> dict:
    logger.info("Obtendo valores BTC")
    ticker_price = float(BTCDataAPI.get_ticker()['ticker']['last'])
    
    mensagem = f"COMPRA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço maior que target."
    
    if ticker_price <= target_price:    
        logger.info("Enviando mensagem para Telegram")
        mensagem = f"COMPRA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço MENOR que target."
        response = TelegramAPI.send_message(chat_id=envs.TARGET_CHAT_ID, message=mensagem, parse_mode=parse_mode, disable_notifications=disable_notifications)
        
    return response['ok']