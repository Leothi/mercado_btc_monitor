import uvicorn

from api.settings import envs
from api.services.telegram import TelegramAPI
from api.services.mercado_btc.data_api import BTCDataAPI

def start():
    uvicorn.run('api:app',
                host=envs.FASTAPI_HOST, port=envs.FASTAPI_PORT,
                reload=envs.FASTAPI_RELOAD, access_log=envs.FASTAPI_ACCESS_LOG)


if __name__ == '__main__':
    btc_data_api = BTCDataAPI 
    telegram_api = TelegramAPI
    
    ticker = btc_data_api.get_ticker()['ticker']
    print(ticker)
    
    response = telegram_api.send_message(chat_id=envs.CHAT_ID, message=ticker, parse_mode=None)
    print(response)
