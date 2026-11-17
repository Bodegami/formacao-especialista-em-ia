"""Orquestração do agente: LLM (Gemini via LangChain) + ferramentas + memória da sessão.

Fluxo de uma mensagem:
    1. Guardas determinísticas (mensagem vazia / longa demais) → resposta fixa, sem LLM.
    2. Reset do TurnGuard (anti-duplicidade por turno).
    3. LangChain `create_agent` executa o loop modelo ↔ ferramentas (ReAct).
    4. O histórico da conversa é guardado para dar contexto às próximas mensagens.
       O SALDO não depende desse histórico: ele vive no repositório.
"""

import logging
import os
from typing import Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage

from agente_bancario.agent.prompt import REFUSAL_MESSAGE, SYSTEM_PROMPT
from agente_bancario.agent.tools import TurnGuard, build_tools
from agente_bancario.application.ports import AccountRepository

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.8-flash"
MAX_INPUT_CHARS = 1000
# Cada ida e volta modelo→ferramenta consome ~2 passos. 12 permite algumas operações
# encadeadas numa mesma mensagem e impede loops infinitos.
RECURSION_LIMIT = 12

_EMPTY_INPUT_REPLY = (
    "Olá! Posso ajudar com: consultar saldo, depositar ou transferir. O que deseja fazer?"
)
_TOO_LONG_REPLY = (
    f"Sua mensagem é muito longa (limite de {MAX_INPUT_CHARS} caracteres). "
    "Envie um pedido curto: consultar saldo, depositar ou transferir."
)
_FAILURE_REPLY = (
    "Desculpe, ocorreu uma falha técnica ao processar seu pedido. "
    "Peça para consultar o saldo e confirmar se alguma operação foi concluída antes de tentar de novo."
)


def create_gemini_model(model_name: str | None = None) -> BaseChatModel:
    """Cria o modelo Gemini com temperatura 0 (respostas determinísticas)."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY no ambiente ou no arquivo .env.")
    return ChatGoogleGenerativeAI(
        model=model_name or os.environ.get("GEMINI_MODEL", DEFAULT_MODEL),
        google_api_key=api_key,
        temperature=0,
        max_retries=2,
    )


class BankAgent:
    """Um agente por sessão de usuário (cada um com seu repositório e histórico)."""

    def __init__(self, model: BaseChatModel | Any, repository: AccountRepository) -> None:
        self._model = model
        self._guard = TurnGuard()
        self._tools = build_tools(repository, self._guard)
        self._graph = None  # criado sob demanda: guardas não precisam do modelo
        self.history: list[AnyMessage] = []
        self.last_tool_calls: list[str] = []
        self.last_tool_errors = False  # alguma ferramenta retornou "ERRO:" no último turno

    def chat(self, user_message: str) -> str:
        self.last_tool_calls = []
        self.last_tool_errors = False
        text = (user_message or "").strip()
        if not text:
            return _EMPTY_INPUT_REPLY
        if len(text) > MAX_INPUT_CHARS:
            return _TOO_LONG_REPLY

        self._guard.reset()
        turn_start = len(self.history)
        try:
            result = self._get_graph().invoke(
                {"messages": [*self.history, HumanMessage(text)]},
                config={"recursion_limit": RECURSION_LIMIT},
            )
        except Exception:  # noqa: BLE001 - falha de rede/API/limite: resposta segura
            logger.exception("Falha ao processar mensagem no agente")
            return _FAILURE_REPLY

        messages: list[AnyMessage] = result["messages"]
        self.history = messages
        new_messages = messages[turn_start:]
        tool_messages = [m for m in new_messages if isinstance(m, ToolMessage)]
        self.last_tool_calls = [m.name or "" for m in tool_messages]
        self.last_tool_errors = any(str(m.content).startswith("ERRO") for m in tool_messages)
        return _final_text(new_messages)

    def _get_graph(self):
        if self._graph is None:
            self._graph = create_agent(
                model=self._model, tools=self._tools, system_prompt=SYSTEM_PROMPT
            )
        return self._graph


def _final_text(messages: list[AnyMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            text = message.text if isinstance(message.text, str) else message.text()
            if text.strip():
                return text.strip()
    # O modelo terminou sem texto: nunca devolver resposta vazia nem inventada.
    return REFUSAL_MESSAGE
