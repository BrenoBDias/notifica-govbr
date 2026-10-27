from dataclasses import dataclass, field


@dataclass(frozen=True)
class Recipient:
    cpf: str
    tags: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValueError("CPF must have 11 digits")


@dataclass(frozen=True)
class Notification:
    subject: str
    recipients: list[Recipient]
    has_push: bool
    template_id: int
    version: int
    tags: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.recipients:
            raise ValueError("Notification must have at least one recipient")
        if not self.subject.strip():
            raise ValueError("subject must not be empty")
        seen: set[str] = set()
        for r in self.recipients:
            if r.cpf in seen:
                raise ValueError(f"duplicate CPF in recipients: {r.cpf}")
            seen.add(r.cpf)


@dataclass(frozen=True)
class FailedSend:
    cpfs: list[str]
    reason: str


@dataclass(frozen=True)
class SendResponse:
    failed: list[FailedSend]
    cpf_successes: list[str]
