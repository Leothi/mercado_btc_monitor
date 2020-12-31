from pydantic import Field, BaseModel
from typing import Dict

from api.models import SuccessResponse


class SendResponse(SuccessResponse):
    """Response model to /send prefix"""
    enviado: bool
    
class NotificationsBase(BaseModel):
    """Base model for notifications response"""
    current_price: bool
    gt_target_price: bool
    lt_target_price: bool
    
class NotificationsResponse(SuccessResponse):
    """Response model to /set_notifcations or /get_notifications on /monitoring prefix"""
    notificacoes: NotificationsBase
