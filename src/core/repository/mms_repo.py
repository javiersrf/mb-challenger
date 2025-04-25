from fastapi import Depends
from src.core.database import get_db
class MMsRepo:
    def __init__(self, db = Depends(get_db)):
        self.db = db
