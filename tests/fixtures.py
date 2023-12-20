import json
import pytest
import httpx
import asyncio

from fastapi.testclient import TestClient
from starlette import status

from shopping_cart.common.app import create_app
from shopping_cart import models


# Use the httpx_mock pytest fixture to mock HTTP calls to the reservation API.
# Since the fixture mocks all calls by default, we must explicitly tell it
# to disable mocking for any calls to the shopping cart API.
@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]


# Disables assertions run by the httpx_mock pytest fixture during test teardown.
@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    return False


# Tells the httpx_mock pytest fixture which Python async framework to use.
@pytest.fixture
def anyio_backend():
    return "asyncio"


# Creates an instance of our shopping cart API
@pytest.fixture
def app():
    models.Base.metadata.create_all(bind=models.engine)
    yield create_app()
    models.Base.metadata.drop_all(bind=models.engine)


# Creates an instance of a test client for our shopping cart API.
# This test client also mocks the reservation API call by returning a reservation ID without delay.
# It is used by the majority of test cases.
@pytest.fixture
def client(app, httpx_mock):
    def do_fast_reservation(request: httpx.Request):
        json_resp = json.loads(request.content)
        return httpx.Response(
            status_code=status.HTTP_200_OK,
            json={"reservation_id": 1000 + json_resp["id"]},
        )

    httpx_mock.add_callback(do_fast_reservation, url="https://dev.reservation-service")
    yield TestClient(app)


# Creates an instance of a test client for our shopping cart API.
# This test client also mocks the reservation API call by returning a reservation ID with a simulated delay.
# It is used to test cases where the reservation takes a very long time.
@pytest.fixture
async def client_slow_reservation(app, httpx_mock):
    async def do_slow_reservation(request: httpx.Request):
        # Reservations could take 30 sec or more.
        # Simulate the delay here. To speed up the tests, we will sleep 3 sec instead of 30.
        await asyncio.sleep(3)
        json_resp = json.loads(request.content)
        return httpx.Response(
            status_code=status.HTTP_200_OK,
            json={"reservation_id": 1000 + json_resp["id"]},
        )

    httpx_mock.add_callback(do_slow_reservation, url="https://dev.reservation-service")
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
