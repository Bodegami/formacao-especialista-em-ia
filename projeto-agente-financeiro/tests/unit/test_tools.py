"""Testes das ferramentas LangChain (adaptador entre o LLM e os casos de uso).

As ferramentas são chamadas diretamente, sem LLM: o objetivo é provar que a
validação está no código e não depende do prompt.
"""

from decimal import Decimal

from agente_bancario.agent.tools import TurnGuard, build_tools
from agente_bancario.infrastructure.in_memory_repository import InMemoryAccountRepository


def _setup():
    repo = InMemoryAccountRepository(initial_balance=Decimal("1000.00"))
    guard = TurnGuard()
    tools = {t.name: t for t in build_tools(repo, guard)}
    return repo, guard, tools


def given_tools_when_built_then_exposes_exactly_three_operations():
    _, _, tools = _setup()

    assert set(tools) == {"consultar_saldo", "depositar", "transferir"}


def given_new_account_when_consultar_saldo_then_returns_formatted_balance():
    _, _, tools = _setup()

    result = tools["consultar_saldo"].invoke({})

    assert result.startswith("OK")
    assert "R$ 1.000,00" in result


def given_valid_amount_when_depositar_then_confirms_amount_and_new_balance():
    repo, _, tools = _setup()

    result = tools["depositar"].invoke({"valor": "250"})

    assert result.startswith("OK")
    assert "R$ 250,00" in result
    assert "R$ 1.250,00" in result
    assert repo.get().balance == Decimal("1250.00")


def given_negative_amount_when_depositar_then_returns_error_and_keeps_balance():
    repo, _, tools = _setup()

    result = tools["depositar"].invoke({"valor": "-50"})

    assert result.startswith("ERRO")
    assert repo.get().balance == Decimal("1000.00")


def given_text_amount_when_depositar_then_returns_error():
    repo, _, tools = _setup()

    result = tools["depositar"].invoke({"valor": "muito dinheiro"})

    assert result.startswith("ERRO")
    assert repo.get().balance == Decimal("1000.00")


def given_valid_transfer_when_transferir_then_confirms_origin_amount_recipient_balance():
    repo, _, tools = _setup()

    result = tools["transferir"].invoke({"valor": "100", "destinatario": "Ana"})

    assert result.startswith("OK")
    assert repo.get().account_id in result
    assert "R$ 100,00" in result
    assert "Ana" in result
    assert "R$ 900,00" in result


def given_insufficient_balance_when_transferir_then_returns_error_with_current_balance():
    repo, _, tools = _setup()

    result = tools["transferir"].invoke({"valor": "5000", "destinatario": "Ana"})

    assert result.startswith("ERRO")
    assert "insuficiente" in result
    assert "R$ 1.000,00" in result
    assert repo.get().balance == Decimal("1000.00")


def given_blank_recipient_when_transferir_then_returns_error():
    repo, _, tools = _setup()

    result = tools["transferir"].invoke({"valor": "100", "destinatario": "  "})

    assert result.startswith("ERRO")
    assert repo.get().balance == Decimal("1000.00")


def given_identical_deposit_twice_in_same_turn_when_called_then_second_is_blocked():
    # Proteção contra o modelo repetir a mesma chamada por engano.
    repo, _, tools = _setup()

    tools["depositar"].invoke({"valor": "100"})
    second = tools["depositar"].invoke({"valor": "100"})

    assert second.startswith("ERRO")
    assert repo.get().balance == Decimal("1100.00")


def given_identical_transfer_twice_in_same_turn_when_called_then_second_is_blocked():
    repo, _, tools = _setup()

    tools["transferir"].invoke({"valor": "100", "destinatario": "Ana"})
    second = tools["transferir"].invoke({"valor": "100", "destinatario": "ana"})

    assert second.startswith("ERRO")
    assert repo.get().balance == Decimal("900.00")


def given_identical_deposit_in_new_turn_when_called_then_is_allowed():
    repo, guard, tools = _setup()

    tools["depositar"].invoke({"valor": "100"})
    guard.reset()
    second = tools["depositar"].invoke({"valor": "100"})

    assert second.startswith("OK")
    assert repo.get().balance == Decimal("1200.00")


def given_failed_operation_when_retried_with_valid_value_in_same_turn_then_is_allowed():
    repo, _, tools = _setup()

    tools["depositar"].invoke({"valor": "-100"})
    second = tools["depositar"].invoke({"valor": "100"})

    assert second.startswith("OK")
    assert repo.get().balance == Decimal("1100.00")
