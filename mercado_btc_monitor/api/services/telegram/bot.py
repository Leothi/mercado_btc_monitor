from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

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
                reply_keyboard, one_time_keyboard=True),
        )
        return GENDER
       
    def setup(self):
        updater = Updater(token=self.bot_token, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', self.start)

        dispatcher.add_handler(start_handler)
        
        updater.start_polling()
        updater.idle()
   
    
if __name__ == "__main__":
    bot = TelegramBOT()
    bot.setup()
    
