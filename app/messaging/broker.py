from faststream.rabbit import RabbitBroker

from app.messaging.config import RABBIT_URL

broker = RabbitBroker(
    RABBIT_URL,
)
