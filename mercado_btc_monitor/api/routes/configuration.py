from fastapi import APIRouter, Query
from loguru import logger

from api.models.telegram_notifier import NotificationsResponse
from api.modules.telegram_notifier import TelegramNotifier
from api.settings import envs


router = APIRouter()


@router.get('/set_notifications', response_model=NotificationsResponse, summary="Configuração de notificações para BOT.")
def router_set_notification(notify_current_price: bool = Query(True, description="Notificação de preço atual."),
                            notify_if_gt_target_price: bool = Query(True, description="Notificação para preço target MAIOR que atual."),
                            notify_if_lt_target_price: bool = Query(True, description="Notificação para preço target MENOR que atual.")) -> dict:
    """Configura a ativação/desativação das notificações para BOT Telegram."""

    logger.log('LOG ROTA', "Chamada rota /set_notification")
    return {"notificacoes": TelegramNotifier.set_notifications(notify_current_price=notify_current_price,
                                                               notify_if_gt_target_price=notify_if_gt_target_price,
                                                               notify_if_lt_target_price=notify_if_lt_target_price)}


@router.get('/get_notifications', response_model=NotificationsResponse, summary="Listagem das configurações do BOT.")
def router_get_notification() -> dict:
    """Lista as configurações de ativação/desativação das notificações para BOT Telegram."""

    logger.log('LOG ROTA', "Chamada rota /get_notifications")
    return {"notificacoes": TelegramNotifier.make_current_cfg_dict()}
