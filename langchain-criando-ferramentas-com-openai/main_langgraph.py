from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

modelo = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=api_key,
    temperature=0.5
)

prompt_consultor = ChatPromptTemplate.from_messages([
    ("system", "Você é um consultor de viagens"),
    ("human", "{query}")
])

assistente = prompt_consultor | modelo | StrOutputParser()

response = assistente.invoke(
    {
        "query": "Quero férias em praias no Brasil."
    }
)

print(response)
