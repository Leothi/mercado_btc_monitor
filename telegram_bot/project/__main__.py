import sys

from loguru import logger

from project.modules.bot import TelegramBOT
from project.settings import envs


# Configuração do Logger
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": 10,
            "format": envs.LOGURU_FORMAT
        }
    ]
)

# Saída para arquivo logger
logger.add("./logs/teste.log", level=0,
           format=envs.LOGURU_FORMAT, rotation='500 MB')
logger.add("./logs/teste_error.log", level=40,
           format=envs.LOGURU_FORMAT, rotation='500.MB')

if __name__ == "__main__":
    bot = TelegramBOT
    logger.info("Subindo BOT Telegram")
    bot.setup()
