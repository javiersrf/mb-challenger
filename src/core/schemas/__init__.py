from pydantic import BaseModel


class MBDataValue(BaseModel):
    close: float
    time: int
