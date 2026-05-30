""""
Organizando seu portfólio

Ana está desenvolvendo seu portfólio para exibir os projetos de Python que concluiu. 
Ela organizou uma lista com o nome de cada projeto, mas percebeu que alguns itens podem estar ausentes, 
aparecendo como None:

projetos = ["website", "jogo", "análise de dados", None, "aplicativo móvel"]

Saída esperada:

Projetos concluídos:
website
jogo
análise de dados
Projeto ausente
aplicativo móvel
"""

projetos = ["website", "jogo", "análise de dados", None, "aplicativo móvel"]

print("Projetos concluídos:")
for projeto in projetos:
    if projeto is None:
        print("Projeto ausente")
    else:
        print(projeto)
