from fastapi import APIRouter, Query
from loguru import logger

from api.models.telegram_notifier import ConfigurationsResponse, NotificationsResponse, SetTargetPriceResponse, Comparation
from api.modules.telegram_notifier import TelegramNotifier


router = APIRouter()


@router.get('/get_all', response_model=ConfigurationsResponse, summary="Listagem das configurações.")
def router_get_notification() -> dict:
    """Lista todas as configurações do BOT Telegram."""

    logger.log('LOG ROTA', "Chamada rota /get_all")
    return {"configuracoes": TelegramNotifier.make_current_cfg_dict()}


@router.get('/set_notifications', response_model=NotificationsResponse, summary="Configuração de notificações.")
def router_set_notification(notify_current_price: bool = Query(True, description="Notificação de preço atual."),
                            notify_if_gt_target_price: bool = Query(
                                True, description="Notificação para preço atual MAIOR que target."),
                            notify_if_lt_target_price: bool = Query(True, description="Notificação para preço atual MENOR que target.")) -> dict:
    """Configura a ativação/desativação das notificações para BOT Telegram."""

    logger.log('LOG ROTA', "Chamada rota /set_notifications")
    return {"notificacoes": TelegramNotifier.set_notifications(notify_current_price=notify_current_price,
                                                               notify_if_gt_target_price=notify_if_gt_target_price,
                                                               notify_if_lt_target_price=notify_if_lt_target_price)}


@router.get('/set_target_price', response_model=SetTargetPriceResponse, summary="Configuração de preços alvo.")
def router_set_target_price(comparation_type: Comparation = Query(..., description="Qual tipo de comparação será feita do preço atual com o target price."),
                            target_price: float = Query(..., description="Preço alvo desejado.")) -> dict:
    """Configura o preço alvo para comparação"""

    logger.log('LOG ROTA', "Chamada rota /set_target_price")
    return {"target_prices": TelegramNotifier.set_target_price(comparation_type.name, target_price)}
