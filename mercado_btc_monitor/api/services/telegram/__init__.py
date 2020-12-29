import requests

from api.settings import envs

# https://core.telegram.org/bots/api


class TelegramAPI:
    base_url: str = envs.BOT_API_URL + envs.BOT_TOKEN

    @classmethod
    def send_message(cls, message: str, chat_id: str, parse_mode: str = envs.PARSE_MODE, disable_notifications: bool = False) -> dict:
        disable_notifications = 'true' if disable_notifications else 'false'
        url = f'{cls.base_url}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}&disable_notification={disable_notifications}'
        response = requests.get(url)
        return response.json()
