from telegram import Update, Bot, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler

from api.settings import envs


class TelegramBOT:
    def __init__(self):
        self.bot = Bot(envs.BOT_TOKEN)
        self.bot_token = envs.BOT_TOKEN

    @staticmethod
    def start(update: Update, context: CallbackContext):
        # context.bot.send_message(chat_id=update.effective_chat.id, text="Bot de monitoração de Bitcoin!")
        reply_keyboard = [['Boy', 'Girl', 'Other']]

        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),)

    @staticmethod
    def keyboard(update: Update, context: CallbackContext):
        query = update.callback_query
        # Get Bot from CallbackContext
        bot = context.bot

        keyboard = [
            [InlineKeyboardButton("Preço Atual", callback_data='teste'),
             InlineKeyboardButton("Atual > Target", callback_data='HRlist8'),
             InlineKeyboardButton("Atual < Target", callback_data='HRlist8')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Selecione o tipo de operação:',
                                  reply_markup=reply_markup,)

    def setup(self):
        updater = Updater(token=self.bot_token, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        keyboard_handler = CommandHandler('keyboard', self.keyboard)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(keyboard_handler)

        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    bot = TelegramBOT()
    bot.setup()
