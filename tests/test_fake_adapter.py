from notifica_govbr.adapters.fake import FakeNotificationAdapter
from notifica_govbr.domain import Notification, Recipient


def _notification(cpfs=("12345678901",)):
    return Notification(
        subject="Hello",
        recipients=[Recipient(cpf=c) for c in cpfs],
        has_push=True,
        template_id=1,
        version=1,
    )


def test_fake_success_all():
    fake = FakeNotificationAdapter()
    notification = _notification(("12345678901", "98765432100"))

    response = fake.send(notification)

    assert response.failed == []
    assert response.cpf_successes == ["12345678901", "98765432100"]
    assert fake.sent == [notification]


def test_fake_partial_failure():
    fake = FakeNotificationAdapter(failing_cpfs={"98765432100"})
    notification = _notification(("12345678901", "98765432100"))

    response = fake.send(notification)

    assert response.cpf_successes == ["12345678901"]
    assert len(response.failed) == 1
    assert response.failed[0].cpfs == ["98765432100"]
    assert response.failed[0].reason == "simulated_failure"


def test_fake_all_fail():
    fake = FakeNotificationAdapter(failing_cpfs={"12345678901", "98765432100"})
    notification = _notification(("12345678901", "98765432100"))

    response = fake.send(notification)

    assert response.cpf_successes == []
    assert sorted(response.failed[0].cpfs) == ["12345678901", "98765432100"]


def test_fake_records_multiple_sends():
    fake = FakeNotificationAdapter()
    n1 = _notification(("12345678901",))
    n2 = _notification(("98765432100",))

    fake.send(n1)
    fake.send(n2)

    assert fake.sent == [n1, n2]
