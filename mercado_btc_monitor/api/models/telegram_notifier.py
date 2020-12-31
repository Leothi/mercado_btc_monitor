from pydantic import BaseModel
from typing import Dict, Union

from api.models import SuccessResponse


class SendResponse(SuccessResponse):
    """Response model to /send prefix"""
    enviado: bool


class NotificationsBase(BaseModel):
    """Base model for /set_notifications on /cfg prefix"""
    current_price: bool
    gt_target_price: bool
    lt_target_price: bool


class TargetPriceBase(BaseModel):
    target_price: float


class NotificationsResponse(SuccessResponse):
    """Response model to /set_notifications on /cfg prefix"""
    notificacoes: NotificationsBase


class ConfigurationsResponse(SuccessResponse):
    """Response model to /get_all on /cfg prefix"""
    configuracoes: Dict[str, Union[NotificationsBase, TargetPriceBase]]
