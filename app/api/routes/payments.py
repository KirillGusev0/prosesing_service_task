from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import verify_api_key
from db.session import get_session
from app.schemas.payment import (
    CreatePaymentRequest,
    CreatePaymentResponse,
    PaymentResponse,
)
from app.services.payment_service import (
    create_payment,
    get_payment,
)

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"],
    dependencies=[Depends(verify_api_key)],
)


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CreatePaymentResponse,
)
async def create_payment_endpoint(
    payload: CreatePaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    session: AsyncSession = Depends(get_session),
):

    payment, created = await create_payment(
        session,
        payload,
        idempotency_key,
    )

    return CreatePaymentResponse(
        payment_id=payment.id,
        status=payment.status,
        created_at=payment.created_at,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment_endpoint(
    payment_id: UUID,
    session: AsyncSession = Depends(get_session),
):

    payment = await get_payment(
        session,
        payment_id,
    )

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return payment
