"""
Calculando o total de vendas

Carlos trabalha em um comércio e precisa saber o valor total de vendas realizadas no dia. 
As vendas são informadas em uma única linha separadas por espaços.

Sua tarefa é criar um programa que receba essa linha, converta os valores para números e exiba o total.

Exemplo de entrada:

Digite os valores das vendas: 100 250 300

Saída esperada:

O total de vendas foi: 650
"""

def calcular_total_vendas(vendas):
    return sum(vendas)

vendas = input("Digite os valores das vendas: ").split()
total = calcular_total_vendas(map(float, vendas))
print(f"O total de vendas foi: {total}")
