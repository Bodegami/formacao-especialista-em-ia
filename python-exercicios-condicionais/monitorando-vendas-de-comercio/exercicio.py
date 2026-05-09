"""
Desafio: Monitorando Vendas de Comércio
Bruno gerencia um pequeno comércio e quer saber qual produto teve o melhor desempenho de vendas no mês passado. 
Ele registrou a quantidade vendida de dois produtos: maçãs e bananas. 
Agora, ele precisa escrever um programa que identifique e exiba qual deles teve maior venda.

Crie um programa que receba o número de vendas dos dois produtos e exiba uma mensagem indicando qual deles vendeu mais. 
Se as quantidades forem iguais, exiba uma mensagem dizendo que houve empate.

Output esperado:
Digite a quantidade de maçãs vendidas: 50
Digite a quantidade de bananas vendidas: 30
As maças tiveram mais vendas.
"""


# Recebendo a quantidade de vendas dos produtos
vendas_macas = int(input("Digite a quantidade de maçãs vendidas: "))
vendas_bananas = int(input("Digite a quantidade de bananas vendidas: "))

# Comparando as vendas e exibindo o resultado
if vendas_macas > vendas_bananas:
    print("As maças tiveram mais vendas.")
elif vendas_bananas > vendas_macas:
    print("As bananas tiveram mais vendas.")
else:
    print("Houve empate entre as vendas das maçãs e das bananas.")