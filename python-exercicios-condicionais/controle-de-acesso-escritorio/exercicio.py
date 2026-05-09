""""
Desafio: Controle de Acesso ao Escritório
Mariana é responsável por liberar o acesso ao escritório e precisa de um programa que verifique se os funcionários podem entrar. 
Para isso, ela usará o horário atual. O escritório só permite acesso entre 8h e 18h. 
Crie um programa que receba a hora atual como entrada (em formato de 24 horas) e exiba uma mensagem informando 
se o acesso é permitido ou negado.

Output esperado:
Digite a hora atual (formato 24h): 21
Acesso negado. O escritório está fechado.
"""

# Solicita a hora atual ao usuário
hora_atual = int(input("Digite a hora atual (formato 24h): "))

# Verifica se a hora está dentro do horário permitido
if 8 <= hora_atual < 18:
    print("Acesso permitido. Bem-vindo ao escritório!")
else:
    print("Acesso negado. O escritório está fechado.")