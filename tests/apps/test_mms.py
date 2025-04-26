from freezegun import freeze_time


@freeze_time("2025-01-14")
def test_get_from_more_than_365(client, mock_request):
    response = client.get("/BRLETH/mms?from=1577836800")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
