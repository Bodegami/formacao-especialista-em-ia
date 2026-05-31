"""
Faça como eu fiz: calculando a idade

Julia é professora e precisa de um programa para ajudar seus alunos a calcularem suas idades com base no ano de nascimento. 
Sua tarefa é criar uma função que receba o ano de nascimento e o ano atual e retorne à idade correspondente.

Exemplo de entrada:

Digite o ano de nascimento: 2005  
Digite o ano atual: 2025

Saída esperada:

A idade é 20 anos.
"""

def calcular_idade(ano_nascimento, ano_atual):
    idade = ano_atual - ano_nascimento
    return idade

ano_nascimento = int(input("Digite o ano de nascimento: "))
ano_atual = int(input("Digite o ano atual: "))

idade = calcular_idade(ano_nascimento, ano_atual)
print(f"A idade é {idade} anos.")