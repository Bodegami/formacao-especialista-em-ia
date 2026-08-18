from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = 7
numero_ciancas = 2
atividade = "música"

prompt = f"Crie um roteiro de viagem de {numero_dias} dias, para familia com {numero_ciancas} crianças, que gosta de {atividade}."

client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Você é um assistente de viagem especializado em criar roteiros para famílias com crianças."},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)