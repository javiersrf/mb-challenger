from datetime import datetime, timedelta
from src.core.exceptions import BadRequestException
from src.core.repository.mms_repo import MMsRepo
from fastapi import Depends
from pydantic import BaseModel


class MMSResponse(BaseModel):
    timestamp: int
    mms: float


class MMSService:
    def __init__(self, mms_repo: MMsRepo = Depends(MMsRepo)):
        self.mms_repo = mms_repo

    def get_mms(self, pair: str, _from: int, _to: int | None, _range: int):
        if not _to:
            _to = (datetime.now() - timedelta(days=1)).timestamp()

        self._validate_dates(_from=_from, _to=_to)

        results = self.mms_repo.list_filter(
            pair=pair, _from=_from, _to=_to, _range=_range
        )

        def get_value(item):
            match _range:
                case 200:
                    return item.mms_200
                case 50:
                    return item.mms_50
                case _:
                    return item.mms_20
            return 0

        return [
            MMSResponse(timestamp=item.timestamp, mms=get_value(item))
            for item in results
        ]

    def _validate_dates(self, _from: int, _to: int):
        if _to < _from:
            raise BadRequestException(
                detail="Invalid date range. 'from' date must be before 'to' date."
            )
        if datetime.fromtimestamp(float(_from)) < datetime.now() - timedelta(days=365):
            raise BadRequestException(
                detail="Invalid 'from' date. It must not be more than 365 days in the past."
            )

    def _validete_pair(self, pair: str):
        if pair not in {"BRLBTC", "BRLETH"}:
            raise BadRequestException(
                detail=f"Invalid pair: {pair}. Valid pairs are: BRLBTC, BRLETH"
            )
