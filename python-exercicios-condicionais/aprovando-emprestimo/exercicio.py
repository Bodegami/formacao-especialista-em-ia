""""
Desafio: Aprovando Empréstimo
Pedro quer solicitar um empréstimo, mas a aprovação depende de duas condições:

O valor da renda mensal precisa ser maior que R$ 2.000,00.
O valor da parcela não pode ultrapassar 30% da renda.
Crie um programa que receba como entrada a renda mensal de Pedro e o valor da parcela desejada. 
O programa deve informar se o empréstimo foi aprovado ou negado com base nas condições acima.

Output esperado:
Digite o valor da sua renda mensal: 2500
Digite o valor da parcela desejada: 800
Empréstimo negado: parcela ultrapassa 30% da renda.
"""

# Recebe a renda mensal e o valor da parcela desejada
renda_mensal = float(input("Digite o valor da sua renda mensal: "))
valor_parcela = float(input("Digite o valor da parcela desejada: "))

# Verifica as condições para aprovação do empréstimo
if renda_mensal > 2000 and valor_parcela <= 0.3 * renda_mensal:
    print("Empréstimo aprovado!")
elif renda_mensal <= 2000:
    print("Empréstimo negado: renda mensal insuficiente.")
else:
    print("Empréstimo negado: parcela ultrapassa 30% da renda.")