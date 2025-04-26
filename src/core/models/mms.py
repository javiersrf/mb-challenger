from sqlmodel import Field
from sqlmodel import SQLModel


class MMsModel(SQLModel, table=True):
    __tablename__ = "mms"
    id: int = Field(default=None, primary_key=True)

    pair: str = Field(index=True)
    timestamp: int = Field(index=True)
    mms_20: float = Field(nullable=True)
    mms_50: float = Field(nullable=True)
    mms_200: float = Field(nullable=True)
