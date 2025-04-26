from pydantic import BaseModel
import enum


class RangeEnum(int, enum.Enum):
    TWENTY = 20
    FIFTY = 50
    TWO_HUNDRED = 200


class PairEnum(str, enum.Enum):
    BRLBTC = "BRLBTC"
    BRLETH = "BRLETH"


class PairMMS(BaseModel):
    value: float
    timestamp: int


def calculate_mms(values: list[PairMMS], n: int) -> list[PairMMS]:
    means = []
    for i in range(len(values) - n + 1):
        range_values = values[i : i + n]
        mean_value = sum([item.value for item in range_values]) / n
        mean_timestamp = range_values[-1].timestamp
        means.append(PairMMS(value=mean_value, timestamp=mean_timestamp))

    return means
