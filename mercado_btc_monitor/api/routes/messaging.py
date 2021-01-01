from fastapi import APIRouter, Query
from loguru import logger

from api.models.telegram_notifier import SendResponse
from api.modules.telegram_notifier import TelegramNotifier

router = APIRouter()


@router.get('/current_price', response_model=SendResponse, summary="Relatório de valores atuais da BTC.")
def router_current(disable_notifications: bool = Query(True, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Retorna os valores atuais de compra, venda e último valor da BTC. Envia os valores para o chat cadastrado via Telegram. """

    logger.log('LOG ROTA', "Chamada rota /current_price.")
    return {"enviado": TelegramNotifier.send_current_price(disable_notifications=disable_notifications)}


@router.get('/if_gt_target_price', response_model=SendResponse, summary="Notificação de valor atual maior que target.")
def router_gt_target(disable_notifications: bool = Query(False, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Compara o valor atual com o Target e notifica via Telegram caso Atual >= Target.

    Ideal para operações de venda.

    Envia somente se a notificação foi ativada e o preço alvo settado.
    """

    logger.log('LOG ROTA', "Chamada rota /if_gt_target_price.")
    return {"enviado": TelegramNotifier.send_if_gt_target_price(disable_notifications=disable_notifications)}


@router.get('/if_lt_target_price', response_model=SendResponse, summary="Notificação de valor atual menor que target.")
def router_lt_target(disable_notifications: bool = Query(False, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Compara o valor atual com o Target e notifica via Telegram caso Atual <= Target.

    Ideal para operações de compra.

    Envia somente se a notificação foi ativada e o preço alvo settado.
    """

    logger.log('LOG ROTA', "Chamada rota /if_lt_target_price.")
    return {"enviado": TelegramNotifier.send_if_lt_target_price(disable_notifications=disable_notifications)}
