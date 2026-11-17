"""Entidade Account: a única fonte da verdade sobre o saldo.

O saldo só muda por `deposit` e `transfer`, que validam TUDO antes de alterar
qualquer estado. Se uma validação falha, nada é modificado (operação atômica).
"""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from agente_bancario.domain.errors import InsufficientFundsError, InvalidRecipientError
from agente_bancario.domain.money import CENTS, validate_amount

MAX_RECIPIENT_LENGTH = 80


class TransactionKind(str, Enum):
    DEPOSIT = "deposito"
    TRANSFER = "transferencia"


@dataclass(frozen=True)
class Transaction:
    kind: TransactionKind
    amount: Decimal
    balance_after: Decimal
    recipient: str | None = None


@dataclass
class Account:
    account_id: str
    _balance: Decimal
    _transactions: list[Transaction] = field(default_factory=list)

    @classmethod
    def open(cls, initial_balance: Decimal, account_id: str = "0001-9") -> "Account":
        if not isinstance(initial_balance, Decimal) or initial_balance < 0:
            raise ValueError("Saldo inicial deve ser um Decimal não negativo.")
        return cls(account_id=account_id, _balance=initial_balance.quantize(CENTS))

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        # Tupla: quem lê o histórico não consegue alterá-lo.
        return tuple(self._transactions)

    def deposit(self, amount: Decimal) -> Decimal:
        amount = validate_amount(amount)
        self._balance += amount
        self._transactions.append(Transaction(TransactionKind.DEPOSIT, amount, self._balance))
        return self._balance

    def transfer(self, amount: Decimal, recipient: str | None) -> Decimal:
        amount = validate_amount(amount)
        recipient = self._validate_recipient(recipient)
        if amount > self._balance:
            raise InsufficientFundsError("Saldo insuficiente para realizar a transferência.")
        self._balance -= amount
        self._transactions.append(
            Transaction(TransactionKind.TRANSFER, amount, self._balance, recipient)
        )
        return self._balance

    @staticmethod
    def _validate_recipient(recipient: str | None) -> str:
        if not isinstance(recipient, str) or not recipient.strip():
            raise InvalidRecipientError("Informe para quem deseja transferir (destinatário).")
        recipient = " ".join(recipient.split())
        if len(recipient) > MAX_RECIPIENT_LENGTH:
            raise InvalidRecipientError(
                f"Nome do destinatário muito longo (máximo de {MAX_RECIPIENT_LENGTH} caracteres)."
            )
        return recipient
