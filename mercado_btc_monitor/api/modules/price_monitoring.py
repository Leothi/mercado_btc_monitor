from ast import literal_eval

from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs
from api.utils.text import make_current_price_message, make_if_target_price_message


def send_current_price(disable_notifications: bool) -> bool:
    """Envia preço atual (último, venda e compra) via Telegram.

    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """
    logger.info("Obtendo valores BTC")
    ticker = BTCDataAPI.get_ticker()['ticker']

    logger.info("Enviando mensagem para Telegram")
    mensagem = make_current_price_message(
        ticker['last'], ticker['sell'], ticker['buy'])
    response = TelegramAPI.send_message(chat_id=envs.LOGGER_CHAT_ID, message=mensagem,
                                        disable_notifications=disable_notifications)

    return response['ok']


def send_if_gt_target_price(target_price: float, disable_notifications: bool) -> bool:
    """Envia uma notificação via Telegram caso o preço atual seja maior que o preço target.

    :param target_price: Preço alvo.
    :type target_price: float
    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """
    logger.info("Obtendo valores BTC")
    last_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

    if last_price >= target_price:
        mensagem = make_if_target_price_message(last_price, target_price)

        logger.info("Enviando mensagem para Telegram")
        response = TelegramAPI.send_message(
            chat_id=envs.TARGET_CHAT_ID, message=mensagem, disable_notifications=disable_notifications)

        return response['ok']
    return False


def send_if_lt_target_price(target_price: float, disable_notifications: bool) -> dict:
    """Envia uma notificação via Telegram caso o preço atual seja menor que o preço target.

    :param target_price: Preço alvo.
    :type target_price: float
    :param disable_notifications: Notificação silenciosa do Telegram.
    :type disable_notifications: bool
    :return: Se a mensagem foi enviada ou não.
    :rtype: bool
    """
    logger.info("Obtendo valores BTC")
    last_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

    if last_price <= target_price:
        mensagem = make_if_target_price_message(last_price, target_price)

        logger.info("Enviando mensagem para Telegram")
        response = TelegramAPI.send_message(
            chat_id=envs.TARGET_CHAT_ID, message=mensagem, disable_notifications=disable_notifications)

        return response['ok']
    return False
