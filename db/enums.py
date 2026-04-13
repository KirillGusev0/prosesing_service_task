import enum


class CurrencyEnum(str, enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentStatusEnum(str, enum.Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"


class OutboxStatusEnum(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
