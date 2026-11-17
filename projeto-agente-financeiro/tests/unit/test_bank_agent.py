"""Testes das proteções determinísticas do BankAgent (executadas ANTES do LLM).

Usa um modelo falso que falha se for chamado: prova que essas entradas nunca
chegam ao modelo.
"""

from decimal import Decimal

from agente_bancario.agent.bank_agent import MAX_INPUT_CHARS, BankAgent
from agente_bancario.infrastructure.in_memory_repository import InMemoryAccountRepository


class ExplodingModel:
    """Dublê: qualquer uso do modelo é um erro de teste."""

    def __getattr__(self, name):
        raise AssertionError(f"O modelo não deveria ser usado (acessou {name!r}).")


def _agent() -> BankAgent:
    repo = InMemoryAccountRepository(initial_balance=Decimal("1000.00"))
    return BankAgent(model=ExplodingModel(), repository=repo)


def given_empty_message_when_chat_then_asks_for_operation_without_calling_model():
    reply = _agent().chat("   ")

    assert "consultar saldo" in reply.lower()


def given_message_over_limit_when_chat_then_refuses_without_calling_model():
    reply = _agent().chat("a" * (MAX_INPUT_CHARS + 1))

    assert "muito longa" in reply.lower()


def given_refused_input_when_chat_then_history_is_not_polluted():
    agent = _agent()

    agent.chat("a" * (MAX_INPUT_CHARS + 1))

    assert agent.history == []
