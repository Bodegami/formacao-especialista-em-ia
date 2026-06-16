import json
from contato_com_llm import recebe_linha_e_retorna_json

# Etapa 1
lista_de_resenhas = []

with open("Resenhas_App_ChatGPT.txt", "r") as file:
    for linha in file:
        lista_de_resenhas.append(linha.strip())

# Etapa 2 e 3
lista_de_resenhas_json = []

for resenha in lista_de_resenhas:
    resenha_json = recebe_linha_e_retorna_json(resenha)
    resenha_dict = json.loads(resenha_json)
    lista_de_resenhas_json.append(resenha_dict)

# Etapa 4
def contador_e_juntador_de_resenhas(lista_de_resenhas_json):
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    lista_de_dicionarios_str = []

    for resenha in lista_de_resenhas_json:
        if resenha["avaliacao"] == "Positiva":
            contador_positivas += 1
        elif resenha["avaliacao"] == "Negativa":
            contador_negativas += 1
        else:
            contador_neutras += 1

        lista_de_dicionarios_str.append(str(resenha))
    
    textos_unidos = '#####'.join(lista_de_dicionarios_str)
    return contador_positivas, contador_negativas, contador_neutras, textos_unidos

pos, neg, neut, textos = contador_e_juntador_de_resenhas(lista_de_resenhas_json)
print(f"Resenhas Positivas: {pos}")
print(f"Resenhas Negativas: {neg}")
print(f"Resenhas Neutras: {neut}")
print(f"Textos unidos: {textos[:500]}...")  # Imprime