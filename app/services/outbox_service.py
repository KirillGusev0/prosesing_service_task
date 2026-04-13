from sqlalchemy.ext.asyncio import AsyncSession

from db.models.outbox import Outbox
from db.enums import OutboxStatusEnum


async def add_event(
    session: AsyncSession,
    event_type: str,
    payload: dict,
):
    event = Outbox(
        event_type=event_type,
        payload=payload,
        status=OutboxStatusEnum.pending,
    )

    session.add(event)
