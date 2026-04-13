import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    JSON,
    Numeric,
    String,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

from db.enums import CurrencyEnum, PaymentStatusEnum


class Payment(Base):

    __tablename__ = "payments"

    __table_args__ = (
        UniqueConstraint(
            "idempotency_key",
            name="uq_payment_idempotency_key",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
    )

    currency: Mapped[CurrencyEnum] = mapped_column(
        Enum(CurrencyEnum),
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum),
        default=PaymentStatusEnum.pending,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    webhook_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
