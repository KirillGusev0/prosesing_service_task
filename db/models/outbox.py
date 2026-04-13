import uuid
from datetime import datetime

from sqlalchemy import DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.enums import OutboxStatusEnum


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    event_type: Mapped[str]

    payload: Mapped[dict] = mapped_column(JSON)

    status: Mapped[OutboxStatusEnum] = mapped_column(
        Enum(OutboxStatusEnum),
        default=OutboxStatusEnum.pending,
    )

    retry_count: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
