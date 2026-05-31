"""
Gerador de funções personalizadas

Miguel está desenvolvendo um sistema de cupons de desconto e precisa de uma forma para aplicar 
diferentes taxas de desconto sobre os valores das compras.

Diante deste problema, crie uma closure que gere uma função capaz de calcular o preço final com um 
desconto fixo definido pelo usuário.

Exemplo de entrada:

Digite a porcentagem de desconto: 10 
Digite o valor da compra: 200

Saída esperada:

Preço final com desconto: 180.0
"""

def gerador_desconto(porcentagem):
    def aplicar_desconto(valor):
        return valor - (valor * (porcentagem / 100))
    return aplicar_desconto

porcentagem = float(input("Digite a porcentagem de desconto: "))
valor_compra = float(input("Digite o valor da compra: "))

funcao_desconto = gerador_desconto(porcentagem)
preco_final = funcao_desconto(valor_compra)

print(f"Preço final com desconto: {preco_final}")