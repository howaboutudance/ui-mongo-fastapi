import asyncio

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from typing import List, Dict, Any
import pytest

from ui_mongo.metrics import EntryTransactionType, transaction_metric


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def metrics_test_app() -> FastAPI:
    from starlette_prometheus import metrics, PrometheusMiddleware
    from starlette.responses import JSONResponse
    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)

    @transaction_metric(transaction_type=EntryTransactionType.get)
    @app.get("/foo/")
    async def get_foo() -> JSONResponse:
        return JSONResponse({"type": "foo"})

    return app


@pytest.fixture
def activities_fixture() -> List[Dict[str, Any]]:
    from ui_mongo.repositories.job_activity import JobActivity
    from ui_mongo.repositories.job_activity import JobActivityType
    return [
            jsonable_encoder(JobActivity(
                type=JobActivityType.employer_contact,
                desc=desc_item))
            for desc_item in
            [f"test_activity_{i}" for i in range(5)]
    ]


@pytest.fixture
async def mock_db(activities_fixture):
    from ui_mongo import config
    client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(config.settings.mongodb_url)
    coll: motor.motor_asyncio.AsyncIOMotorCollection = client.college

    await coll.job_activity.insert_many(activities_fixture)
    yield coll

    await coll.drop_collection("job_activity.py")
