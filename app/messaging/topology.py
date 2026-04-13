from faststream.rabbit import RabbitExchange, RabbitQueue

from app.messaging.config import (
    PAYMENTS_EXCHANGE,
    PAYMENTS_QUEUE,
    PAYMENTS_DLQ,
    ROUTING_KEY,
)

payments_exchange = RabbitExchange(
    PAYMENTS_EXCHANGE,
    type="direct",
)


payments_queue = RabbitQueue(
    PAYMENTS_QUEUE,
    routing_key=ROUTING_KEY,
    durable=True,
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": PAYMENTS_DLQ,
    },
)


payments_dlq = RabbitQueue(
    PAYMENTS_DLQ,
    routing_key=PAYMENTS_DLQ,
    durable=True,
)
