from fastapi import FastAPI

from .settings import get_settings
from ..routers import create_items_router


def create_app(settings=get_settings()):
    app = FastAPI(
        title="Shopping Cart API",
        description="This is a shopping cart API that reserves items once they are put into a cart.",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
    )
    router_list = [create_items_router()]
    for router in router_list:
        app.include_router(router)
    return app
