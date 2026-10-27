"""Integração com FastAPI usando pydantic-settings.

Uso:
    from notifica_govbr.integration.fastapi import get_notifica_client

    @app.post("/notificar")
    def notificar(client: NotificaClient = Depends(get_notifica_client)):
        return client.send(...)

Variáveis de ambiente esperadas (prefixo NOTIFICA_):
    NOTIFICA_BASE_URL   URL da API (produção ou homologação)
    NOTIFICA_API_KEY    Chave de acesso fornecida pelo SERPRO
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from notifica_govbr.adapters.http import HttpNotificationAdapter
from notifica_govbr.client import NotificaClient


class NotificaSettings(BaseSettings):
    """Configurações do cliente Notifica, carregadas do ambiente ou de .env."""

    base_url: str
    api_key: str

    model_config = SettingsConfigDict(
        env_prefix="NOTIFICA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> NotificaSettings:
    """Retorna as settings, com cache para não reler o ambiente a cada request."""
    return NotificaSettings()  # type: ignore[call-arg]


def get_notifica_client() -> NotificaClient:
    """Dependency do FastAPI que monta o NotificaClient a partir das settings."""
    settings = get_settings()
    adapter = HttpNotificationAdapter(
        base_url=settings.base_url,
        api_key=settings.api_key,
    )
    return NotificaClient(adapter)
