"""Testes da entidade Account: regras de saldo, depósito e transferência."""

from decimal import Decimal

import pytest

from agente_bancario.domain.account import Account, TransactionKind
from agente_bancario.domain.errors import (
    InsufficientFundsError,
    InvalidAmountError,
    InvalidRecipientError,
)


def given_new_account_when_created_then_balance_is_initial_value():
    account = Account.open(initial_balance=Decimal("1000.00"))

    assert account.balance == Decimal("1000.00")


def given_account_when_deposit_then_balance_increases_exactly():
    account = Account.open(initial_balance=Decimal("1000.00"))

    account.deposit(Decimal("250.00"))

    assert account.balance == Decimal("1250.00")


def given_account_when_transfer_within_balance_then_balance_decreases_exactly():
    account = Account.open(initial_balance=Decimal("1000.00"))

    account.transfer(Decimal("100.00"), recipient="Ana")

    assert account.balance == Decimal("900.00")


def given_account_when_transfer_entire_balance_then_balance_is_zero():
    account = Account.open(initial_balance=Decimal("1000.00"))

    account.transfer(Decimal("1000.00"), recipient="Ana")

    assert account.balance == Decimal("0.00")


def given_account_when_transfer_exceeds_balance_then_raises_and_balance_unchanged():
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InsufficientFundsError):
        account.transfer(Decimal("5000.00"), recipient="Ana")

    assert account.balance == Decimal("1000.00")


def given_account_when_transfer_one_cent_over_balance_then_raises():
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InsufficientFundsError):
        account.transfer(Decimal("1000.01"), recipient="Ana")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-50")])
def given_non_positive_amount_when_deposit_then_raises_and_balance_unchanged(amount):
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InvalidAmountError):
        account.deposit(amount)

    assert account.balance == Decimal("1000.00")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-50")])
def given_non_positive_amount_when_transfer_then_raises(amount):
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InvalidAmountError):
        account.transfer(amount, recipient="Ana")


def given_amount_with_fraction_of_cent_when_deposit_then_raises():
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("0.001"))


@pytest.mark.parametrize("recipient", ["", "   ", None])
def given_blank_recipient_when_transfer_then_raises_and_balance_unchanged(recipient):
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InvalidRecipientError):
        account.transfer(Decimal("100.00"), recipient=recipient)

    assert account.balance == Decimal("1000.00")


def given_too_long_recipient_when_transfer_then_raises():
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InvalidRecipientError):
        account.transfer(Decimal("100.00"), recipient="A" * 81)


def given_sequence_of_operations_when_applied_then_balance_is_exact():
    # Sequência clássica que quebraria com float: 0.1 + 0.2 - 0.3
    account = Account.open(initial_balance=Decimal("1000.00"))

    account.deposit(Decimal("0.10"))
    account.deposit(Decimal("0.20"))
    account.transfer(Decimal("0.30"), recipient="Ana")
    account.deposit(Decimal("250.00"))
    account.transfer(Decimal("100.00"), recipient="Ana")

    assert account.balance == Decimal("1150.00")


def given_operations_when_applied_then_transactions_are_recorded_in_order():
    account = Account.open(initial_balance=Decimal("1000.00"))

    account.deposit(Decimal("250.00"))
    account.transfer(Decimal("100.00"), recipient="Ana")

    kinds = [t.kind for t in account.transactions]
    assert kinds == [TransactionKind.DEPOSIT, TransactionKind.TRANSFER]
    assert account.transactions[-1].balance_after == Decimal("1150.00")
    assert account.transactions[-1].recipient == "Ana"


def given_failed_operation_when_applied_then_no_transaction_is_recorded():
    account = Account.open(initial_balance=Decimal("1000.00"))

    with pytest.raises(InsufficientFundsError):
        account.transfer(Decimal("5000.00"), recipient="Ana")

    assert account.transactions == ()
