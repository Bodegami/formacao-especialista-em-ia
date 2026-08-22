from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, Literal
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

modelo = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=api_key,
    temperature=0.5
)

prompt_consultor_praia = ChatPromptTemplate.from_messages([
    ("system", "Apresente-se como Sra Praia. Você é uma especialista em viagens com destinos para praias."),
    ("human", "{query}")
])

prompt_consultor_montanha = ChatPromptTemplate.from_messages([
    ("system", "Apresente-se como Sra Montanha. Você é uma especialista em viagens com destinos para montanhas e atividades radicais."),
    ("human", "{query}")
])

cadeia_praia = prompt_consultor_praia | modelo | StrOutputParser()
cadeia_montanha = prompt_consultor_montanha | modelo | StrOutputParser()

# O TypedDict é usado para definir a estrutura de dados esperada para a rota, 
# Usando o Literal, garantindo que o destino seja apenas "praia" ou "montanha".
class Rota(TypedDict):
    destino: Literal["praia", "montanha"]

prompt_roteador = ChatPromptTemplate.from_messages([
    ("system", "Responda apenas com 'praia' ou 'montanha' para indicar o tipo de destino que o usuário deseja."),
    ("human", "{query}")
])

roteador = prompt_roteador | modelo.with_structured_output(Rota) 

def response(pergunta: str):
    rota = roteador.invoke({"query": pergunta})["destino"]
    print(rota)
    if rota == "praia":
        return cadeia_praia.invoke({"query": pergunta})
    elif rota == "montanha":
        return cadeia_montanha.invoke({"query": pergunta})
    else:
        return "Desculpe, não consegui identificar o tipo de destino desejado. Por favor, tente novamente."

print(response("Quero surfar em um lugar quente."))
