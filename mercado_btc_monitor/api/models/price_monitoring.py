from pydantic import Field

from api.models import SuccessResponse


# Validação de campos e construção do Schema no Swagger
# ... Significa obrigatório (required)
class SendPriceResponse(SuccessResponse):
    """Response model to /send_price"""
    resultado: dict
