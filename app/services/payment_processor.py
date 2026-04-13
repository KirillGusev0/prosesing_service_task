import asyncio
import logging
import random
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.payment import Payment
from db.enums import PaymentStatusEnum

from app.services.webhook_service import (
    send_webhook_with_retry,
)

logger = logging.getLogger(__name__)


SUCCESS_RATE = 0.9


async def simulate_gateway() -> bool:

    processing_time = random.randint(2, 5)

    await asyncio.sleep(processing_time)

    result = random.random() < SUCCESS_RATE

    logger.info(
        "gateway processed",
        extra={
            "processing_time": processing_time,
            "success": result,
        },
    )

    return result


async def process_payment(
    session: AsyncSession,
    payment_id: UUID,
    webhook_url: str,
):

    payment: Payment | None = await session.get(
        Payment,
        payment_id,
    )

    if not payment:

        logger.error(
            "payment not found",
            extra={
                "payment_id": str(payment_id),
            },
        )

        return

    if payment.status != PaymentStatusEnum.pending:

        logger.info(
            "payment already processed",
            extra={
                "payment_id": str(payment_id),
                "status": payment.status.value,
            },
        )

        return

    success = await simulate_gateway()

    payment.status = (
        PaymentStatusEnum.succeeded if success else PaymentStatusEnum.failed
    )

    payment.processed_at = datetime.utcnow()

    await session.commit()

    webhook_payload = {
        "payment_id": str(payment.id),
        "status": payment.status.value,
        "processed_at": payment.processed_at.isoformat(),
    }

    webhook_success = await send_webhook_with_retry(
        webhook_url,
        webhook_payload,
    )

    if not webhook_success:

        logger.error(
            "webhook permanently failed",
            extra={
                "payment_id": str(payment.id),
            },
        )
