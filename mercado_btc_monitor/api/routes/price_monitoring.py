from fastapi import APIRouter, Query
from loguru import logger

from api.models.price_monitoring import SendPriceResponse, TargetPriceResponse
from api.modules import price_monitoring
from api.settings import envs

router = APIRouter()

@router.get('/send_current_price', response_model=SendPriceResponse, summary="Retorna o dobro do valor de entrada.")
def router_current(parse_mode: str = Query(None)) -> float:
    logger.log('LOG ROTA', "Chamada rota /send_price")
    return {"enviado": price_monitoring.send_current_price(parse_mode)}

@router.get('/send_if_gt_target_price', response_model=TargetPriceResponse, summary="Retorna o dobro do valor de entrada.")
def router_target(target_price: float = Query(..., gt=0),
                  parse_mode: str = Query(None)) -> float:
    logger.log('LOG ROTA', "Chamada rota /send_if_target_price")
    return {"resultado": price_monitoring.send_if_gt_target_price(target_price=target_price, parse_mode=parse_mode)}
