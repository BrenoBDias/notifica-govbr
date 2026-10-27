from typing import Protocol

from notifica_govbr.domain import Notification, SendResponse


class NotificationPort(Protocol):
    def send(self, notification: Notification) -> SendResponse: ...
