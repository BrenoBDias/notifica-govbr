import pytest

from notifica_govbr.integration.fastapi import (
    NotificaSettings,
    get_notifica_client,
    get_settings,
)


def test_settings_read_from_env(monkeypatch):
    monkeypatch.setenv("NOTIFICA_BASE_URL", "https://example.test")
    monkeypatch.setenv("NOTIFICA_API_KEY", "secret")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.base_url == "https://example.test"
    assert settings.api_key == "secret"


def test_settings_missing_field_raises(monkeypatch):
    monkeypatch.delenv("NOTIFICA_BASE_URL", raising=False)
    monkeypatch.delenv("NOTIFICA_API_KEY", raising=False)

    with pytest.raises(ValueError, match="base_url"):
        NotificaSettings(_env_file=None)  # type: ignore[call-arg]


def test_get_client_builds_adapter_from_settings(monkeypatch):
    monkeypatch.setenv("NOTIFICA_BASE_URL", "https://example.test")
    monkeypatch.setenv("NOTIFICA_API_KEY", "secret")
    get_settings.cache_clear()

    client = get_notifica_client()
    base_url = client._port._client.base_url

    assert base_url.scheme == "https"
    assert base_url.host == "example.test"
    assert client._port._client.headers["Authorization"] == "secret"


def test_get_settings_is_cached(monkeypatch):
    monkeypatch.setenv("NOTIFICA_BASE_URL", "https://example.test")
    monkeypatch.setenv("NOTIFICA_API_KEY", "secret")
    get_settings.cache_clear()

    assert get_settings() is get_settings()


def test_explicit_values_override_env(monkeypatch):
    monkeypatch.setenv("NOTIFICA_BASE_URL", "https://from-env.test")
    monkeypatch.setenv("NOTIFICA_API_KEY", "env-key")
    get_settings.cache_clear()

    settings = NotificaSettings(
        base_url="https://override.test",  # type: ignore[call-arg]
        api_key="override-key",  # type: ignore[call-arg]
    )

    assert settings.base_url == "https://override.test"
    assert settings.api_key == "override-key"
