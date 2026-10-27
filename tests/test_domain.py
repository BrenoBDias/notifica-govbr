from dataclasses import FrozenInstanceError

import pytest

from notifica_govbr.domain import (
    FailedSend,
    Notification,
    Recipient,
    SendResponse,
)

# --- Recipient ---


def test_recipient_valid():
    r = Recipient(cpf="12345678901")
    assert r.cpf == "12345678901"
    assert r.tags == {}


def test_recipient_cpf_with_leading_zero_is_valid():
    r = Recipient(cpf="01234567890")
    assert r.cpf == "01234567890"


@pytest.mark.parametrize(
    "invalid_cpf",
    ["", "123", "123456789012", "abcdefghijk", "1234567890a"],
)
def test_recipient_invalid_cpf_raises(invalid_cpf):
    with pytest.raises(ValueError, match="CPF"):
        Recipient(cpf=invalid_cpf)


def test_recipient_tags_are_not_shared():
    r1 = Recipient(cpf="12345678901")
    r2 = Recipient(cpf="12345678901")
    assert r1.tags is not r2.tags


def test_recipient_is_frozen():
    r = Recipient(cpf="12345678901")
    with pytest.raises(FrozenInstanceError):
        r.cpf = "98765432100"  # type: ignore[misc]


# --- Notification ---


def _make_notification(**overrides):
    base = {
        "subject": "Hello",
        "recipients": [Recipient(cpf="12345678901")],
        "has_push": True,
        "template_id": 1,
        "version": 1,
    }
    base.update(overrides)
    return Notification(**base)


def test_notification_valid():
    n = _make_notification()
    assert n.subject == "Hello"
    assert len(n.recipients) == 1
    assert n.has_push is True
    assert n.template_id == 1
    assert n.version == 1
    assert n.tags == {}


def test_notification_empty_recipients_raises():
    with pytest.raises(ValueError, match="at least one recipient"):
        _make_notification(recipients=[])


def test_notification_empty_subject_raises():
    with pytest.raises(ValueError, match="subject"):
        _make_notification(subject="   ")


def test_notification_duplicate_cpf_raises():
    duplicates = [
        Recipient(cpf="12345678901"),
        Recipient(cpf="12345678901"),
    ]
    with pytest.raises(ValueError, match="duplicate CPF"):
        _make_notification(recipients=duplicates)


def test_notification_tags_are_not_shared():
    n1 = _make_notification()
    n2 = _make_notification()
    assert n1.tags is not n2.tags


def test_notification_is_frozen():
    n = _make_notification()
    with pytest.raises(FrozenInstanceError):
        n.subject = "Changed"  # type: ignore[misc]


# --- FailedSend ---


def test_failed_send():
    f = FailedSend(cpfs=["12345678901"], reason="invalid_cpf")
    assert f.cpfs == ["12345678901"]
    assert f.reason == "invalid_cpf"


# --- SendResponse ---


def test_send_response_all_success():
    r = SendResponse(failed=[], cpf_successes=["12345678901"])
    assert r.failed == []
    assert r.cpf_successes == ["12345678901"]


def test_send_response_with_failures():
    r = SendResponse(
        failed=[FailedSend(cpfs=["12345678901"], reason="invalid_cpf")],
        cpf_successes=["98765432100"],
    )
    assert len(r.failed) == 1
    assert r.failed[0].cpfs == ["12345678901"]
    assert r.cpf_successes == ["98765432100"]
