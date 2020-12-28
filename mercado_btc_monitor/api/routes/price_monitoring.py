from fastapi import APIRouter, Query
from loguru import logger

from api.models.price_monitoring import SendPriceResponse
from api.modules import price_monitoring

router = APIRouter()

@router.get('/send_price', response_model=SendPriceResponse, summary="Retorna o dobro do valor de entrada.")
def router_dobro(parse_mode: str = Query(None)) -> float:
    logger.log('LOG ROTA', "Chamada rota /send_price")
    return {"resultado": price_monitoring.send_current_prince(parse_mode)}
