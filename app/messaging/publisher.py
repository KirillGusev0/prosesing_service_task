import asyncio

from sqlalchemy import select

from db.session import SessionLocal
from db.models.outbox import Outbox
from db.enums import OutboxStatusEnum

from app.messaging.broker import broker
from app.messaging.topology import payments_queue

RETRY_LIMIT = 3


async def publish_event(event: Outbox):
    try:
        await broker.publish(
            event.payload,
            queue=payments_queue.name,
        )

        event.status = OutboxStatusEnum.sent
        print(f" Sent event {event.id}")

    except Exception as e:
        print(f" Error sending event {event.id}: {e}")

        event.retry_count += 1

        if event.retry_count >= RETRY_LIMIT:
            event.status = OutboxStatusEnum.failed


async def outbox_loop():
    while True:
        try:
            await broker.connect()
            break
        except Exception:
            print("RabbitMQ not ready, retrying...")
            await asyncio.sleep(2)

    while True:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Outbox).where(Outbox.status == OutboxStatusEnum.pending)
            )

            events = result.scalars().all()

            for event in events:
                await publish_event(event)

            await session.commit()

        await asyncio.sleep(2)
        
if __name__ == "__main__":

    asyncio.run(outbox_loop())
