"""Repositório em memória: uma instância por sessão de usuário.

Na interface Streamlit, a instância fica em `st.session_state`, então o saldo
persiste entre mensagens da mesma sessão e é isolado entre sessões diferentes.
Trocar por SQLite/Redis exigiria apenas outra classe com `get`/`save`.
"""

from decimal import Decimal

from agente_bancario.domain.account import Account


class InMemoryAccountRepository:
    def __init__(self, initial_balance: Decimal, account_id: str = "0001-9") -> None:
        self._account = Account.open(initial_balance=initial_balance, account_id=account_id)

    def get(self) -> Account:
        return self._account

    def save(self, account: Account) -> None:
        self._account = account
