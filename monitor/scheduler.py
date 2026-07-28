from __future__ import annotations

import asyncio
import logging

from monitor.settings import settings

logger = logging.getLogger(__name__)


class PollScheduler:
    def __init__(self, poll_coro) -> None:
        self._poll_coro = poll_coro
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        interval = settings.monitor_interval_minutes * 60

        async def loop():
            while True:
                await asyncio.sleep(interval)
                try:
                    count = await self._poll_coro()
                    if count:
                        logger.info("Scheduled poll: %d new items", count)
                except Exception:
                    logger.exception("Scheduled poll failed")

        self._task = asyncio.create_task(loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
