"""Biblioteca de integração com a Caixa Postal Digital do gov.br.

Envie notificações para a Caixa Postal do cidadão, com push opcional no
aplicativo gov.br.
"""

from notifica_govbr.adapters.fake import FakeNotificationAdapter
from notifica_govbr.adapters.http import HttpNotificationAdapter
from notifica_govbr.client import NotificaClient
from notifica_govbr.domain import (
    FailedSend,
    Notification,
    Recipient,
    SendResponse,
)
from notifica_govbr.ports import NotificationPort

__version__ = "0.1.0"
__license__ = "Apache-2.0"

__all__ = [
    "FailedSend",
    "FakeNotificationAdapter",
    "HttpNotificationAdapter",
    "NotificaClient",
    "Notification",
    "NotificationPort",
    "Recipient",
    "SendResponse",
    "__version__",
]
