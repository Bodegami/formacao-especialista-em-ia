from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = 7
numero_ciancas = 2
atividade = "praia"

prompt = f"Crie um roteiro de viagem, para um periodo de {numero_dias} dias, para familia com {numero_ciancas} crianças, que gosta de {atividade}."

modelo = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=api_key,
    temperature=0.5
)

resposta = modelo.invoke(prompt)
print(resposta.content)