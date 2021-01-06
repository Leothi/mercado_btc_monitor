from fastapi import APIRouter, Query
from loguru import logger

from api.models.telegram_notifier import SendResponse, Comparison
from api.services.telegram.bot import TelegramBOT

router = APIRouter()


@router.get('/current_price', response_model=SendResponse, summary="Relatório de valores atuais da BTC.")
def router_current(disable_notification: bool = Query(True, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Retorna os valores atuais de compra, venda e último valor da BTC. Envia os valores para o chat cadastrado via Telegram. """

    logger.log('LOG ROTA', "Chamada rota /current_price.")
    return {"enviado": TelegramBOT.send_current_price(disable_notification=disable_notification)}


@router.get('/if_target_price', response_model=SendResponse, summary="Notificação de valor atual menor ou maior que target.")
def router_target(comparison_type: Comparison = Query(..., description="Qual tipo de comparação será feita entre o preço atual com o target price."),
                  disable_notification: bool = Query(False, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Compara o valor atual com o Target e notifica via Telegram caso Atual <= Target ou Atual >= Target dependendo do tipo de comparação.

    Envia somente se a notificação foi ativada e o preço alvo settado.
    """

    logger.log('LOG ROTA', "Chamada rota /if_target_price.")
    return {"enviado": TelegramBOT.send_if_target_price(comparison_type=comparison_type,
                                                          disable_notification=disable_notification)}
