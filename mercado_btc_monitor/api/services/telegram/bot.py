from loguru import logger

from telegram import Update, Bot, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from api.services.mercado_btc.data_api import BTCDataAPI
from api.settings import envs
from api.utils.text import make_current_price_message, make_if_target_price_message


class TelegramBOT:
    notify_current_price: bool = True
    notify_if_gt_target_price: bool = True
    notify_if_lt_target_price: bool = True

    gt_target_price: float = None
    lt_target_price: float = None

    bot = Bot(envs.BOT_TOKEN)

    def __init__(self):
        self.setup()

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

        logger.success("Notificações modificadas.")
        return cls._make_current_cfg_dict()['notificacoes']

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
        logger.info(f"Ajustando preço limite para '{comparison_type}'.")

        if comparison_type == "greater_than":
            cls.gt_target_price = target_price
        elif comparison_type == "lesser_than":
            cls.lt_target_price = target_price

        logger.success("Preço ajustado.")
        return cls._make_current_cfg_dict()['target_prices']

    @classmethod
    def _make_current_cfg_dict(cls) -> dict:
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
    def send_current_price(cls, disable_notification: bool = False) -> bool:
        """Envia preço atual (último, venda e compra) via Telegram.

        :param disable_notifications: Notificação silenciosa do Telegram.
        :type disable_notifications: bool
        :return: Se a mensagem foi enviada ou não.
        :rtype: bool
        """
        logger.debug("Verificando notificação.")
        if cls.notify_current_price:
            logger.info("Obtendo valores BTC.")
            ticker = BTCDataAPI.get_ticker()['ticker']

            logger.info("Enviando mensagem para Telegram")
            message = make_current_price_message(
                ticker['last'], ticker['sell'], ticker['buy'])

            cls.bot.send_message(chat_id=envs.TARGET_CHAT_ID,
                                 text=message,
                                 disable_notification=disable_notification,
                                 parse_mode=envs.PARSE_MODE)

            logger.success("Mensagem enviada com sucesso.")

            return True

        logger.success("Notificação desativada.")
        return False

    @classmethod
    def send_if_target_price(cls, comparison_type: str, disable_notification: bool = False) -> bool:
        """Envia uma notificação via Telegram caso o preço atual seja menor ou menor que o preço target.

        :param comparison_type: Tipo de comparação com o preço atual.
        :type comparison_type: str
        :param disable_notifications: Notificação silenciosa do Telegram.
        :type disable_notifications: bool
        :return: Se a mensagem foi enviada ou não.
        :rtype: bool
        """
        send_message = False

        # Atribuindo valores de acordo com o tipo de comparação
        if comparison_type == "greater_than":
            target_price = cls.gt_target_price
            notify = cls.notify_if_gt_target_price
        elif comparison_type == "lesser_than":
            target_price = cls.lt_target_price
            notify = cls.notify_if_lt_target_price

        logger.debug("Verificando notificação.")
        if notify:

            logger.debug("Verificando existência de preço alvo.")
            if target_price:
                logger.info("Obtendo valores BTC.")
                last_price = float(BTCDataAPI.get_ticker()['ticker']['last'])

                comparison = last_price >= target_price

                # Condicional verdadeira
                if comparison and comparison_type == "greater_than":
                    send_message = True
                elif not comparison and comparison_type == "lesser_than":
                    send_message = True
                # Condicional falsa
                else:
                    logger.success("Condicional de comparação não satisfeita.")

                # Envia mensagem caso condicional verdadeira
                if send_message:
                    message = make_if_target_price_message(
                        last_price, target_price)

                    logger.info("Enviando mensagem para Telegram.")
                    response = cls.bot.send_message.send_message(chat_id=envs.TARGET_CHAT_ID,
                                                                 text=message,
                                                                 disable_notification=disable_notification,
                                                                 parse_mode=envs.PARSE_MODE)

                    if response['ok']:
                        logger.success("Mensagem enviada com sucesso.")

                        return response['ok']

            else:
                logger.success("Preço alvo não configurado.")
        else:
            logger.success("Notificação desativada.")
        return False

    @staticmethod
    def _price(update: Update, context: CallbackContext):
        """
        docstring
        """
        keyboard = [
            [
                InlineKeyboardButton("Preço atual", callback_data='current'),
                InlineKeyboardButton("Preço alvo", callback_data='target'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    @classmethod
    def _button(cls, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        if query.data == 'current':
            cls.send_current_price()
            text = "Preço atual."
        else:
            print("pass")
        query.edit_message_text(text=text)

    @staticmethod
    def _start(update: Update, context: CallbackContext):
        reply_keyboard = [
            ['Boy', 'Girl', 'Other']
        ]
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=reply_markup)

    @classmethod
    def setup(cls):
        updater = Updater(token=envs.BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', cls._start)
        price_handler = CommandHandler('price', cls._price)
        button_handler = CallbackQueryHandler(cls._button)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(price_handler)
        dispatcher.add_handler(button_handler)

        updater.start_polling(poll_interval=2)
        updater.idle()

if __name__ == "__main__":
    bot = TelegramBOT
    bot.setup()
