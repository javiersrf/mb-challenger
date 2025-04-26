from datetime import datetime, timedelta
from src.core.repository.mercado_bitcoin import MBRepo
from src.core.repository.mms_repo import get_db, MMsModel, MMsRepo
from src.core.utils import calculate_mms, PairMMS


def get_date_range():
    """Get date range from today-200 days to today"""
    today = datetime.today()
    start_date = today - timedelta(days=200)

    start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())

    end_timestamp = int(datetime.combine(today, datetime.max.time()).timestamp())

    return start_timestamp, end_timestamp, today.date()


if __name__ == "__main__":
    _from, _to, today_date = get_date_range()

    print(
        f"Calculating MMS using data from {datetime.fromtimestamp(_from)} to {datetime.fromtimestamp(_to)}"
    )
    print(f"Will store only today's final values ({today_date})")

    mb_repo = MBRepo()

    for pair in {"BTC-BRL", "ETH-BRL"}:
        print(f"\nProcessing pair: {pair}")

        resp = mb_repo.get(symbol=pair, _from=_from, _to=_to)

        if not resp:
            print(f"No data available for {pair} in this period")
            continue

        input_values = [PairMMS(value=item.close, timestamp=item.time) for item in resp]

        sma_20 = calculate_mms(input_values, 20)
        sma_50 = calculate_mms(input_values, 50)
        sma_200 = calculate_mms(input_values, 200)

        today_values = {"mms_20": None, "mms_50": None, "mms_200": None}

        if sma_20:
            today_values["mms_20"] = sma_20[-1].value
        if sma_50:
            today_values["mms_50"] = sma_50[-1].value
        if sma_200:
            today_values["mms_200"] = sma_200[-1].value

        # Only create a record if we have all three values
        if all(today_values.values()):
            mms_model = MMsModel(
                pair=pair,
                timestamp=datetime.combine(today_date, datetime.min.time()),
                mms_20=today_values["mms_20"],
                mms_50=today_values["mms_50"],
                mms_200=today_values["mms_200"],
            )

            with get_db() as session:
                repo = MMsRepo(db=session)
                repo.bulk_add([mms_model])
            print(f"Added today's MMS values for {pair}:")
            print(f"200-day: {today_values['mms_200']:.2f}")
            print(f"50-day: {today_values['mms_50']:.2f}")
            print(f"20-day: {today_values['mms_20']:.2f}")
        else:
            print(f"Couldn't calculate all MMS values for {pair} today")
            print(f"Missing: {[k for k, v in today_values.items() if v is None]}")

    print("\nToday's MMS calculation complete")
