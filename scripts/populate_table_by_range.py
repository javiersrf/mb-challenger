import argparse
from src.core.repository.mercado_bitcoin import MBRepo
from src.core.repository.mms_repo import get_db, MMsModel, MMsRepo
from datetime import datetime
from src.core.utils import calculate_mms, PairMMS


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate and store MMS values for crypto pairs"
    )
    parser.add_argument(
        "--from",
        dest="from_timestamp",
        type=int,
        required=True,
        help="Start timestamp (in seconds)",
    )
    parser.add_argument(
        "--to",
        dest="to_timestamp",
        type=int,
        required=True,
        help="End timestamp (in seconds)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    mb_repo = MBRepo()
    _from = args.from_timestamp
    _to = args.to_timestamp

    for pair in {"BTC-BRL", "ETH-BRL"}:
        print(
            f"Processing pair: {pair} from {datetime.fromtimestamp(_from)} to {datetime.fromtimestamp(_to)}"
        )

        resp = mb_repo.get(symbol=pair, _from=_from, _to=_to)
        input_values = [PairMMS(value=item.close, timestamp=item.time) for item in resp]

        sma_20 = calculate_mms(input_values, 20)
        sma_50 = calculate_mms(input_values, 50)
        sma_200 = calculate_mms(input_values, 200)

        mms_data: dict[int, dict] = {}

        for item in sma_20:
            mms_data[item.timestamp] = {
                "pair": pair,
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
            if "mms_20" in values and "mms_50" in values and "mms_200" in values:
                mms_models.append(
                    MMsModel(
                        pair=values["pair"],
                        timestamp=datetime.fromtimestamp(timestamp),
                        mms_20=values["mms_20"],
                        mms_50=values["mms_50"],
                        mms_200=values["mms_200"],
                    )
                )

        with get_db() as session:
            repo = MMsRepo(db=session)
            repo.bulk_add(mms_list=mms_models)

        print(f"Added {len(mms_models)} records for {pair} to the database")
