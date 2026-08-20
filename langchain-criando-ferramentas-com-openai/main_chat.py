import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

modelo = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=api_key,
    temperature=0.5
)

perguntas = [
    "Quero visitar um lugar do Brasil, famoso por praias e cultura. Pode sugerir?",
    "Qual a melhor época do ano para visitar esse lugar??"
]

for pergunta in perguntas:
    resposta = modelo.invoke(pergunta)
    print(f"Usuário: {pergunta}")
    print(f"IA: {resposta}")
    print("-" * 50)