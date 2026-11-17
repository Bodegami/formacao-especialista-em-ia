"""Erros de domínio.

Toda violação de regra de negócio vira uma exceção tipada. A camada de
ferramentas converte essas exceções em mensagens "ERRO: ..." para o LLM,
que apenas repassa o motivo ao usuário — ele nunca decide se a operação é válida.
"""


class DomainError(Exception):
    """Base para erros de regra de negócio. `message` é seguro para exibir ao usuário."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidAmountError(DomainError):
    """Valor não numérico, não positivo, com frações de centavo ou em formato ambíguo."""


class InsufficientFundsError(DomainError):
    """Transferência maior que o saldo disponível (impede saldo negativo)."""


class InvalidRecipientError(DomainError):
    """Destinatário da transferência ausente ou inválido."""
