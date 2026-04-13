import asyncio
import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


MAX_RETRIES = 3

INITIAL_DELAY = 1


async def send_webhook(
    url: str,
    payload: dict[str, Any],
) -> bool:

    try:

        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(
            timeout=timeout,
        ) as session:

            async with session.post(
                url,
                json=payload,
            ) as response:

                if response.status < 400:

                    logger.info(
                        "webhook sent",
                        extra={
                            "url": url,
                            "status": response.status,
                        },
                    )

                    return True

                logger.warning(
                    "webhook failed",
                    extra={
                        "url": url,
                        "status": response.status,
                    },
                )

                return False

    except Exception as e:

        logger.exception(
            "webhook exception",
            extra={
                "url": url,
                "error": str(e),
            },
        )

        return False


async def send_webhook_with_retry(
    url: str,
    payload: dict[str, Any],
) -> bool:

    delay = INITIAL_DELAY

    for attempt in range(1, MAX_RETRIES + 1):

        success = await send_webhook(
            url,
            payload,
        )

        if success:

            return True

        logger.warning(
            "retry webhook",
            extra={
                "attempt": attempt,
                "delay": delay,
            },
        )

        await asyncio.sleep(delay)

        delay *= 2

    logger.error(
        "webhook failed after retries",
        extra={
            "url": url,
        },
    )

    return False
