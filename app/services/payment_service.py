from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.payment import Payment

from db.enums import PaymentStatusEnum

from app.services.outbox_service import add_event

EVENT_TYPE = "payment.created"


async def create_payment(
    session: AsyncSession,
    payload,
    idempotency_key: str,
):

    query = select(Payment).where(Payment.idempotency_key == idempotency_key)

    existing_payment = await session.scalar(query)

    if existing_payment:

        return existing_payment, False

    payment = Payment(
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        metadata_json=payload.metadata,
        webhook_url=str(payload.webhook_url),
        status=PaymentStatusEnum.pending,
        idempotency_key=idempotency_key,
    )

    session.add(payment)

    try:

        await session.flush()

    except IntegrityError:

        await session.rollback()

        existing_payment = await session.scalar(query)

        return existing_payment, False

    await add_event(
        session,
        event_type=EVENT_TYPE,
        payload={
            "payment_id": str(payment.id),
            "amount": float(payment.amount),
            "currency": payment.currency.value,
            "webhook_url": payment.webhook_url,
        },
    )

    await session.commit()

    return payment, True


async def get_payment(
    session: AsyncSession,
    payment_id,
):

    query = select(Payment).where(Payment.id == payment_id)

    payment = await session.scalar(query)

    return payment
