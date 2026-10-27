from notifica_govbr.adapters.fake import FakeNotificationAdapter
from notifica_govbr.client import NotificaClient
from notifica_govbr.domain import Notification, Recipient


def _notification(cpfs=("12345678901",)):
    return Notification(
        subject="Hello",
        recipients=[Recipient(cpf=c) for c in cpfs],
        has_push=True,
        template_id=1,
        version=1,
    )


def test_client_delegates_to_port():
    fake = FakeNotificationAdapter()
    client = NotificaClient(fake)
    n = _notification()

    response = client.send(n)

    assert fake.sent == [n]
    assert response.cpf_successes == ["12345678901"]
    assert response.failed == []


def test_client_partial_failure():
    fake = FakeNotificationAdapter(failing_cpfs={"98765432100"})
    client = NotificaClient(fake)
    n = _notification(("12345678901", "98765432100"))

    response = client.send(n)

    assert response.cpf_successes == ["12345678901"]
    assert response.failed[0].cpfs == ["98765432100"]


def test_client_works_with_any_object_that_has_send():
    """Prova o typing estrutural: nada de herança de NotificationPort."""

    class AdHocAdapter:
        def __init__(self) -> None:
            self.calls = 0

        def send(self, notification: Notification):
            self.calls += 1
            from notifica_govbr.domain import SendResponse

            return SendResponse(failed=[], cpf_successes=[])

    ad_hoc = AdHocAdapter()
    client = NotificaClient(ad_hoc)  # type: ignore[arg-type]

    client.send(_notification())

    assert ad_hoc.calls == 1


def test_client_can_swap_implementations():
    """O mesmo client funciona com fake; o próximo teste, com HTTP."""
    fake = FakeNotificationAdapter()
    client = NotificaClient(fake)

    client.send(_notification())

    assert len(fake.sent) == 1
