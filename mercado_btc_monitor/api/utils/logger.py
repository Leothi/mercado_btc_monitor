from loguru import logger

# Modificação do padrão do Loguru para string allignment
time = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>'
level = "<level>{level: ^18}</level>"
function = "<cyan>{name: <32}</cyan>:<cyan>{function: ^30}</cyan>:<cyan>{line: 4}</cyan>"
message = "<bold>{message}</bold>"

DEFAULT_FORMAT = ' | '.join([time, level, function, message])


# Função para Logging com mudanças acima
def log_request(level: str, method: str, endpoint: str, tempo: str = None):
    message = f"{method: ^4} | ENDPOINT: {endpoint: ^26}"
    if tempo:
        message = ' | '.join([message, f"TEMPO: {tempo}"])
    logger.log(level, message)
