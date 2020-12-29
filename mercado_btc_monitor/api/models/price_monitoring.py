from pydantic import Field

from api.models import SuccessResponse


class SendPriceResponse(SuccessResponse):
    """Response model to /send_price"""
    enviado: bool
    
class TargetPriceResponse(SuccessResponse):
    """Response model to /send_price"""
    resultado: str
