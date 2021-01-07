import requests
from loguru import logger
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from project.settings import envs


class TelegramBOT:
    _CURRENT_PRICE_URL = envs.API_BASE_URL + envs.CURRENT_PRICE_ENDPOINT

    @staticmethod
    def _price(update: Update, context: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("Preço atual", callback_data='current'),
                InlineKeyboardButton("Preço alvo", callback_data='target'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            'Please choose:', reply_markup=reply_markup)

    @classmethod
    def _button(cls, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        if query.data == 'current':

            logger.info(f"Enviando request para {cls._CURRENT_PRICE_URL}")
            requests.get(cls._CURRENT_PRICE_URL)
            text = "Preço atual."
        else:
            text = 'Preço alvo'
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

        updater.start_polling()
        updater.idle()
