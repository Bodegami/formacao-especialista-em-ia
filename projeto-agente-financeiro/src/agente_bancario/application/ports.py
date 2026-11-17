"""Porta de saída (Clean Architecture): os casos de uso dependem desta interface,
não de uma implementação concreta de armazenamento."""

from typing import Protocol

from agente_bancario.domain.account import Account


class AccountRepository(Protocol):
    def get(self) -> Account:
        """Retorna a conta da sessão atual."""
        ...

    def save(self, account: Account) -> None:
        """Persiste o estado da conta."""
        ...
