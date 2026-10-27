from notifica_govbr.domain import Notification, SendResponse
from notifica_govbr.ports import NotificationPort


class NotificaClient:
    def __init__(self, port: NotificationPort) -> None:
        self._port = port

    def send(self, notification: Notification) -> SendResponse:
        return self._port.send(notification)
