from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = 7
numero_ciancas = 2
atividade = "praia"

modelo_de_prompt = PromptTemplate(
    template="""
    Crie um roteiro de viagem, para um periodo de {dias} dias, 
    para familia com {criancas} crianças, que gosta de {atividade}.
    """,
)

prompt = modelo_de_prompt.format(
    dias=numero_dias,
    criancas=numero_ciancas,
    atividade=atividade
)

print("Prompt gerado: \n", prompt)

modelo = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=api_key,
    temperature=0.5
)

resposta = modelo.invoke(prompt)
print(resposta.content)