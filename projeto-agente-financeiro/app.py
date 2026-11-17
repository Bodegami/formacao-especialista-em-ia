"""Interface Streamlit do Agente Bancário Restrito (layout "neobank violeta").

Execute com:  uv run streamlit run app.py

Persistência: o repositório e o agente ficam em `st.session_state`, ou seja,
o saldo é mantido entre mensagens da mesma sessão (aba do navegador) e cada
sessão começa com R$ 1.000,00.

O saldo da barra lateral e os recibos no chat são lidos DIRETO da conta (não do
texto do LLM). Eles servem de auditoria visual: se o agente dissesse um valor
diferente, a divergência ficaria evidente.
"""

import html
from decimal import Decimal
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agente_bancario.agent.bank_agent import BankAgent, create_gemini_model
from agente_bancario.infrastructure.in_memory_repository import InMemoryAccountRepository
from agente_bancario.ui.render import (
    balance_label,
    is_refusal,
    message_html,
    receipt_html,
    transaction_row_html,
)

INITIAL_BALANCE = Decimal("1000.00")
STYLES = Path(__file__).parent / "src" / "agente_bancario" / "ui" / "styles.css"
QUICK_ACTIONS = [
    ("Ver saldo", ":material/account_balance_wallet:", "Qual meu saldo?"),
    ("Depositar", ":material/add:", "Quero fazer um depósito"),
    ("Transferir", ":material/swap_horiz:", "Quero fazer uma transferência"),
]
WELCOME = (
    "Olá! Sou o assistente da sua conta. Posso <b>consultar seu saldo</b>, "
    "<b>fazer depósitos</b> e <b>transferências</b>. Como posso ajudar?"
)

load_dotenv()
st.set_page_config(page_title="Agente Bancário", page_icon=":material/account_balance:", layout="wide")
st.html(f"<style>{STYLES.read_text(encoding='utf-8')}</style>")


# ---------------------------------------------------------------- estado da sessão
def start_session() -> None:
    repository = InMemoryAccountRepository(initial_balance=INITIAL_BALANCE)
    st.session_state.repository = repository
    st.session_state.agent = BankAgent(model=create_gemini_model(), repository=repository)
    # Mensagens apenas para exibição: {"role", "text", "kind", "receipts", "tools"}
    st.session_state.messages = []
    st.session_state.hide_balance = False


def queue_prompt(text: str) -> None:
    st.session_state.pending_prompt = text


def toggle_balance() -> None:
    st.session_state.hide_balance = not st.session_state.hide_balance


if "agent" not in st.session_state:
    try:
        start_session()
    except RuntimeError as exc:  # chave de API ausente
        st.error(str(exc))
        st.stop()

repository: InMemoryAccountRepository = st.session_state.repository
agent: BankAgent = st.session_state.agent
account = repository.get()


# ---------------------------------------------------------------- barra lateral
with st.sidebar:
    st.html(
        '<div class="brand"><span class="brand-mark">◆</span>'
        f"Conta {html.escape(account.account_id)}</div>"
        '<div class="balance-card">'
        '<div class="balance-label">Saldo disponível</div>'
        f'<div class="balance-value">{balance_label(account.balance, st.session_state.hide_balance)}</div>'
        f'<div class="balance-sub">Saldo inicial R$ 1.000,00 · {len(account.transactions)} operação(ões)</div>'
        "</div>"
    )
    with st.container(key="side_actions", horizontal=True):
        hidden = st.session_state.hide_balance
        st.button(
            "Mostrar" if hidden else "Ocultar",
            icon=":material/visibility:" if hidden else ":material/visibility_off:",
            on_click=toggle_balance,
        )
        if st.button("Reiniciar", icon=":material/restart_alt:", help="Volta o saldo para R$ 1.000,00"):
            start_session()
            st.rerun()

    rows = "".join(transaction_row_html(tx) for tx in reversed(account.transactions[-8:]))
    st.html(
        '<div class="side-title">Últimas movimentações</div>'
        + (rows or '<div class="tx-empty">Nenhuma movimentação nesta sessão.</div>')
        + '<div class="shield">🛡 Operações validadas pelo sistema, não pelo modelo.</div>'
    )


# ---------------------------------------------------------------- área principal
st.html(
    '<p class="page-title">Assistente da conta</p>'
    '<p class="page-sub">Converse em linguagem natural ou use um atalho.</p>'
)
with st.container(key="quick", horizontal=True):
    for label, icon, prompt_text in QUICK_ACTIONS:
        st.button(label, icon=icon, on_click=queue_prompt, args=(prompt_text,))


def render_user(text: str) -> None:
    st.html(f'<div class="msg-user"><div class="bubble">{html.escape(text)}</div></div>')


def render_bot(msg: dict) -> None:
    parts = []
    if msg.get("text"):
        css = {"refusal": "bubble refusal", "error": "bubble error"}.get(msg.get("kind"), "bubble")
        parts.append(f'<div class="{css}">{msg["text"]}</div>')
    parts.extend(msg.get("receipts", []))
    if msg.get("tools"):
        parts.append(f'<div class="tools">🔧 ferramentas: {html.escape(", ".join(msg["tools"]))}</div>')
    st.html(f'<div class="msg-bot"><div class="avatar">✦</div><div class="bot-col">{"".join(parts)}</div></div>')


render_bot({"text": WELCOME})
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_user(msg["text"])
    else:
        render_bot(msg)


# ---------------------------------------------------------------- nova mensagem
typed = st.chat_input("Ex.: transferir 50 para o João")
prompt = typed or st.session_state.pop("pending_prompt", None)

if prompt:
    render_user(prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})

    tx_before = len(account.transactions)
    with st.spinner("Processando..."):
        reply = agent.chat(prompt)
    new_transactions = repository.get().transactions[tx_before:]
    receipts = [receipt_html(tx, account.account_id) for tx in new_transactions]

    # Recibo (dado real) substitui o texto quando tudo deu certo; havendo erro
    # ou nenhuma operação, mostramos o texto do agente.
    show_text = not receipts or agent.last_tool_errors
    kind = "error" if agent.last_tool_errors else "refusal" if is_refusal(reply) else "normal"
    st.session_state.messages.append(
        {
            "role": "assistant",
            "text": message_html(reply) if show_text else "",
            "kind": kind,
            "receipts": receipts,
            "tools": list(agent.last_tool_calls),
        }
    )
    st.rerun()  # redesenha tudo (inclusive o saldo da barra lateral) com o estado novo
