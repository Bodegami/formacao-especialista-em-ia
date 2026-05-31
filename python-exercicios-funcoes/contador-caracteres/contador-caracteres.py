""""
contador de caracteres

Sara está participando de um concurso de escrita, e uma das regras exige que cada palavra de 
seu texto tenha um limite máximo de caracteres.

Ajude Sara criando uma função que receba uma palavra e exiba a quantidade de caracteres.

Exemplo de entrada:

Digite uma palavra: tecnologia

Saída esperada:

Essa palavra tem 10 caracteres.
"""

def contador_caracteres(palavra):
    result = len(palavra.strip())  # Remove espaços em branco no início e no final
    return result


palavra = input("Digite uma palavra: ")
print(f"Essa palavra tem {contador_caracteres(palavra)} caracteres.")