from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm


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

def listar_faturas(cliente_id: str):
    """
        Lista as faturas de um cliente específico.
        Args:
            cliente_id (str): O ID do cliente para o qual as faturas devem ser listadas.
        Returns:
            dict: Um dicinário contendo a lista de faturas do cliente.
    """
    return {"faturas": [fatura for fatura in FATURAS if fatura["cliente_id"] == cliente_id]}

## In terminal, run the command: adk run folder agent name. Ex: adk run meu_agente
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
    tools=[listar_faturas]
)


