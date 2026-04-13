import os

RABBIT_URL = os.getenv(
    "RABBIT_URL",
    "amqp://guest:guest@rabbitmq:5672/",
)


PAYMENTS_EXCHANGE = "payments.exchange"

PAYMENTS_QUEUE = "payments.new"

PAYMENTS_DLQ = "payments.dlq"

ROUTING_KEY = "payments.new"
