import asyncio
import random
from datetime import datetime
from uuid import UUID

import aiohttp

from faststream import FastStream
from faststream.rabbit import RabbitRouter

from db.session import SessionLocal
from db.models.payment import Payment
from db.enums import PaymentStatusEnum

from app.messaging.broker import broker
from app.messaging.topology import payments_queue

router = RabbitRouter()


async def fake_gateway():
    await asyncio.sleep(random.randint(2, 5))
    return random.random() < 0.9


async def send_webhook(url: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return response.status < 400


async def retry_webhook(url: str, payload: dict):
    delay = 1

    for _ in range(3):
        success = await send_webhook(url, payload)

        if success:
            return True

        await asyncio.sleep(delay)
        delay *= 2

    return False


@router.subscriber(queue=payments_queue)
async def handle_payment(event: dict):
    success = await fake_gateway()

    async with SessionLocal() as session:
        payment = await session.get(
            Payment,
            UUID(event["payment_id"]),
        )

        payment.status = (
            PaymentStatusEnum.succeeded if success else PaymentStatusEnum.failed
        )

        payment.processed_at = datetime.utcnow()

        await session.commit()

    await retry_webhook(
        event["webhook_url"],
        {
            "payment_id": event["payment_id"],
            "status": payment.status.value,
        },
    )


app = FastStream(broker)
broker.include_router(router)


if __name__ == "__main__":
    asyncio.run(app.run())
