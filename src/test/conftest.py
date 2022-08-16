import asyncio

from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from typing import List, Dict, Any
import pytest


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


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
