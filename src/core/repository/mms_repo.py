from fastapi import Depends
from src.core.database import get_db
from sqlalchemy.orm import Session
from src.core.models.mms import MMsModel


class MMsRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def list_filter(self, pair: str, _from: int, _to: int):
        query = (
            self.db.query(MMsModel.timestamp, MMsModel.mms_20)
            .filter(MMsModel.pair == pair)
            .filter(_from <= MMsModel.timestamp, _to >= MMsModel.timestamp)
        )

        return query.all()

    def bulk_add(self, mms_list: list[MMsModel]):
        self.db.bulk_save_objects(mms_list)
        self.db.commit()
