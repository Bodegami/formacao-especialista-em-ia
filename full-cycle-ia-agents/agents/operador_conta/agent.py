from google.adk import Agent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext


FATURAS = [
    {
        "id": "fatura_01",
        "cliente_id": "cliente_123",
        "valor": 49.99,
        "data_emissao": "2024-01-15",
        "data_vencimento": "2024-01-25",
        "status": "paga",
    },
    {
        "id": "fatura_02",
        "cliente_id": "cliente_123",
        "valor": 61.99,
        "data_emissao": "2024-02-15",
        "data_vencimento": "2024-02-25",
        "status": "pendente",
    }
]

ASSINATURAS: dict[str, dict] = {
    "cliente_123": {"plano": "Pro", "status": "ativa", "renovacao": "2026-07-01"},
}

def cancelar_assinatura(cliente_id: str, senha: str, tool_context: ToolContext) -> dict:
    """"
        Cancela a assinatura de um cliente específico.
        Args:
            cliente_id (str): O ID do cliente para o qual a assinatura deve ser cancelada.
        Returns:
            dict: Um dicionário contendo o status da operação de cancelamento.
    """

    if tool_context.tool_confirmation is None:
        tool_context.request_confirmation(
            hint="O valor da assinatura é alto. Tem certeza que deseja cancelar?",
            payload={
                "cliente_id": cliente_id,
                "senha": ""
            }
        )
        return {"status": "aguardando_confirmacao"}

    if not tool_context.tool_confirmation.confirmed:
        return {"status": "nao_cancelada", "mensagem": "Cancelando não confirmado pelo usuário."}

    if senha != "senha_secreta":
        return {"status": "nao_cancelada", "mensagem": "Senha incorreta. Cancelamento não autorizado."}

    assinatura = ASSINATURAS.get(cliente_id)
    if assinatura is not None:
        assinatura["status"] = "cancelada"
    return {"status": "cancelada", "cliente_id": cliente_id}

def listar_faturas(cliente_id: str) -> dict:
    """
        Lista as faturas de um cliente específico.
        Args:
            cliente_id (str): O ID do cliente para o qual as faturas devem ser listadas.
        Returns:
            dict: Um dicinário contendo a lista de faturas do cliente.
    """
    return {"faturas": [fatura for fatura in FATURAS if fatura["cliente_id"] == cliente_id]}

# def verificar_valor_assinatura(cliente_id: str, valor: float) -> dict:
#     return valor < 100

## In terminal, run the command: adk run folder agent name. Ex: adk run meu_agente
## Also, you can execute a command to use vie web interface. Ex: adk web agents
root_agent = Agent(
    name="operador_conta",
    instruction=""""
    Você é o atendente de conta interativo da Acme.
    Voce é o responsável por:
    - Informar ao cliente sobre sua assinatura: o plano, status e renovação.
    - Tirar dúvidas sobre faturas do cliente.
    - Cancelar a assinatura do cliente, se solicitado.
    O usuário precisa fornecer o ID do cliente para que você possa buscar as informações corretas.
    Seja cordial e direto.
    """,
    model="gemini-3.5-flash-lite",
    tools=[
        listar_faturas, 
        cancelar_assinatura
        # FunctionTool(cancelar_assinatura, require_confirmation=True)
        # FunctionTool(cancelar_assinatura, require_confirmation=verificar_valor_assinatura) # can be a boolean True or False/ but also a boolean function
    ]
)


