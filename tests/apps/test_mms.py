from freezegun import freeze_time
from datetime import datetime
from tests.factory.mms import MMsModelFactory


@freeze_time("2025-01-14")
def test_get_from_more_than_365(client, mock_request):
    date_365 = datetime.fromisoformat("2023-01-14").timestamp()
    response = client.get(f"/BRLETH/mms?from={date_365}")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid 'from' date. It must not be more than 365 days in the past."
    }


def test_get_start_bigger_than_end(client, mock_request):
    _to = datetime.fromisoformat("2025-01-14").timestamp()
    _from = datetime.fromisoformat("2025-02-14").timestamp()
    response = client.get(f"/BRLETH/mms?from={_from}&to={_to}")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid date range. 'from' date must be before 'to' date."
    }


@freeze_time("2025-01-15")
def test_get_with_success(client, mock_request):
    mock_data = [
        MMsModelFactory(pair="BRLETH", timestamp=1736812800),
        MMsModelFactory(pair="BRLETH", timestamp=1736726400),
        MMsModelFactory(pair="BRLETH", timestamp=1736640000),
        MMsModelFactory(pair="BRLETH", timestamp=1736553600),
    ]
    date_365 = datetime.fromisoformat("2025-01-10").timestamp()
    response = client.get(f"/BRLETH/mms?from={date_365}")
    assert response.status_code == 200
    assert response.json() == [
        {"timestamp": item.timestamp, "mms": item.mms_20} for item in mock_data
    ]


@freeze_time("2025-01-15")
def test_get_with_success_filtering_pair(client, mock_request):
    mock_data = [
        MMsModelFactory(pair="BRLETH", timestamp=1736812800),
        MMsModelFactory(pair="BRLETH", timestamp=1736726400),
        MMsModelFactory(pair="BRLETH", timestamp=1736640000),
        MMsModelFactory(pair="BRLBTC", timestamp=1736553600),
    ]
    date_365 = datetime.fromisoformat("2025-01-10").timestamp()
    response = client.get(f"/BRLETH/mms?from={date_365}")
    assert response.status_code == 200
    assert response.json() == [
        {"timestamp": item.timestamp, "mms": item.mms_20} for item in mock_data[:3]
    ]
