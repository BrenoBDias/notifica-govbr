"""Integração com Django.

Uso:
    # settings.py
    NOTIFICA_BASE_URL = "https://..."
    NOTIFICA_API_KEY = "..."

    # views.py
    from notifica_govbr.integration.django import get_notifica_client

    def minha_view(request):
        client = get_notifica_client()
        client.send(...)
"""

from notifica_govbr.adapters.http import HttpNotificationAdapter
from notifica_govbr.client import NotificaClient


def get_notifica_client() -> NotificaClient:
    """Monta o NotificaClient a partir de django.conf.settings.

    O import é preguiçoso: este módulo pode ser importado mesmo sem Django
    instalado; só a chamada desta função exige Django configurado.
    """
    from django.conf import settings

    return NotificaClient(
        HttpNotificationAdapter(
            base_url=settings.NOTIFICA_BASE_URL,
            api_key=settings.NOTIFICA_API_KEY,
        )
    )
