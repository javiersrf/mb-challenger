from src.core.repository.mercado_bitcoin import MBRepo
from src.core.repository.mms_repo import get_db, MMsModel, MMsRepo
from datetime import datetime, timedelta
from src.core.utils import calculate_mms, PairMMS
from src.core.utils import PairEnum


def parsed_pair(value: str):
    base, quote = value.split("-")
    return PairEnum(f"{quote}{base}")


if __name__ == "__main__":
    mb_repo = MBRepo()
    _now = datetime.now()
    _to = int(_now.timestamp())
    _from = _now - timedelta(days=365)

    for pair in {"BTC-BRL", "ETH-BRL"}:
        resp = mb_repo.get(symbol=pair, _from=int(_from.timestamp()), _to=_to)
        input_values = [PairMMS(value=item.close, timestamp=item.time) for item in resp]

        sma_20 = calculate_mms(input_values, 20)
        sma_50 = calculate_mms(input_values, 50)
        sma_200 = calculate_mms(input_values, 200)

        mms_data: dict[int, dict] = {}

        for item in sma_20:
            mms_data[item.timestamp] = {
                "pair": parsed_pair(pair),
                "timestamp": item.timestamp,
                "mms_20": item.value,
            }

        for item in sma_50:
            if item.timestamp in mms_data:
                mms_data[item.timestamp]["mms_50"] = item.value

        for item in sma_200:
            if item.timestamp in mms_data:
                mms_data[item.timestamp]["mms_200"] = item.value

        mms_models = []
        for timestamp, values in mms_data.items():
            mms_models.append(
                MMsModel(
                    pair=values["pair"],
                    timestamp=timestamp,
                    mms_20=values.get("mms_20"),
                    mms_50=values.get("mms_50"),
                    mms_200=values.get("mms_200"),
                )
            )

        repo = MMsRepo(db=next(get_db()))
        repo.bulk_add(mms_list=mms_models)

        print(f"Added {len(mms_models)} records to the database")
