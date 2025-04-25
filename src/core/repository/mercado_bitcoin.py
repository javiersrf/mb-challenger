from src.core.settings import settings
from src.core.schemas import MBDataValue
import requests

class MBRepo:

    def get_all(self, symbol: str, _from: int, _to: int)->list[MBDataValue]:
        
        if symbol not in {'BTC-BRL', 'ETH-BRL'}:
            raise ValueError(f"Invalid symbol: {symbol}. Valid symbols are: BTC-BRL, ETH-BRL")
    
        response = requests.get(
            url=f"{settings.MB_URL}/candles?symbol={symbol}&from={_from}&to={_to}&resolution=1d",
        )
        if response.status_code != 200:
            raise ValueError(f"Error fetching data from Mercado Bitcoin: {response.text}")

        data = response.json()
        if not data:
            raise ValueError("No data found for the given parameters.")
        result: list[MBDataValue] = []
        for idx, item in enumerate(data["t"]):
            result.append(
                MBDataValue(
                    time=item,
                    close=float(data["c"][idx]),
                )
            )



        return result
