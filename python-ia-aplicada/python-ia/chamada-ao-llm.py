from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key ="lm-studio" 
)

resposta_do_modelo = client.chat.completions.create(
    model="google/gemma-3-4b",
    messages=[
        {"role": "system", "content": "Você é um assistente de IA prestativo, mas que response sempre de forma sarcástica."},
        {"role": "user", "content": "O que é a IA Generativa?"}
    ],
    temperature=1.0,
)


print(resposta_do_modelo)
print("*" * 50)
print(resposta_do_modelo.choices[0].message.content)