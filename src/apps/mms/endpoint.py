from fastapi import APIRouter, Depends, Query
from .services import MMSService
from datetime import datetime
router = APIRouter(
    prefix="/",
    tags=["mms"],
)


@router.get("/{pair}/mms")
async def get_mms(
    pair: str,
    _from: datetime = Query(..., alias="from"),
    _to: datetime = Query(None, alias="to"),
    mms_service: MMSService = Depends(),
):
    result = mms_service.get_mms(pair) 
    return result