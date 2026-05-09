""""
Desafio: Controlando o Orçamento Mensal

Carlos quer monitorar seu orçamento mensal para evitar gastos excessivos. 
Ele estabeleceu um limite de R$ 3.000,00 para seus gastos e precisa de um programa que ajude a controlar suas despesas. 
O programa deve receber o total de despesas realizadas e informar se ele ultrapassou o limite ou ainda está dentro do orçamento.


Output esperado:
Digite o total de despesas do mês (R$): 5897.58
Atenção! Você ultrapassou o limite do orçamento mensal.
"""

# Solicita ao usuário o total de despesas do mês
despesas = float(input("Digite o total de despesas do mês (R$): "))

# Define o limite do orçamento mensal
limite_orcamento = 3000.00

# Verifica se as despesas ultrapassam o limite
if despesas > limite_orcamento:
    print("Atenção! Você ultrapassou o limite do orçamento mensal.")
else:
    print("Você está dentro do orçamento mensal.")