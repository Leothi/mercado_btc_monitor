from pydantic import Field

from api.models import SuccessResponse


class MonitoringResponse(SuccessResponse):
    """Response model to /monitoring prefix"""
    enviado: bool
    

