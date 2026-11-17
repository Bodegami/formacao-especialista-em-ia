"""Casos de uso: um por operação permitida.

Recebem a entrada BRUTA vinda do LLM (texto), convertem e validam via domínio,
aplicam a operação e persistem. Retornam DTOs imutáveis — a entidade não vaza
para as camadas externas.
"""

from dataclasses import dataclass
from decimal import Decimal

from agente_bancario.application.ports import AccountRepository
from agente_bancario.domain.money import parse_amount


@dataclass(frozen=True)
class BalanceResult:
    account_id: str
    balance: Decimal


@dataclass(frozen=True)
class DepositResult:
    account_id: str
    amount: Decimal
    new_balance: Decimal


@dataclass(frozen=True)
class TransferResult:
    origin: str
    recipient: str
    amount: Decimal
    new_balance: Decimal


class GetBalanceUseCase:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    def execute(self) -> BalanceResult:
        account = self._repository.get()
        return BalanceResult(account.account_id, account.balance)


class DepositUseCase:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    def execute(self, raw_amount: object) -> DepositResult:
        amount = parse_amount(raw_amount)  # lança InvalidAmountError antes de tocar no estado
        account = self._repository.get()
        new_balance = account.deposit(amount)
        self._repository.save(account)
        return DepositResult(account.account_id, amount, new_balance)


class TransferUseCase:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    def execute(self, raw_amount: object, recipient: str | None) -> TransferResult:
        amount = parse_amount(raw_amount)
        account = self._repository.get()
        new_balance = account.transfer(amount, recipient)
        self._repository.save(account)
        last = account.transactions[-1]
        return TransferResult(account.account_id, last.recipient or "", amount, new_balance)
