from notifica_govbr.domain import FailedSend, Notification, SendResponse


class FakeNotificationAdapter:
    def __init__(
        self,
        failing_cpfs: set[str] | None = None,
        failure_reason: str = "simulated_failure",
    ) -> None:
        self.sent: list[Notification] = []
        self._failing_cpfs = failing_cpfs or set()
        self._failure_reason = failure_reason

    def send(self, notification: Notification) -> SendResponse:
        self.sent.append(notification)

        successes: list[str] = []
        failed_cpfs: list[str] = []

        for recipient in notification.recipients:
            if recipient.cpf in self._failing_cpfs:
                failed_cpfs.append(recipient.cpf)
            else:
                successes.append(recipient.cpf)

        failed = (
            [FailedSend(cpfs=failed_cpfs, reason=self._failure_reason)]
            if failed_cpfs
            else []
        )

        return SendResponse(failed=failed, cpf_successes=successes)
