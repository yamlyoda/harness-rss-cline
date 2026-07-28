from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from monitor.app import app, service


@pytest.fixture(autouse=True)
def mock_service(mocker):
    """Mock MonitorService to avoid real NATS/HTTP connections."""
    service.broker.connect = AsyncMock()
    service.broker.close = AsyncMock()
    service.poll_all = AsyncMock(return_value=5)


class TestMonitorApp:
    async def test_health_endpoint(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    async def test_refresh_endpoint(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/refresh")
            assert response.status_code == 200
            assert response.json() == {"new_items": 5}

    async def test_refresh_zero_items(self, mocker):
        service.poll_all = AsyncMock(return_value=0)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/refresh")
            assert response.status_code == 200
            assert response.json() == {"new_items": 0}

    async def test_health_method_not_allowed(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/health")
            assert response.status_code == 405

    async def test_refresh_method_not_allowed(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/refresh")
            assert response.status_code == 405
