"""Testes dos casos de uso, usando o repositório em memória (sem LLM, sem rede)."""

from decimal import Decimal

import pytest

from agente_bancario.application.use_cases import (
    DepositUseCase,
    GetBalanceUseCase,
    TransferUseCase,
)
from agente_bancario.domain.errors import InsufficientFundsError, InvalidAmountError
from agente_bancario.infrastructure.in_memory_repository import InMemoryAccountRepository


def _repo() -> InMemoryAccountRepository:
    return InMemoryAccountRepository(initial_balance=Decimal("1000.00"))


def given_new_session_when_get_balance_then_returns_initial_balance():
    result = GetBalanceUseCase(_repo()).execute()

    assert result.balance == Decimal("1000.00")


def given_valid_raw_amount_when_deposit_then_persists_new_balance():
    repo = _repo()

    result = DepositUseCase(repo).execute("250")

    assert result.amount == Decimal("250.00")
    assert result.new_balance == Decimal("1250.00")
    assert GetBalanceUseCase(repo).execute().balance == Decimal("1250.00")


def given_negative_raw_amount_when_deposit_then_raises_and_balance_unchanged():
    repo = _repo()

    with pytest.raises(InvalidAmountError):
        DepositUseCase(repo).execute("-50")

    assert GetBalanceUseCase(repo).execute().balance == Decimal("1000.00")


def given_valid_transfer_when_executed_then_returns_origin_amount_recipient_and_balance():
    repo = _repo()

    result = TransferUseCase(repo).execute("100", "Ana")

    assert result.amount == Decimal("100.00")
    assert result.recipient == "Ana"
    assert result.origin == repo.get().account_id
    assert result.new_balance == Decimal("900.00")


def given_transfer_above_balance_when_executed_then_raises_and_balance_unchanged():
    repo = _repo()

    with pytest.raises(InsufficientFundsError):
        TransferUseCase(repo).execute("5000", "Ana")

    assert GetBalanceUseCase(repo).execute().balance == Decimal("1000.00")


def given_two_repositories_when_one_changes_then_other_is_isolated():
    # Cada sessão tem seu próprio repositório: não há estado global compartilhado.
    repo_a, repo_b = _repo(), _repo()

    DepositUseCase(repo_a).execute("100")

    assert GetBalanceUseCase(repo_b).execute().balance == Decimal("1000.00")
