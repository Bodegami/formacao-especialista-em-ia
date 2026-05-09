"""
Desafio: Temperatura dos Servidores
Lucas é responsável por monitorar a temperatura dos servidores em um data center. 
Ele precisa garantir que

Output esperado:
Digite a temperatura atual: 30
Alerta! Temperatura acima do limite recomendado.
"""

# Recebendo a temperatura atual dos servidores
temperatura = float(input("Digite a temperatura atual: "))

# Verificando se a temperatura está acima do limite recomendado
if temperatura > 25:
    print("Alerta! Temperatura acima do limite recomendado.")
else:
    print("Temperatura dentro do limite recomendado.")