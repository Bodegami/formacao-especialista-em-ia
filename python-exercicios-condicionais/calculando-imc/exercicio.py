""""
Desafio: Calculando o IMC

Anna Júlia está criando um sistema para calcular o Índice de Massa Corporal (IMC) e fornecer recomendações básicas. 
O programa deve receber o peso e a altura de uma pessoa e exibir o valor do IMC, além de indicar se está abaixo do peso, 
com peso normal ou acima do peso. 

Crie um programa que receba o peso (em kg) e a altura (em metros) e calcule o IMC usando a fórmula: 
IMC = peso / (altura ** 2) Depois, exiba o valor do IMC e uma mensagem indicando se está abaixo do peso 
(IMC < 18.5), peso normal (18.5 <= IMC < 25) ou acima do peso (IMC >= 25).


Output esperado:
Digite o peso em kg: 75
Digite a altura em metros: 1.68
Seu IMC é: 26.57
Você está acima do peso.
"""

# Recebendo o peso e a altura do usuário
peso = float(input("Digite o peso em kg: "))
altura = float(input("Digite a altura em metros: "))

# Calculando o IMC
imc = peso / (altura ** 2)
# Exibindo o valor do IMC
print(f"Seu IMC é: {imc:.2f}") 

# Verificando a categoria do IMC e exibindo a mensagem correspondente
if imc < 18.5:
    print("Você está abaixo do peso.")
elif 18.5 <= imc < 25:
    print("Você está com peso normal.")
else:
    print("Você está acima do peso.")