import pytest
from async_asgi_testclient import TestClient
from unittest.mock import patch


@pytest.mark.asyncio
async def test_metrics_route__status_content_type(mock_db):
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            await test_client.get("/job_activity/")
            metrics_resp = await test_client.get("/metrics/")
            assert metrics_resp.status_code == 200

            # ,/metrics/ route should be plain text
            assert "text/plain" in metrics_resp.headers.get("content-type")

        assert any([
            line
            for line in metrics_resp.text.split("\n")
            if "ui_mongo_entry_transactions" in line
            ])

@pytest.mark.asyncio
async def test_metrics_route__test_app(metrics_test_app):
    async with TestClient(metrics_test_app) as test_client:
        await test_client.get("/foo/")
        metrics_resp = await test_client.get("/metrics/")
        assert metrics_resp.status_code == 200
        assert "text/plain" in metrics_resp.headers.get("content-type")

        # make sure ui_mongo metrics in response
        entry_transaction_lines = [
                                    line
                                    for line in metrics_resp.text.split("\n")
                                    if "ui_mongo_entry_transactions" in line
                                    ]
        assert any(entry_transaction_lines)
        assert any([
            line
            for line in entry_transaction_lines
            if "get_foo" in line])
