import datetime
from src.core.exceptions import BadRequestException
class MMSService:
    def __init__(self, db):
        self.db = db

    def get_mms(self, pair: str, _from: datetime, _to: datetime):
        return self.db.get_all_mms()
    

    def _validete_pair(self, pair: str):
        if pair not in {'BRLBTC', 'BRLETH'}:
            raise BadRequestException(
                detail=f"Invalid pair: {pair}. Valid pairs are: BRLBTC, BRLETH"
            )
