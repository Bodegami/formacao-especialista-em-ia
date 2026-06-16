from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key ="lm-studio" 
)

def recebe_linha_e_retorna_json(linha):
    resposta_do_modelo = client.chat.completions.create(
        model="google/gemma-3-4b",
        messages=[
            {"role": "system", "content": """Você é um especialista em analise de dados e conversão de dados para JSON.
                Você receberá uma linha de textp que é uma resenha de um aplicativo de marketplace online.
                Eu quero que você analise essa resenha, e me retorne um JSON com as seguintes chaves: 
                - 'usuario': o nome do usuario que fez a resenha
                - 'resenha_original': a resenha no idioma original que você recebeu
                - 'resenha_pt': a resenha traduzida para o português
                - 'avaliacao': uma avaliação se essa resenha foi 'Positiva', 'Negativa' ou 'Neutra' (apenas uma dessas três palavras)
                
                Exemplo de entrada:
                '8765234590$Pedro Silva$This app is amazing! I love it!'

                Exemplo de saída:
                {
                    "usuario": "Pedro Silva",
                    "resenha_original": "This app is amazing! I love it!",
                    "resenha_pt": "Este aplicativo é incrível! Eu adoro!",
                    "avaliacao": "Positiva"
                }
                
                Regra importante: Você deve retornar apenas o JSON como no exemplo acima, sem nenhum texto adicional.
                """},

            {"role": "user", 
             "content": f"Resenha: {linha}"}
        ],
        temperature=1.0,
    )

    response = resposta_do_modelo.choices[0].message.content
    response_formatado = response.replace("```json", "").replace("```", "").replace("\n", "")

 #   print(response_formatado)
    return response_formatado