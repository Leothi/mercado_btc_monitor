import requests

from api.settings import envs

# https://core.telegram.org/bots/api

class TelegramAPI:
    base_url: str = envs.BOT_API_URL + envs.BOT_TOKEN 
    
    @classmethod
    def send_message(cls, message: str, chat_id: str, parse_mode: str = envs.PARSE_MODE) -> dict:
        url = f'{cls.base_url}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}'
        
        response = requests.get(url)
        return response.json()
