import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from api import __version__
from api.schemas import DEFAULT_RESPONSES_JSON
from api.routes import messaging, configuration
from api.modules.default.middleware import Middleware
from api.exceptions import ExceptionHandler
from api.settings import envs


def get_app():
    # Logger configuration
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": envs.LOG_LEVEL,
                "format": envs.LOGURU_FORMAT
            }
        ]
    )

    # Logger level creation
    logger.level('REQUEST RECEBIDA', no=37, color="<yellow>")
    logger.level('REQUEST FINALIZADA', no=38, color="<yellow>")
    logger.level('LOG ROTA', no=39, color="<light-green>")

    # Saída para arquivo logger
    logger.add("./logs/teste.log", level=0,
               format=envs.LOGURU_FORMAT, rotation='500 MB')
    logger.add("./logs/teste_error.log", level=40,
               format=envs.LOGURU_FORMAT, rotation='500.MB')

    async def startup_event():
        logger.info("Starting API")

    async def shutdown_event():
        logger.info("API shutdown")

    # Instância API
    app = FastAPI(title='Mercado BTC Monitor',
                  description="Api para monitoração de Criptos pela Mercado BTC.",
                  version=__version__,
                  root_path=envs.FASTAPI_ROOT_PATH,
                  on_startup=[startup_event],
                  on_shutdown=[shutdown_event],
                  )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(messaging.router,
                       prefix='/send',
                       tags=["Envio de mensagem"],
                       responses={**DEFAULT_RESPONSES_JSON}
                       )

    app.include_router(configuration.router,
                       prefix='/cfg',
                       tags=["Configurações"],
                       responses={**DEFAULT_RESPONSES_JSON}
                       )

    # API Modules
    Middleware(app)
    ExceptionHandler(app)

    return app
