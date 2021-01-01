from loguru import logger

from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs
from api.utils.text import make_current_price_message, make_if_target_price_message


class TelegramNotifier:
    notify_current_price: bool = True
    notify_if_gt_target_price: bool = True
    notify_if_lt_target_price: bool = True

    gt_target_price: float = None
    lt_target_price: float = None

    @classmethod
    def set_notifications(cls, notify_current_price: bool,
                          notify_if_gt_target_price: bool,
                          notify_if_lt_target_price: bool) -> dict:
        """Configura notificações para BOT do Telegram.

        :param notify_current_price: "Notificação de preço atual."
        :type notify_current_price: bool
        :param notify_if_gt_target_price: Notificação de preço atual maior que target.
        :type notify_if_gt_target_price: bool
        :param notify_if_lt_target_price: "Notificação de preço atual menor que target.
        :type notify_if_lt_target_price: bool
        :return: Resumo das configurações de notificação.
        :rtype: dict
        """
        logger.info("Modificando configurações de notificação.")
        cls.notify_current_price = notify_current_price
        cls.notify_if_gt_target_price = notify_if_gt_target_price
        cls.notify_if_lt_target_price = notify_if_lt_target_price

        return cls.make_current_cfg_dict()['notificacoes']

    @classmethod
    def set_target_price(cls, comparison_type: str, target_price: float) -> dict:
        """Configura preços alvo para monitoração.

        :param comparison_type: Comparação maior que ou menor que.
        :type comparison_type: str
        :param target_price: Preço alvo para comparação.
        :type target_price: float
        :return: Resumo das configurações de preço alvo.
        :rtype: dict
        """
        if comparison_type == "greater_than":
            cls.gt_target_price = target_price
        elif comparison_type == "lesser_than":
            cls.lt_target_price = target_price
        return cls.make_current_cfg_dict()['target_prices']

    @classmethod
    def make_current_cfg_dict(cls) -> dict:
        """Faz um dicionário contendo todas as configurações de monitoração.

        :return: Configurações de notificação e preços alvo.
        :rtype: dict
        """
        configurations = {
            "notificacoes": {
                "notify_current_price": cls.notify_current_price,
                "notify_if_gt_target_price": cls.notify_if_gt_target_price,
                "notify_if_lt_target_price": cls.notify_if_lt_target_price,
            },
            "target_prices": {
                "gt_target_price": cls.gt_target_price,
                "lt_target_price": cls.lt_target_price,
            }
        }
        return configurations

    @classmethod
    def send_current_price(cls, disable_notifications: bool) -> bool:
        """Envia preço atual (último, venda e compra) via Telegram.

        :param disable_notifications: Notificação silenciosa do Telegram.
        :type disable_notifications: bool
        :return: Se a mensagem foi enviada ou não.
        :rtype: bool
        """
        if cls.notify_current_price:
            logger.info("Obtendo valores BTC")
            ticker = BTCDataAPI.get_ticker()['ticker']

            logger.info("Enviando mensagem para Telegram")
            mensagem = make_current_price_message(
                ticker['last'], ticker['sell'], ticker['buy'])
            response = TelegramAPI.send_message(chat_id=envs.LOGGER_CHAT_ID, message=mensagem,
                                                disable_notifications=disable_notifications)

            return response['ok']

        logger.info("Notificação desativada.")
        return False

    @classmethod
    def send_if_gt_target_price(cls, disable_notifications: bool) -> bool:
        """Envia uma notificação via Telegram caso o preço atual seja maior que o preço target.

        :param target_price: Preço alvo.
        :type target_price: float
        :param disable_notifications: Notificação silenciosa do Telegram.
        :type disable_notifications: bool
        :return: Se a mensagem foi enviada ou não.
        :rtype: bool
        """
        logger.debug("Verificando notificação.")
        if cls.notify_if_gt_target_price:

            logger.debug("Verificando existência de preço alvo.")
            if cls.gt_target_price:
                logger.info("Obtendo valores BTC")
                last_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

                # Condicional de comparação
                if last_price >= cls.gt_target_price:
                    mensagem = make_if_target_price_message(
                        last_price, cls.gt_target_price)

                    logger.info("Enviando mensagem para Telegram")
                    response = TelegramAPI.send_message(
                        chat_id=envs.TARGET_CHAT_ID, message=mensagem, disable_notifications=disable_notifications)

                    return response['ok']

                logger.info("Condicional de comparação não satisfeita.")
            else:
                logger.info("Preço alvo não configurado.")
                return False

        logger.info("Notificação desativada.")
        return False

    @classmethod
    def send_if_lt_target_price(cls, disable_notifications: bool) -> dict:
        """Envia uma notificação via Telegram caso o preço atual seja menor que o preço target.

        :param target_price: Preço alvo.
        :type target_price: float
        :param disable_notifications: Notificação silenciosa do Telegram.
        :type disable_notifications: bool
        :return: Se a mensagem foi enviada ou não.
        :rtype: bool
        """
        logger.debug("Verificando notificação.")
        if cls.notify_if_lt_target_price:

            logger.debug("Verificando existência de preço alvo.")
            if cls.lt_target_price:
                logger.info("Obtendo valores BTC")
                last_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

                # Condicional de comparação
                if last_price <= cls.lt_target_price:
                    mensagem = make_if_target_price_message(
                        last_price, cls.lt_target_price)

                    logger.info("Enviando mensagem para Telegram")
                    response = TelegramAPI.send_message(
                        chat_id=envs.TARGET_CHAT_ID, message=mensagem, disable_notifications=disable_notifications)

                    return response['ok']

                logger.info("Condicional de comparação não satisfeita.")
            else:
                logger.info("Preço alvo não configurado.")
                return False

        logger.info("Notificação desativada.")
        return False
