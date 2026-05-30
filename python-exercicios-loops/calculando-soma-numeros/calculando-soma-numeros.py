"""
Calculando a soma de números

Você está recebendo uma lista de valores representando os produtos de sua loja virtual e 
gostaria de calcular a soma total desses produtos para entender o desempenho financeiro semanal.

valores = [10, 20, 30, 40, 50]

Saída esperada:

A soma total dos produtos é: 150
"""

valores = [10, 20, 30, 40, 50]

total = 0
for valor in valores:
    total += valor

print(f"A soma total dos produtos é: {total}")