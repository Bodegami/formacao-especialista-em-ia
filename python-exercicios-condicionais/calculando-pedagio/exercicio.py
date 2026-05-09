"""
Desafio: Calculando Pedágio
Fernanda está planejando uma viagem e quer calcular quanto pagará de pedágio. 
O valor do pedágio depende da distância percorrida:

Até 100 km: R$ 10,00
Entre 100 km e 200 km: R$ 20,00
Acima de 200 km: R$ 30,00
Crie um programa que receba a distância percorrida e informe o valor do pedágio correspondente.

Output esperado:
Digite a distância percorrida (em km): 250
O valor do pedágio é: R$ 30,00
"""

# Solicita a distância percorrida ao usuário
distancia = float(input("Digite a distância percorrida (em km): "))

# Calcula o valor do pedágio com base na distância
if distancia <= 100:
    pedagio = 10.00
elif distancia <= 200:
    pedagio = 20.00
else:
    pedagio = 30.00

# Exibe o valor do pedágio
print(f"O valor do pedágio é: R$ {pedagio:.2f}")