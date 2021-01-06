from telegram import Update, Bot, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler

from api.modules.telegram_notifier import TelegramNotifier
from api.settings import envs


class TelegramBOT:
    def __init__(self):
        self.bot = Bot(envs.BOT_TOKEN)
        self.bot_token = envs.BOT_TOKEN
        
    @staticmethod
    def price(update: Update, context: CallbackContext):
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
        
    @staticmethod
    def button(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        if query.data == 'current':
            TelegramNotifier.send_current_price(disable_notifications=False)
            text = "Preço atual."
        else:
            print("pass")
        query.edit_message_text(text=text)
        
        
    @staticmethod
    def start(update: Update, context: CallbackContext):
        reply_keyboard = [
            ['Boy', 'Girl', 'Other']
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=reply_markup)

    @staticmethod
    def keyboard(update: Update, context: CallbackContext):
        query = update.callback_query
        bot = context.bot

        keyboard = [
            ["Preço Atual", "Atual > Target", "Atual < Target",]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text('Selecione o tipo de operação:',
                                  reply_markup=reply_markup,)

    def setup(self):
        updater = Updater(token=self.bot_token, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        keyboard_handler = CommandHandler('keyboard', self.keyboard)
        price_handler = CommandHandler('price', self.price)
        button_handler = CallbackQueryHandler(self.button)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(price_handler)
        dispatcher.add_handler(keyboard_handler)
        dispatcher.add_handler(button_handler)

        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    bot = TelegramBOT()
    bot.setup()
