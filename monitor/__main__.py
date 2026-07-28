from __future__ import annotations

import asyncio
import logging

import uvicorn

from monitor.app import app, service
from monitor.scheduler import PollScheduler

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    scheduler = PollScheduler(service.poll_all)
    await scheduler.start()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    try:
        await server.serve()
    finally:
        await scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
