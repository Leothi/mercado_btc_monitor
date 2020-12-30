from fastapi import APIRouter, Query
from loguru import logger

from api.models.price_monitoring import MonitoringResponse
from api.modules import price_monitoring
from api.settings import envs

router = APIRouter()


@router.get('/send_current_price', response_model=MonitoringResponse, summary="Relatório de valores atuais da BTC.")
def router_current(disable_notifications: bool = Query(True, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Retorna os valores atuais de compra, venda e último valor da BTC. Envia os valores para o chat cadastrado via Telegram. """

    logger.log('LOG ROTA', "Chamada rota /send_current_price")
    return {"enviado": price_monitoring.send_current_price(disable_notifications=disable_notifications)}


@router.get('/send_if_gt_target_price', response_model=MonitoringResponse, summary="Notificação de valor maior que Target.")
def router_target(target_price: float = Query(..., gt=0, description="Preço alvo para operação VENDA."),
                  disable_notifications: bool = Query(False, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Compara o valor atual com o Target e notifica via Telegram caso Atual >= Target. Ideal para operações de venda."""

    logger.log('LOG ROTA', "Chamada rota /send_if_gt_target_price")
    return {"enviado": price_monitoring.send_if_gt_target_price(target_price=target_price, disable_notifications=disable_notifications)}


@router.get('/send_if_lt_target_price', response_model=MonitoringResponse, summary="Notificação de valor menor que Target.")
def router_target(target_price: float = Query(..., gt=0, description="Preço alvo para operação COMPRA."),
                  disable_notifications: bool = Query(False, description="Notificação silenciosa (apenas vibração).")) -> dict:
    """Compara o valor atual com o Target e notifica via Telegram caso Atual <= Target. Ideal para operações de compra."""

    logger.log('LOG ROTA', "Chamada rota /send_if_lt_target_price")
    return {"enviado": price_monitoring.send_if_lt_target_price(target_price=target_price, disable_notifications=disable_notifications)}
