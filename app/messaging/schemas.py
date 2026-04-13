from pydantic import BaseModel
from uuid import UUID


class PaymentCreatedEvent(BaseModel):
    payment_id: UUID
    amount: float
    currency: str
    webhook_url: str
