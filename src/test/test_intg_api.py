import pytest
from async_asgi_testclient import TestClient
from unittest.mock import patch

def test_activities_fixture(activities_fixture):
    assert activities_fixture[0]["desc"] == "test_activity_0"

@pytest.mark.asyncio
async def test_fixture_list_job_activity(mock_db):
    job_activity_list = await mock_db["job_activity"].find().to_list(1000)
    assert "_id" in job_activity_list[0]
    assert "desc" in job_activity_list[0]
    assert "test_activity_0" == job_activity_list[0]["desc"]

@pytest.mark.asyncio
async def test_get_job_activities(mock_db):
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            resp = await test_client.get("/job_activity/")

    assert resp.status_code == 200
    assert 0 < len(resp.json())


@pytest.mark.asyncio
async def test_get_job_activity(mock_db):
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            resp_activities = await test_client.get("/job_activity/")
        assert resp_activities.status_code == 200

        resp_activities_json = resp_activities.json()
        assert 0 < len(resp_activities_json)

        resp_id = resp_activities_json[0]["_id"]
    
    assert isinstance(resp_id, str)

    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            resp_single = await test_client.get(f"/job_activity/{resp_id}")
        assert resp_single.status_code == 200

        resp_json = resp_single.json()
    
    assert "_id" in resp_json
    assert resp_json.get("_id") == resp_id

@pytest.mark.asyncio
async def test_delete_job_activity(mock_db):
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            resp_activities = await test_client.get("/job_activity/")
            assert resp_activities.status_code == 200
            resp_activities_json = resp_activities.json()
            assert 0 < len(resp_activities_json)

            resp_id = resp_activities_json[0]["_id"]

            resp_delete = await test_client.delete(f"/job_activity/{resp_id}")
            assert resp_delete.status_code == 200
