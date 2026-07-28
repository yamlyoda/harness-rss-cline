from __future__ import annotations

import asyncio
from typing import Any

import pytest
from faststream.nats import NatsBroker


@pytest.mark.integration
class TestNatsPubSub:
    async def test_publish_and_subscribe(self, nats_broker: NatsBroker):
        received: list[dict[str, Any]] = []

        async def handler(msg):
            received.append(msg)

        await nats_broker.subscribe("test.subject", handler)
        await nats_broker.start()

        await nats_broker.publish(
            {"key": "value", "number": 42},
            subject="test.subject",
        )

        await asyncio.sleep(0.5)

        assert len(received) == 1
        assert received[0]["key"] == "value"
        assert received[0]["number"] == 42

    async def test_multiple_messages(self, nats_broker: NatsBroker):
        received: list[dict[str, Any]] = []

        async def handler(msg):
            received.append(msg)

        await nats_broker.subscribe("test.batch", handler)
        await nats_broker.start()

        for i in range(5):
            await nats_broker.publish(
                {"index": i},
                subject="test.batch",
            )

        await asyncio.sleep(0.5)

        assert len(received) == 5
        assert [m["index"] for m in received] == [0, 1, 2, 3, 4]

    async def test_different_subjects(self, nats_broker: NatsBroker):
        received_a: list[dict[str, Any]] = []
        received_b: list[dict[str, Any]] = []

        async def handler_a(msg):
            received_a.append(msg)

        async def handler_b(msg):
            received_b.append(msg)

        await nats_broker.subscribe("subject.a", handler_a)
        await nats_broker.subscribe("subject.b", handler_b)
        await nats_broker.start()

        await nats_broker.publish({"data": "A"}, subject="subject.a")
        await nats_broker.publish({"data": "B"}, subject="subject.b")

        await asyncio.sleep(0.5)

        assert len(received_a) == 1
        assert len(received_b) == 1
        assert received_a[0]["data"] == "A"
        assert received_b[0]["data"] == "B"
