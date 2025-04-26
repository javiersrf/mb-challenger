from sqlmodel import Field
from datetime import datetime
from sqlmodel import SQLModel


class MMsModel(SQLModel, table=True):
    __tablename__ = "mms"
    id: int = Field(default=None, primary_key=True)

    pair: str = Field(index=True)
    timestamp: datetime = Field(index=True)
    mms_20: float = Field(nullable=False)
    mms_50: float = Field(nullable=False)
    mms_200: float = Field(nullable=False)
