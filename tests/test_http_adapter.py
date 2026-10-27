import httpx
import pytest
import respx

from notifica_govbr.adapters.http import SEND_PATH, HttpNotificationAdapter
from notifica_govbr.domain import Notification, Recipient

BASE_URL = "https://h-api-orgaos-cxpostal.np.estaleiro.serpro.gov.br"
API_KEY = "test-key"
FULL_URL = f"{BASE_URL}{SEND_PATH}"


def _notification(cpfs=("12345678901",)):
    return Notification(
        subject="Hello",
        recipients=[Recipient(cpf=c) for c in cpfs],
        has_push=True,
        template_id=1,
        version=1,
    )


@respx.mock
def test_send_success():
    route = respx.post(FULL_URL).mock(
        return_value=httpx.Response(
            200, json={"falhas": [], "sucessos": ["12345678901"]}
        )
    )

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    response = adapter.send(_notification())

    assert response.failed == []
    assert response.cpf_successes == ["12345678901"]
    assert route.called


@respx.mock
def test_send_payload_matches_wire_format():
    route = respx.post(FULL_URL).mock(
        return_value=httpx.Response(200, json={"falhas": [], "sucessos": []})
    )

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    adapter.send(_notification())

    import json

    body = json.loads(route.calls[0].request.content)
    assert body == {
        "assunto": "Hello",
        "destinatarios": [{"cpf": "12345678901", "tags": {}}],
        "has_push": True,
        "tags": {},
        "template_id": 1,
        "versao": 1,
    }


@respx.mock
def test_send_partial_failure():
    respx.post(FULL_URL).mock(
        return_value=httpx.Response(
            200,
            json={
                "falhas": [{"cpfs": ["98765432100"], "motivo": "CPF não encontrado"}],
                "sucessos": ["12345678901"],
            },
        )
    )

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    response = adapter.send(_notification(("12345678901", "98765432100")))

    assert response.cpf_successes == ["12345678901"]
    assert len(response.failed) == 1
    assert response.failed[0].cpfs == ["98765432100"]
    assert response.failed[0].reason == "CPF não encontrado"


@respx.mock
def test_send_missing_fields_treated_as_empty():
    respx.post(FULL_URL).mock(return_value=httpx.Response(200, json={}))

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    response = adapter.send(_notification())

    assert response.failed == []
    assert response.cpf_successes == []


@respx.mock
def test_send_raises_on_401():
    respx.post(FULL_URL).mock(return_value=httpx.Response(401))

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    with pytest.raises(httpx.HTTPStatusError):
        adapter.send(_notification())


@respx.mock
def test_send_raises_on_timeout():
    respx.post(FULL_URL).mock(side_effect=httpx.TimeoutException("timeout"))

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    with pytest.raises(httpx.TimeoutException):
        adapter.send(_notification())


@respx.mock
def test_send_sets_authorization_header():
    route = respx.post(FULL_URL).mock(
        return_value=httpx.Response(200, json={"falhas": [], "sucessos": []})
    )

    adapter = HttpNotificationAdapter(base_url=BASE_URL, api_key=API_KEY)
    adapter.send(_notification())

    request = route.calls[0].request
    assert request.headers["Authorization"] == API_KEY


@respx.mock
def test_send_supports_auth_scheme_prefix():
    route = respx.post(FULL_URL).mock(
        return_value=httpx.Response(200, json={"falhas": [], "sucessos": []})
    )

    adapter = HttpNotificationAdapter(
        base_url=BASE_URL, api_key=API_KEY, auth_scheme="Bearer"
    )
    adapter.send(_notification())

    request = route.calls[0].request
    assert request.headers["Authorization"] == f"Bearer {API_KEY}"
