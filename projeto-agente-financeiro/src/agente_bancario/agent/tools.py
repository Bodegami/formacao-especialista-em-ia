"""Ferramentas expostas ao LLM (adaptador entre o modelo e os casos de uso).

Regras de projeto:
- Existem EXATAMENTE três ferramentas. O modelo não tem como executar nada além disso.
- O modelo nunca calcula: ele só passa o valor bruto que o usuário disse. O cálculo,
  a validação e a formatação acontecem aqui/no domínio.
- O retorno é sempre texto começando com "OK:" ou "ERRO:", com os valores já
  formatados — o modelo só precisa repassar, sem refazer contas.
- Exceções de domínio viram "ERRO: <motivo>"; exceções inesperadas viram um erro
  genérico (sem vazar detalhes internos) e o saldo permanece intacto.
"""

import threading
from collections.abc import Callable
from decimal import Decimal

from langchain_core.tools import BaseTool, tool

from agente_bancario.application.ports import AccountRepository
from agente_bancario.application.use_cases import (
    DepositUseCase,
    GetBalanceUseCase,
    TransferUseCase,
)
from agente_bancario.domain.errors import DomainError
from agente_bancario.domain.money import format_brl, parse_amount

_GENERIC_ERROR = "ERRO: não foi possível concluir a operação. Nenhum valor foi alterado."


class TurnGuard:
    """Bloqueia a repetição de uma operação IDÊNTICA dentro da mesma mensagem do usuário.

    Protege contra o modelo chamar a mesma ferramenta duas vezes por engano
    (ex.: depositar 100 duas vezes para um único pedido). Se o usuário realmente
    quiser repetir, o modelo deve pedir confirmação, e a repetição ocorre no turno
    seguinte. `reset()` é chamado pelo agente a cada nova mensagem do usuário.
    """

    def __init__(self) -> None:
        self._executed: set[tuple[str, Decimal, str]] = set()

    def reset(self) -> None:
        self._executed.clear()

    def already_executed(self, signature: tuple[str, Decimal, str] | None) -> bool:
        return signature is not None and signature in self._executed

    def record(self, signature: tuple[str, Decimal, str] | None) -> None:
        if signature is not None:
            self._executed.add(signature)


def _signature(op: str, raw_amount: str, recipient: str = "") -> tuple[str, Decimal, str] | None:
    try:
        amount = parse_amount(raw_amount)
    except DomainError:
        return None  # valor inválido: o caso de uso vai rejeitar com a mensagem correta
    return (op, amount, " ".join(recipient.split()).casefold())


def _safe(run: Callable[[], str], lock: threading.Lock) -> str:
    # O lock serializa as operações: se o modelo pedir chamadas em paralelo,
    # o LangGraph as executa em threads e duas transferências não podem
    # ler o mesmo saldo ao mesmo tempo.
    try:
        with lock:
            return run()
    except DomainError as exc:
        return f"ERRO: {exc.message} Nenhum valor foi alterado."
    except Exception:  # noqa: BLE001 - nunca deixar o agente quebrar nem vazar stack trace
        return _GENERIC_ERROR


_DUPLICATE = (
    "ERRO: esta operação idêntica já foi executada nesta mensagem e NÃO foi repetida. "
    "Se o usuário realmente quiser repeti-la, peça confirmação explícita."
)


def build_tools(repository: AccountRepository, guard: TurnGuard) -> list[BaseTool]:
    """Cria as três ferramentas ligadas ao repositório da sessão."""
    get_balance = GetBalanceUseCase(repository)
    deposit = DepositUseCase(repository)
    transfer = TransferUseCase(repository)
    lock = threading.Lock()

    @tool
    def consultar_saldo() -> str:
        """Consulta o saldo atual da conta do usuário. Não recebe parâmetros.
        Use sempre que o usuário perguntar o saldo; nunca informe saldo sem chamar esta ferramenta."""

        def run() -> str:
            result = get_balance.execute()
            return f"OK: saldo atual da conta {result.account_id}: {format_brl(result.balance)}."

        return _safe(run, lock)

    @tool
    def depositar(valor: str) -> str:
        """Deposita um valor na conta do usuário.

        Args:
            valor: valor em reais exatamente como o usuário informou, apenas o número
                (ex.: "250", "250.50" ou "250,50"). Não faça contas nem converta o valor.
        """

        def run() -> str:
            signature = _signature("depositar", valor)
            if guard.already_executed(signature):
                return _DUPLICATE
            result = deposit.execute(valor)
            guard.record(signature)
            return (
                f"OK: depósito de {format_brl(result.amount)} realizado na conta "
                f"{result.account_id}. Novo saldo: {format_brl(result.new_balance)}."
            )

        return _safe(run, lock)

    @tool
    def transferir(valor: str, destinatario: str) -> str:
        """Transfere um valor da conta do usuário para um destinatário (envio simulado).

        Args:
            valor: valor em reais exatamente como o usuário informou, apenas o número
                (ex.: "100", "100.50" ou "100,50"). Não faça contas nem converta o valor.
            destinatario: nome ou identificação do destinatário dita pelo usuário
                (ex.: "Ana"). Nunca invente um destinatário.
        """

        def run() -> str:
            signature = _signature("transferir", valor, destinatario or "")
            if guard.already_executed(signature):
                return _DUPLICATE
            try:
                result = transfer.execute(valor, destinatario)
            except DomainError as exc:
                balance = format_brl(get_balance.execute().balance)
                return f"ERRO: {exc.message} Saldo disponível: {balance}. Nenhum valor foi alterado."
            guard.record(signature)
            return (
                f"OK: transferência realizada. Origem: conta {result.origin}. "
                f"Destinatário: {result.recipient}. Valor: {format_brl(result.amount)}. "
                f"Novo saldo: {format_brl(result.new_balance)}."
            )

        return _safe(run, lock)

    return [consultar_saldo, depositar, transferir]
