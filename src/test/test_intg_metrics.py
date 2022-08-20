import pytest
from async_asgi_testclient import TestClient
from unittest.mock import patch


@pytest.mark.asyncio
async def test_metrics_route(mock_db):
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            await test_client.get("/job_activity/")
            metrics_resp = await test_client.get("/metrics/")
            assert metrics_resp.status_code == 200
            assert metrics_resp.headers.get("content-type") == "text"
