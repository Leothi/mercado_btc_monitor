import requests

from api.settings import envs

# https://core.telegram.org/bots/api


class TelegramAPI:
    """Api de BOT do Telegram. """ 
    base_url: str = envs.BOT_API_URL + envs.BOT_TOKEN

    @classmethod
    def send_message(cls, message: str, chat_id: str, parse_mode: str = envs.PARSE_MODE, disable_notifications: bool = False) -> dict:
        """Envia mensagem para um chat do Telegram.

        :param message: Mensagem a ser enviada.
        :type message: str
        :param chat_id: ID do chat de destino.
        :type chat_id: str
        :param parse_mode: Tipo de parsing de texto do Telegram., defaults to envs.PARSE_MODE
        :type parse_mode: str, optional
        :param disable_notifications: Notificação silenciosa do Telegram., defaults to False
        :type disable_notifications: bool, optional
        :return: Dicionário contendo informações da API de envio.
        :rtype: dict
        """        
        disable_notifications = 'true' if disable_notifications else 'false'
        url = f'{cls.base_url}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}&disable_notification={disable_notifications}'
        response = requests.get(url)
        return response.json()
