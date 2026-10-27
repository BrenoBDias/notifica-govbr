# notifica-govbr

Biblioteca Python para envio de notificações à **Caixa Postal Digital do cidadão**,
com entrega opcional por **push no aplicativo gov.br**, via API do SERPRO.

> **Público-alvo:** órgãos e entidades da Administração Pública com acesso à API
> de envio de mensagens da Caixa Postal.

## Instalação

```bash
pip install notifica-govbr
```

## Pré-requisitos

- **API key** fornecida pelo SERPRO para o seu órgão.
- **Template cadastrado** previamente no serviço. A biblioteca referencia um
  `template_id`; ela não cria templates.

## Uso básico

```python
from notifica_govbr import (
    HttpNotificationAdapter,
    NotificaClient,
    Notification,
    Recipient,
)

adapter = HttpNotificationAdapter(
    base_url="https://h-api-orgaos-cxpostal.np.estaleiro.serpro.gov.br",  # homologação
    api_key="sua-api-key",
)

client = NotificaClient(adapter)

response = client.send(
    Notification(
        subject="Olá, cidadão",
        recipients=[
            Recipient(cpf="12345678901", tags={"nome": "Maria"}),
        ],
        has_push=True,
        template_id=42,
        version=1,
        tags={"documento": "CNH"},
    )
)

print(response.cpf_successes)   # ['12345678901']
print(response.failed)          # []  ou  [FailedSend(cpfs=[...], reason='...')]
```

O adaptador HTTP gerencia o ciclo de vida da conexão e pode ser usado como
_context manager_:

```python
with HttpNotificationAdapter(base_url=..., api_key=...) as adapter:
    client = NotificaClient(adapter)
    client.send(...)
```

## Testes com a API fake

A biblioteca inclui um adaptador em memória para testar o seu código sem rede.
Ele implementa a mesma porta do adaptador HTTP e registra o que foi enviado:

```python
from notifica_govbr import FakeNotificationAdapter, NotificaClient

fake = FakeNotificationAdapter()
client = NotificaClient(fake)

client.send(...)

assert fake.sent[0].subject == "Olá, cidadão"
```

Para simular falhas por CPF:

```python
fake = FakeNotificationAdapter(
    failing_cpfs={"98765432100"},
    failure_reason="CPF não encontrado",
)
response = NotificaClient(fake).send(...)

assert response.failed[0].cpfs == ["98765432100"]
assert response.failed[0].reason == "CPF não encontrado"
```

## Formato da resposta

`SendResponse` reflete o contrato da API (`falhas`/`sucessos`):

- `response.cpf_successes: list[str]` — CPFs processados com sucesso.
- `response.failed: list[FailedSend]` — falhas agrupadas por motivo.
  - `FailedSend.cpfs: list[str]`
  - `FailedSend.reason: str`

Falhas **por destinatário** vêm no `SendResponse`. Falhas **de transporte**
(timeout, `401`, `5xx`) viram exceções `httpx.HTTPError` — o usuário trata
os dois casos em lugares diferentes, sem misturar.

## API pública

```python
from notifica_govbr import (
    FailedSend,
    FakeNotificationAdapter,
    HttpNotificationAdapter,
    NotificaClient,
    Notification,
    NotificationPort,
    Recipient,
    SendResponse,
)
```

`NotificationPort` é o `Protocol` que qualquer adaptador precisa cumprir. Use-o
apenas se quiser implementar um adaptador próprio (ex: cache, fila, outro
transporte). Para o uso comum, basta `HttpNotificationAdapter` ou
`FakeNotificationAdapter`.

## Status

Versão **0.1.0** — adaptador síncrono (`httpx.Client`). Versão assíncrona
(`httpx.AsyncClient`) planejada para uma versão futura, sem quebrar a API atual.

## Licença

Este projeto está licenciado sob a **Apache License 2.0**.
Veja o arquivo [LICENSE](LICENSE) para o texto completo.
