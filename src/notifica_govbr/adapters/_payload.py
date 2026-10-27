from typing import Any

from notifica_govbr.domain import Notification


def build_payload(notification: Notification) -> dict[str, Any]:
    return {
        "assunto": notification.subject,
        "destinatarios": [
            {"cpf": r.cpf, "tags": r.tags} for r in notification.recipients
        ],
        "has_push": notification.has_push,
        "tags": notification.tags,
        "template_id": notification.template_id,
        "versao": notification.version,
    }
