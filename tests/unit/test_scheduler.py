from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

from monitor.scheduler import PollScheduler


class TestPollScheduler:
    async def test_start_calls_poll_coro(self):
        with patch("monitor.scheduler.settings.monitor_interval_minutes", 0.001):
            poll_coro = AsyncMock(return_value=3)
            scheduler = PollScheduler(poll_coro)

            await scheduler.start()
            await asyncio.sleep(0.15)
            await scheduler.stop()

            poll_coro.assert_awaited()

    async def test_stop_cancels_task(self):
        with patch("monitor.scheduler.settings.monitor_interval_minutes", 10):
            poll_coro = AsyncMock(return_value=0)
            scheduler = PollScheduler(poll_coro)

            await scheduler.start()
            assert scheduler._task is not None
            assert not scheduler._task.done()

            await scheduler.stop()
            assert scheduler._task.done()

    async def test_start_stop_multiple(self):
        with patch("monitor.scheduler.settings.monitor_interval_minutes", 0.001):
            poll_coro = AsyncMock(return_value=1)
            scheduler = PollScheduler(poll_coro)

            await scheduler.start()
            await asyncio.sleep(0.1)
            await scheduler.stop()

            assert poll_coro.await_count >= 1

    async def test_stop_without_start(self):
        poll_coro = AsyncMock()
        scheduler = PollScheduler(poll_coro)

        # Should not raise
        await scheduler.stop()
