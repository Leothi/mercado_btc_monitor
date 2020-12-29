from ast import literal_eval

from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs


def send_current_price(parse_mode: str, disable_notifications: bool) -> bool:
    """Envia preço atual (último, venda e compra) via Telegram.

    :param parse_mode: Tipo de parsing de texto do Telegram.
    :type parse_mode: str
    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """    
    logger.info("Obtendo valores BTC")
    ticker = BTCDataAPI.get_ticker()['ticker']

    logger.info("Enviando mensagem para Telegram")
    mensagem = f"Último: {ticker['last']} \nVenda: {ticker['sell']} \nCompra: {ticker['buy']}"
    response = TelegramAPI.send_message(chat_id=envs.LOGGER_CHAT_ID, message=mensagem,
                                        parse_mode=parse_mode, disable_notifications=disable_notifications)

    return response['ok']


def send_if_gt_target_price(target_price: float, parse_mode: str, disable_notifications: bool) -> bool:
    """Envia uma notificação via Telegram caso o preço atual seja maior que o preço target.

    :param target_price: Preço alvo.
    :type target_price: float
    :param parse_mode: Tipo de parsing de texto do Telegram.
    :type parse_mode: str
    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """    
    logger.info("Obtendo valores BTC")
    ticker_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

    mensagem = f"VENDA\nTarget: {target_price}\tAtual: {ticker_price}\nPreço menor que target."

    if ticker_price >= target_price:
        logger.info("Enviando mensagem para Telegram")
        mensagem = f"VENDA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço MAIOR que target."
        response = TelegramAPI.send_message(
            chat_id=envs.TARGET_CHAT_ID, message=mensagem, parse_mode=parse_mode, disable_notifications=disable_notifications)

        return response['ok']
    return False


def send_if_lt_target_price(target_price: float, parse_mode: str, disable_notifications: bool) -> dict:
    """Envia uma notificação via Telegram caso o preço atual seja menor que o preço target.

    :param target_price: Preço alvo.
    :type target_price: float
    :param parse_mode: Tipo de parsing de texto do Telegram.
    :type parse_mode: str
    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """ 
    logger.info("Obtendo valores BTC")
    ticker_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

    mensagem = f"COMPRA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço maior que target."

    if ticker_price <= target_price:
        mensagem = f"COMPRA \nTarget: {target_price}\tAtual: {ticker_price}\nPreço MENOR que target."
        
        logger.info("Enviando mensagem para Telegram")
        response = TelegramAPI.send_message(
            chat_id=envs.TARGET_CHAT_ID, message=mensagem, parse_mode=parse_mode, disable_notifications=disable_notifications)

        return response['ok']
    return False
