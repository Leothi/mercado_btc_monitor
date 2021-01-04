import uvicorn

from api.settings import envs
from api.services.telegram.bot import TelegramBOT

def start():
    uvicorn.run('api:app',
                host=envs.FASTAPI_HOST, port=envs.FASTAPI_PORT,
                reload=envs.FASTAPI_RELOAD, access_log=envs.FASTAPI_ACCESS_LOG)


if __name__ == '__main__':
    bot = TelegramBOT()
    bot.setup()
    # start()
