"""Testes da conversão/validação de valores monetários (camada de domínio)."""

from decimal import Decimal

import pytest

from agente_bancario.domain.errors import InvalidAmountError
from agente_bancario.domain.money import format_brl, parse_amount


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("250", Decimal("250.00")),
        ("250.5", Decimal("250.50")),
        ("250.55", Decimal("250.55")),
        ("250,55", Decimal("250.55")),
        ("  100  ", Decimal("100.00")),
        ("R$ 100", Decimal("100.00")),
        ("0.01", Decimal("0.01")),
        (250, Decimal("250.00")),
        (Decimal("10.5"), Decimal("10.50")),
    ],
)
def given_valid_amount_when_parsed_then_returns_exact_decimal_in_cents(raw, expected):
    # Given / When
    result = parse_amount(raw)

    # Then
    assert result == expected
    assert result.as_tuple().exponent == -2


@pytest.mark.parametrize("raw", ["-50", "-0.01", -50])
def given_negative_amount_when_parsed_then_raises_must_be_positive(raw):
    with pytest.raises(InvalidAmountError, match="maior que zero"):
        parse_amount(raw)


@pytest.mark.parametrize("raw", ["0", "0.00", "0,00", 0])
def given_zero_amount_when_parsed_then_raises_must_be_positive(raw):
    with pytest.raises(InvalidAmountError, match="maior que zero"):
        parse_amount(raw)


@pytest.mark.parametrize(
    "raw", ["abc", "", "   ", "cem", "1e3", "NaN", "Infinity", "10..5", "1,2,3", None, True, [100]]
)
def given_non_numeric_amount_when_parsed_then_raises_not_numeric(raw):
    with pytest.raises(InvalidAmountError, match="numérico"):
        parse_amount(raw)


@pytest.mark.parametrize("raw", ["0.001", "10.5555", "1,2345"])
def given_more_than_two_decimal_places_when_parsed_then_raises_cents_error(raw):
    with pytest.raises(InvalidAmountError, match="centavos"):
        parse_amount(raw)


@pytest.mark.parametrize("raw", ["1.000,50", "1,000.50", "1.000", "10.555", "10,555", "1.000.000"])
def given_possible_thousand_separator_when_parsed_then_raises_ambiguous_format(raw):
    # "1.000" pode ser mil (pt-BR) ou um (en-US) → o sistema recusa e pede o valor
    # sem separador de milhar, em vez de adivinhar.
    with pytest.raises(InvalidAmountError, match="ambíguo"):
        parse_amount(raw)


def given_float_with_binary_noise_when_parsed_then_uses_shortest_repr():
    # 0.1 + 0.2 em float é 0.30000000000000004 → mais de 2 casas → recusado
    with pytest.raises(InvalidAmountError):
        parse_amount(0.1 + 0.2)


def given_simple_float_when_parsed_then_converts_exactly():
    assert parse_amount(250.5) == Decimal("250.50")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("1000"), "R$ 1.000,00"),
        (Decimal("1250.5"), "R$ 1.250,50"),
        (Decimal("0.01"), "R$ 0,01"),
        (Decimal("1234567.89"), "R$ 1.234.567,89"),
        (Decimal("0"), "R$ 0,00"),
    ],
)
def given_decimal_when_formatted_then_returns_brazilian_currency(value, expected):
    assert format_brl(value) == expected


def given_absurdly_large_amount_when_parsed_then_raises_instead_of_crashing():
    with pytest.raises(InvalidAmountError):
        parse_amount("9" * 40)
