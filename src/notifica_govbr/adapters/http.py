from typing import Self

import httpx

from notifica_govbr.adapters._parse import parse_response
from notifica_govbr.adapters._payload import build_payload
from notifica_govbr.domain import Notification, SendResponse

SEND_PATH = "/orgao/mensagem/enviar"


class HttpNotificationAdapter:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        api_key_header: str = "Authorization",
        auth_scheme: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        header_value = f"{auth_scheme} {api_key}" if auth_scheme else api_key
        self._client = httpx.Client(
            base_url=base_url,
            headers={api_key_header: header_value},
            timeout=timeout,
        )

    def send(self, notification: Notification) -> SendResponse:
        response = self._client.post(
            SEND_PATH,
            json=build_payload(notification),
        )
        response.raise_for_status()
        return parse_response(response.json())

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()
