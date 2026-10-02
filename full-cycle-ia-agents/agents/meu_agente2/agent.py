from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

## In terminal, run the command: adk run folder agent name. Ex: adk run meu_agente
root_agent = Agent(
    name="meu_agente2",
    instruction=""""
    You are a specialist in Python programming.
    """,
    #model="gemini-3.5-flash-lite",
    model=LiteLlm(model="anthropic/claude-sonnet-4-6")
)


