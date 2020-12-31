from pydantic import BaseModel, Field
from typing import Dict, Union, List

from api.models import SuccessResponse


class SendResponse(SuccessResponse):
    """Response model to /send prefix"""
    enviado: bool = Field(..., description="Se a mensagem foi enviada pelo Telegram ou não.")


class Notifications(BaseModel):
    """Base model for /set_notifications on /cfg prefix"""
    current_price: bool = Field(..., description="Notificação de preço atual.")
    gt_target_price: bool = Field(..., description="Notificação de preço atual maior que target.")
    lt_target_price: bool = Field(..., description="Notificação de preço atual menor que target.")


class NotificationsResponse(SuccessResponse):
    """Response model to /set_notifications on /cfg prefix"""
    notificacoes: Notifications


class TargetPrice(BaseModel):
    greater_than: float = Field(...)
    lesser_than: float = Field(...)


class ConfigurationsResponse(SuccessResponse):
    """Response model to /get_all on /cfg prefix"""
    configuracoes: Dict[str, Union[Notifications, TargetPrice]]

    class Config:
        schema_extra = {
            "example": {
                "configuracoes": {
                    "notificacoes": Notifications(current_price=True,
                                  gt_target_price=True,
                                  lt_target_price=True).dict(),
                    "target_prices": 
                        TargetPrice(greater_than=12,
                                    lesser_than=10).dict(),
                }
            }
        }