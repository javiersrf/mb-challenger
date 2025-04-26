from src.core.utils import calculate_mms, PairMMS
from datetime import datetime


def test_calculate_mms():
    input_data = [
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-01").timestamp()),
                "value": 5.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-02").timestamp()),
                "value": 5.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-03").timestamp()),
                "value": 5.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-04").timestamp()),
                "value": 6.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-05").timestamp()),
                "value": 7.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-06").timestamp()),
                "value": 8.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-07").timestamp()),
                "value": 10.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-08").timestamp()),
                "value": 20.00,
            }
        ),
        PairMMS(
            **{
                "timestamp": int(datetime.fromisoformat("2020-11-09").timestamp()),
                "value": 21.00,
            }
        ),
    ]
    output = calculate_mms(values=input_data, n=3)
    assert output[-1].model_dump() == {"value": 17.0, "timestamp": 1604890800}
