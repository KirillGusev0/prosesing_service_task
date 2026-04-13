from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from db.enums import CurrencyEnum, PaymentStatusEnum


class CreatePaymentRequest(BaseModel):

    amount: Decimal

    currency: CurrencyEnum

    description: str | None = None

    metadata: dict | None = None

    webhook_url: HttpUrl


class PaymentResponse(BaseModel):

    id: UUID

    amount: Decimal

    currency: CurrencyEnum

    description: str | None

    metadata: dict | None

    status: PaymentStatusEnum

    webhook_url: HttpUrl

    created_at: datetime

    processed_at: datetime | None


class CreatePaymentResponse(BaseModel):

    payment_id: UUID

    status: PaymentStatusEnum

    created_at: datetime
