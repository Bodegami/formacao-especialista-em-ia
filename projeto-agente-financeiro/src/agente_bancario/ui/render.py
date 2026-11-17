"""Helpers de apresentação: geram os trechos HTML da interface (layout "neobank violeta").

Tudo que vem do usuário ou do LLM passa por `html.escape` antes de virar HTML.
Os recibos são montados a partir das transações REAIS da conta, não do texto do
modelo: o que aparece no recibo é exatamente o que aconteceu no saldo.
"""

import html
import re
from decimal import Decimal

from agente_bancario.agent.prompt import REFUSAL_MESSAGE
from agente_bancario.domain.account import Transaction, TransactionKind
from agente_bancario.domain.money import format_brl

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_REFUSAL_MARKER = "só posso ajudar"
assert _REFUSAL_MARKER in REFUSAL_MESSAGE.lower()  # mantém o marcador em sincronia com o prompt


def message_html(text: str) -> str:
    """Converte o texto do modelo em HTML seguro (escape + negrito + listas simples)."""
    lines = []
    for line in html.escape(text.strip()).splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            stripped = "• " + stripped[2:]
        lines.append(_BOLD.sub(r"<b>\1</b>", stripped))
    return "<br>".join(lines)


def is_refusal(text: str) -> bool:
    return _REFUSAL_MARKER in text.lower()


def balance_label(balance: Decimal, hidden: bool) -> str:
    return "R$ ••••••" if hidden else format_brl(balance)


def receipt_html(tx: Transaction, account_id: str) -> str:
    """Cartão de recibo exibido no chat após uma operação concluída."""
    if tx.kind is TransactionKind.TRANSFER:
        title = "Transferência enviada"
        rows = [
            ("De", f"Conta {account_id}"),
            ("Para", tx.recipient or ""),
            ("Novo saldo", format_brl(tx.balance_after)),
        ]
    else:
        title = "Depósito realizado"
        rows = [("Conta", account_id), ("Novo saldo", format_brl(tx.balance_after))]

    rows_html = "".join(
        f'<span class="rc-k">{html.escape(k)}</span><span class="rc-v">{html.escape(v)}</span>'
        for k, v in rows
    )
    return (
        '<div class="receipt">'
        f'<div class="rc-head"><span>{title}</span><span class="chip-ok">Concluída</span></div>'
        f'<div class="rc-amount">{format_brl(tx.amount)}</div>'
        f'<div class="rc-grid">{rows_html}</div>'
        "</div>"
    )


def transaction_row_html(tx: Transaction) -> str:
    """Linha de movimentação na barra lateral."""
    if tx.kind is TransactionKind.TRANSFER:
        icon, label, amount = "↗", html.escape(tx.recipient or ""), f"− {format_brl(tx.amount)}"
    else:
        icon, label, amount = "↙", "Depósito", f"+ {format_brl(tx.amount)}"
    return (
        '<div class="tx-row">'
        f'<span class="tx-label"><span class="tx-icon">{icon}</span>{label}</span>'
        f'<span class="tx-amount">{amount}</span>'
        "</div>"
    )
