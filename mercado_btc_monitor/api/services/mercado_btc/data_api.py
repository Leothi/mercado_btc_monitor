import requests

from api.settings import envs

# https://www.mercadobitcoin.com.br/api-doc/


class BTCDataAPI:
    """Api de Dados da corretora Mercado Bitcoin. """
    _base_url = envs.DATA_API_URL

    @classmethod
    def get_ticker(cls) -> dict:
        """Requisição Ticker da corretora.

        :return: Resumo dos preços atuais da moeda.
        :rtype: dict
        """
        url = f'{cls._base_url}/ticker'

        response = requests.get(url)
        return response.json()
