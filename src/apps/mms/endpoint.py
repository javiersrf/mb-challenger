from fastapi import APIRouter, Depends, Query
from .services import MMSService
from src.core.utils import PairEnum, RangeEnum

router = APIRouter(
    tags=["mms"],
)


@router.get("/{pair}/mms")
async def get_mms(
    pair: PairEnum,
    _from: float = Query(..., alias="from", description="Timestamp in seconds"),
    _to: float = Query(None, alias="to", description="Timestamp in seconds"),
    _range: RangeEnum = Query(RangeEnum.TWENTY, alias="range"),
    mms_service: MMSService = Depends(),
):
    result = mms_service.get_mms(
        pair=pair.value, _from=_from, _to=_to, _range=_range.value
    )
    return result
