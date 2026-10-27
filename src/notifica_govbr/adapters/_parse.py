from typing import Any

from notifica_govbr.domain import FailedSend, SendResponse


def parse_response(data: dict[str, Any]) -> SendResponse:
    failed = [
        FailedSend(cpfs=f["cpfs"], reason=f["motivo"]) for f in data.get("falhas", [])
    ]
    successes = list(data.get("sucessos", []))
    return SendResponse(failed=failed, cpf_successes=successes)
