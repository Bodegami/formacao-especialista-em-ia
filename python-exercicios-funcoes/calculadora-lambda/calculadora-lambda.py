"""
Calculadora com lambda

Joana está participando de um processo seletivo para uma vaga de desenvolvedora e 
recebeu um desafio técnico de criar uma calculadora para somar, subtrair, multiplicar e dividir dois números.

Sua tarefa é criar um programa usando funções lambda que receba dois números e 
um operador matemático escolhido pelo usuário (+, -, * ou /) e exiba o resultado correspondente.

Exemplo de entrada:

Digite o primeiro número: 10   
Digite o segundo número: 5   
Escolha a operação (| + | - | * | / |): +

Saída esperada:

O resultado é: 15
"""

def calculadora(num1, num2, operador):
    operacoes = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else 'Erro: Divisão por zero'
    }
    
    if operador in operacoes:
        return operacoes[operador](num1, num2)
    else:
        return 'Operação inválida'
    
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
operador = input(f"Escolha a operação (| + | - | * | / |): ")
resultado = calculadora(num1, num2, operador)
print(f"O resultado é: {resultado}")