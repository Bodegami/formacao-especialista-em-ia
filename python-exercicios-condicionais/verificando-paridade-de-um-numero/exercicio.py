""""
Desafio: Verificando a paridade de um número

Lucas está desenvolvendo um jogo e precisa de uma funcionalidade que verifique se um número é par ou ímpar. 
Essa verificação será usada para definir ações diferentes dentro do jogo. 
Escreva um programa que receba um número inteiro e exiba uma mensagem informando se ele é par ou ímpar.

Output esperado:
Digite um número inteiro: 20
O número 20 é par.
"""

numero = int(input("Digite um número inteiro: "))
if numero % 2 == 0:
    print(f"O número {numero} é par.")
else:    
    print(f"O número {numero} é ímpar.")