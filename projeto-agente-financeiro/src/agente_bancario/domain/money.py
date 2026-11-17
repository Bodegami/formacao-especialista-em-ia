"""Representação e validação de dinheiro.

Decisões:
- Todo valor é `Decimal` com exatamente 2 casas (centavos). `float` nunca é usado
  em cálculos, porque 0.1 + 0.2 != 0.3 em ponto flutuante.
- A conversão de texto é ESTRITA: aceitamos "250", "250.50" ou "250,50".
  Qualquer separador seguido de exatamente 3 dígitos ("1.000", "10,555") é
  ambíguo entre formato brasileiro e americano, então é recusado em vez de adivinhado.
- Nenhum arredondamento silencioso: "10.5555" é recusado, não vira 10.56.
"""

import math
import re
from decimal import Decimal, InvalidOperation

from agente_bancario.domain.errors import InvalidAmountError

CENTS = Decimal("0.01")
MAX_INTEGER_DIGITS = 13  # limite técnico (trilhões), protege a precisão do Decimal

# Número simples: sinal opcional, dígitos, e opcionalmente UM separador decimal.
_SIMPLE_NUMBER = re.compile(r"^-?\d+(?:[.,]\d+)?$")
# Qualquer separador seguido de exatamente 3 dígitos pode ser separador de milhar.
_POSSIBLE_THOUSANDS = re.compile(r"^-?[1-9]\d{0,2}(?:[.,]\d{3})+(?:[.,]\d+)?$")

_NOT_NUMERIC = "O valor informado não é numérico. Informe apenas números, por exemplo: 250 ou 250,50."
_NOT_POSITIVE = "O valor deve ser maior que zero."
_TOO_MANY_DECIMALS = "O valor não pode ter frações de centavos (máximo de 2 casas decimais)."
_TOO_LARGE = "O valor informado excede o limite técnico suportado pelo sistema."
_AMBIGUOUS = (
    "O formato do valor é ambíguo (pode conter separador de milhar). "
    "Informe o valor sem separador de milhar, por exemplo: 1000 ou 1000,50."
)


def parse_amount(raw: object) -> Decimal:
    """Converte uma entrada bruta em Decimal com 2 casas, ou lança InvalidAmountError."""
    value = _to_decimal(raw)
    return validate_amount(value)


def validate_amount(value: Decimal) -> Decimal:
    """Garante que o valor é finito, positivo e sem frações de centavo."""
    if not isinstance(value, Decimal) or not value.is_finite():
        raise InvalidAmountError(_NOT_NUMERIC)
    # adjusted() = posição do dígito mais significativo; evita estourar a precisão do Decimal.
    if value.adjusted() >= MAX_INTEGER_DIGITS:
        raise InvalidAmountError(_TOO_LARGE)
    if value != value.quantize(CENTS):
        raise InvalidAmountError(_TOO_MANY_DECIMALS)
    if value <= 0:
        raise InvalidAmountError(_NOT_POSITIVE)
    return value.quantize(CENTS)


def format_brl(value: Decimal) -> str:
    """Formata em Real brasileiro: Decimal('1250.5') -> 'R$ 1.250,50'."""
    us_format = f"{value.quantize(CENTS):,.2f}"  # "1,250.50"
    return "R$ " + us_format.replace(",", "_").replace(".", ",").replace("_", ".")


def _to_decimal(raw: object) -> Decimal:
    # bool é subclasse de int em Python: precisa ser recusado explicitamente.
    if isinstance(raw, bool) or raw is None:
        raise InvalidAmountError(_NOT_NUMERIC)
    if isinstance(raw, Decimal):
        return raw
    if isinstance(raw, int):
        return Decimal(raw)
    if isinstance(raw, float):
        if not math.isfinite(raw):
            raise InvalidAmountError(_NOT_NUMERIC)
        # repr() dá a menor representação exata do float (250.5 -> "250.5").
        return Decimal(repr(raw))
    if isinstance(raw, str):
        return _parse_text(raw)
    raise InvalidAmountError(_NOT_NUMERIC)


def _parse_text(text: str) -> Decimal:
    cleaned = text.strip().removeprefix("R$").strip().replace(" ", "")
    if _POSSIBLE_THOUSANDS.match(cleaned):
        raise InvalidAmountError(_AMBIGUOUS)
    if not _SIMPLE_NUMBER.match(cleaned):
        raise InvalidAmountError(_NOT_NUMERIC)
    try:
        return Decimal(cleaned.replace(",", "."))
    except InvalidOperation as exc:  # defensivo: a regex já garante o formato
        raise InvalidAmountError(_NOT_NUMERIC) from exc
