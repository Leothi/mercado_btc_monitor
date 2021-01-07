import uvicorn

from api.settings import envs

if __name__ == "__main__":
    bot = TelegramBOT
    bot.setup()
