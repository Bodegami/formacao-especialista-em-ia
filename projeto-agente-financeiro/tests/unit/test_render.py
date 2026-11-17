"""Testes dos helpers de apresentação (HTML da interface)."""

from decimal import Decimal

from agente_bancario.domain.account import Transaction, TransactionKind
from agente_bancario.ui.render import (
    balance_label,
    is_refusal,
    message_html,
    receipt_html,
    transaction_row_html,
)


def given_text_with_html_when_rendered_then_html_is_escaped():
    result = message_html("<script>alert(1)</script>")

    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def given_markdown_bold_when_rendered_then_becomes_bold_tag():
    assert "<b>Valor:</b>" in message_html("**Valor:** R$ 100,00")


def given_markdown_list_when_rendered_then_lines_become_bullets_with_breaks():
    result = message_html("Feito\n- item 1\n* item 2")

    assert result == "Feito<br>• item 1<br>• item 2"


def given_refusal_message_when_checked_then_is_refusal():
    assert is_refusal("Desculpe, só posso ajudar com as operações da sua conta: ...")


def given_normal_message_when_checked_then_is_not_refusal():
    assert not is_refusal("Seu saldo é R$ 1.000,00.")


def given_hidden_flag_when_balance_label_then_masks_value():
    assert "1.000" not in balance_label(Decimal("1000.00"), hidden=True)


def given_visible_flag_when_balance_label_then_shows_formatted_value():
    assert balance_label(Decimal("1000.00"), hidden=False) == "R$ 1.000,00"


def given_transfer_when_receipt_rendered_then_shows_origin_recipient_amount_and_balance():
    tx = Transaction(TransactionKind.TRANSFER, Decimal("100.00"), Decimal("900.00"), "Ana")

    result = receipt_html(tx, account_id="0001-9")

    for expected in ("Transferência enviada", "R$ 100,00", "0001-9", "Ana", "R$ 900,00"):
        assert expected in result


def given_deposit_when_receipt_rendered_then_shows_amount_and_balance():
    tx = Transaction(TransactionKind.DEPOSIT, Decimal("250.00"), Decimal("1250.00"))

    result = receipt_html(tx, account_id="0001-9")

    assert "Depósito realizado" in result
    assert "R$ 250,00" in result
    assert "R$ 1.250,00" in result


def given_recipient_with_html_when_rendered_then_is_escaped():
    tx = Transaction(TransactionKind.TRANSFER, Decimal("1.00"), Decimal("999.00"), "<b>x</b>")

    assert "<b>x</b>" not in receipt_html(tx, account_id="0001-9")
    assert "<b>x</b>" not in transaction_row_html(tx)


def given_transfer_when_row_rendered_then_shows_negative_amount():
    tx = Transaction(TransactionKind.TRANSFER, Decimal("100.00"), Decimal("900.00"), "Ana")

    assert "− R$ 100,00" in transaction_row_html(tx)


def given_deposit_when_row_rendered_then_shows_positive_amount():
    tx = Transaction(TransactionKind.DEPOSIT, Decimal("250.00"), Decimal("1250.00"))

    assert "+ R$ 250,00" in transaction_row_html(tx)
