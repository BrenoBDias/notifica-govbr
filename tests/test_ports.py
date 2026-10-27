from notifica_govbr.domain import Notification, Recipient, SendResponse
from notifica_govbr.ports import NotificationPort


class _StubAdapter:
    """Implementa a porta SEM herdar de NotificationPort."""

    def send(self, notification: Notification) -> SendResponse:
        return SendResponse(
            failed=[], cpf_successes=[r.cpf for r in notification.recipients]
        )


def _assert_implements_port(port: NotificationPort) -> None:
    """Helper de tipo: se o argumento não satisfizer a porta, mypy reclama."""


def test_structural_typing_accepts_any_object_with_send():
    stub = _StubAdapter()
    _assert_implements_port(stub)  # verificado pelo mypy, não em runtime


def test_protocol_method_signature_matches_domain_types():
    notification = Notification(
        subject="Hello",
        recipients=[Recipient(cpf="12345678901")],
        has_push=True,
        template_id=1,
        version=1,
    )
    stub = _StubAdapter()
    response = stub.send(notification)

    assert isinstance(response, SendResponse)
    assert response.cpf_successes == ["12345678901"]
