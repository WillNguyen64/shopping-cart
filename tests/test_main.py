import pytest

from starlette import status

from .fixtures import (
    non_mocked_hosts,
    assert_all_responses_were_requested,
    anyio_backend,
    app,
    client,
    client_slow_reservation,
)


def test_get_empty_cart(client):
    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"items": []}


def test_add_one_item_to_cart(client):
    response = client.post("/items", json={"name": "item1", "quantity": 5})
    assert response.status_code == status.HTTP_202_ACCEPTED

    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    item = response.json()["items"][0]
    assert item == {
        "id": 1,
        "name": "item1",
        "quantity": 5,
        "reservation_id": 1001,
    }


def test_add_many_items_to_cart(client):
    items = [
        {"name": "item1", "quantity": 5},
        {"name": "item2", "quantity": 10},
        {"name": "item2", "quantity": 15},
    ]

    for item in items:
        response = client.post("/items", json=item)
        assert response.status_code == status.HTTP_202_ACCEPTED

    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    expected_id = 1
    for item in response.json()["items"]:
        assert item == {
            "id": expected_id,
            "name": item["name"],
            "quantity": item["quantity"],
            "reservation_id": 1000 + expected_id,
        }
        expected_id += 1


def test_add_item_missing_name(client):
    response = client.post("/items", json={"quantity": 1})
    _assert_unprocessable_entity(response, "Field required")


def test_add_item_empty_name(client):
    response = client.post("/items", json={"name": "", "quantity": 1})
    _assert_unprocessable_entity(response, "Name must not be empty")


def test_add_item_empty_quantity(client):
    response = client.post("/items", json={"name": "item1", "quantity": ""})
    _assert_unprocessable_entity(response, "Input should be a valid integer")


def test_add_item_missing_quantity(client):
    response = client.post("/items", json={"name": "item1"})
    assert response.status_code == status.HTTP_202_ACCEPTED

    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    item = response.json()["items"][0]
    assert item == {
        "id": 1,
        "name": "item1",
        "quantity": 1,
        "reservation_id": 1001,
    }


@pytest.mark.anyio
async def test_add_item_with_slow_reservation(client_slow_reservation):
    # FIXME: When using the httpx test client, I noticed that the
    # POST request blocks until the reservation task finishes which is several seconds.
    # The expected behaviour is for the POST to return immediately and then run the reservation
    # task in the background.
    # I am not sure if this is a Starlette bug, but others have reported a similar issue:
    # https://github.com/encode/starlette/issues/533
    # https://github.com/encode/starlette/issues/578
    client = client_slow_reservation
    response = await client.post("/items", json={"name": "item1", "quantity": 5})

    assert response.status_code == status.HTTP_202_ACCEPTED
    response = await client.get("/items")
    item = response.json()["items"][0]
    assert item["reservation_id"] == 1000 + item["id"]


def _assert_unprocessable_entity(response, exp_error_msg):
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    actual_error_msg = response.json()["detail"][0]["msg"]
    print(actual_error_msg)
    assert exp_error_msg in actual_error_msg
