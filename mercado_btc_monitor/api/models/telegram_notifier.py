from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Union, TypeVar

from api.models import SuccessResponse


FloatOrNone = TypeVar('IntOrNone', float, None)


class SendResponse(SuccessResponse):
    """Response model to /send prefix"""
    enviado: bool = Field(...,
                          description="Se a mensagem foi enviada pelo Telegram ou não.")


class Notifications(BaseModel):
    """Base model for /set_notifications on /cfg prefix"""
    notify_current_price: bool = Field(...,
                                       description="Notificação de preço atual.")
    notify_if_gt_target_price: bool = Field(
        ..., description="Notificação de preço atual maior que target.")
    notify_if_lt_target_price: bool = Field(
        ..., description="Notificação de preço atual menor que target.")


class NotificationsResponse(SuccessResponse):
    """Response model to /set_notifications on /cfg prefix"""
    notificacoes: Notifications


class TargetPrice(BaseModel):
    """Base model for /set_target_price on /cfg prefix"""
    gt_target_price: FloatOrNone = Field(...,
                                         description="Preço alvo para greater_than target")
    lt_target_price: FloatOrNone = Field(...,
                                         description="Preço alvo para lesser_than target")


class Comparation(str, Enum):
    """Enum model for /set_target_price on /cfg prefix"""
    greater_than = 'greater_than'
    lesser_than = 'lesser_than'


class SetTargetPriceResponse(SuccessResponse):
    """Response model to /set_target_price on /cfg prefix"""
    target_prices: TargetPrice


class ConfigurationsResponse(SuccessResponse):
    """Response model to /get_all on /cfg prefix"""
    configuracoes: Dict[str, Union[Notifications, TargetPrice]]

    class Config:
        schema_extra = {
            "example": {
                "configuracoes": {
                    "notificacoes": Notifications(notify_current_price=True,
                                                  notify_if_gt_target_price=True,
                                                  notify_if_lt_target_price=True).dict(),
                    "target_prices":
                        TargetPrice(gt_target_price=12,
                                    lt_target_price=10).dict(),
                }
            }
        }
