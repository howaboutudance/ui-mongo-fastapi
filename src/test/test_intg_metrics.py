import pytest
from async_asgi_testclient import TestClient
from unittest.mock import patch


@pytest.mark.asyncio
async def test_metrics_route__status_content_type(mock_db):
    """
    Integration test that /metrics/ works and has correct content-type
    """
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            await test_client.get("/job_activity/")
            metrics_resp = await test_client.get("/metrics/")
            assert metrics_resp.status_code == 200

            # ,/metrics/ route should be plain text
            assert "text/plain" in metrics_resp.headers.get("content-type")


@pytest.mark.asyncio
async def test_entry_transaction_metric__format(metrics_test_app):
    """
    Test entry_transactions is correctly formatted in test app
    """
    async with TestClient(metrics_test_app) as test_client:
        await test_client.get("/foo/")
        metrics_resp = await test_client.get("/metrics/")
        assert metrics_resp.status_code == 200
        assert "text/plain" in metrics_resp.headers.get("content-type")

        # At least two lines per meteric defined
        assert 4 <= len(
                        entry_transaction_lines := [
                            line
                            for line in metrics_resp.text.split("\n")
                            if "ui_mongo_entry_transactions" in line
                        ]
        )
        assert 0 == (len(entry_transaction_lines) % 2)

        assert 4 == len([
            line
            for line in entry_transaction_lines
            if (
                line.startswith("# HELP") or
                line.startswith("# TYPE")
            )
            ])

        # Format checks of lines that match
        #
        # There is exactly one line:
        # - starts with ui_mongo_transaction_total (the desc)
        # - with the label function_name = "get_foo"
        # - with the label method = "GET"
        # - end with 1.0 (the value)
        assert len([
            line
            for line in entry_transaction_lines
            if (
                line.startswith("ui_mongo_entry_transactions_total") and
                'function_name="get_foo"' in line and
                'method="GET"' in line and
                line.endswith("1.0")
                )]
            ) == 1

        # There is exactly one line:
        # - starts with ui_mongo_transaction_created (the desc)
        # - with the label function_name = "get_foo"
        # - with the label method = "GET"
        assert len([
            line
            for line in entry_transaction_lines
            if (
                'function_name="get_foo"' in line and
                'method="GET"' in line and
                line.startswith("ui_mongo_entry_transactions_created")
                )]
            ) == 1


@pytest.mark.asyncio
async def test_entry_transaction_metric__job_activity_use(mock_db):
    """
    Integration test that /metrics/ works against with call /job_activity/ route
    first
    """
    from ui_mongo import api
    async with TestClient(api.app) as test_client:
        with patch("ui_mongo.globals.db", new=mock_db):
            await test_client.get("/job_activity/")
            metrics_resp = await test_client.get("/metrics/")
            assert metrics_resp.status_code == 200

            # ,/metrics/ route should be plain text
            assert "text/plain" in metrics_resp.headers.get("content-type")

        # Make sure at least three (two for the defintion) line has
        # ui_mongo_entry_transactions in them
        assert 4 <= len(
                        entry_transaction_lines := [
                            line
                            for line in metrics_resp.text.split("\n")
                            if "ui_mongo_entry_transactions" in line
                            ]
                        )

        # Make sure at least 1 line has both the labels respective to the
        # GET call againt /job_activity/ made earlier
        assert 0 < len([
            ('function_name="get_activities"' in line and 'method="GET"' in line)
            for line in entry_transaction_lines
            ])
