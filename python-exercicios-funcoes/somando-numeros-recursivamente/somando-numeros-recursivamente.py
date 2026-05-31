"""
Somando números recursivamente

Paulo está desenvolvendo um programa para calcular valores acumulados em um sistema financeiro. 
Ele precisa somar os todos os números inteiros de 1 até n, onde n é um valor escolhido pelo usuário.

Ajude Paulo criando uma função recursiva que receba um número n e retorne a soma de todos 
os números inteiros de 1 até N.

Exemplo de entrada:

Digite um número: 5

Saída esperada:

A soma de 1 a 5 é: 15
"""

def somar_numeros(n):
    if n == 1:
        return 1
    return n + somar_numeros(n - 1)

n = int(input("Digite um número: "))
resultado = somar_numeros(n)
print(f"A soma de 1 a {n} é: {resultado}")