import sys
import types

import pytest

from notifica_govbr.integration.django import get_notifica_client


def _fake_django_settings(monkeypatch, **values):
    """Cria um django.conf.settings fake com os valores passados."""
    fake_settings = types.SimpleNamespace(**values)
    fake_conf = types.ModuleType("django.conf")
    fake_conf.settings = fake_settings
    fake_django = types.ModuleType("django")
    fake_django.conf = fake_conf

    monkeypatch.setitem(sys.modules, "django", fake_django)
    monkeypatch.setitem(sys.modules, "django.conf", fake_conf)
    return fake_settings


def test_get_client_reads_from_django_settings(monkeypatch):
    _fake_django_settings(
        monkeypatch,
        NOTIFICA_BASE_URL="https://example.test",
        NOTIFICA_API_KEY="secret",
    )

    client = get_notifica_client()
    base_url = client._port._client.base_url

    assert base_url.scheme == "https"
    assert base_url.host == "example.test"
    assert client._port._client.headers["Authorization"] == "secret"


def test_get_client_missing_setting_raises(monkeypatch):
    _fake_django_settings(
        monkeypatch,
        NOTIFICA_API_KEY="secret",
        # NOTIFICA_BASE_URL ausente de propósito
    )

    with pytest.raises(AttributeError, match="NOTIFICA_BASE_URL"):
        get_notifica_client()


def test_get_client_missing_api_key_raises(monkeypatch):
    _fake_django_settings(
        monkeypatch,
        NOTIFICA_BASE_URL="https://example.test",
    )

    with pytest.raises(AttributeError, match="NOTIFICA_API_KEY"):
        get_notifica_client()
