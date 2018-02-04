from random import choice
COLUNAS = 'ABCDEFGHIJ'
PILHAS = 'abcde'
ALTURAS = '12345'

lista_containers = ['{0:05d}'.format(num) for num in range(10000)]

stack = {coluna+pilha+altura: None
         for coluna in COLUNAS
         for pilha in PILHAS
         for altura in ALTURAS}

print(lista_containers[1:10])
print(stack)
print(len(stack))
print(lista_containers[-9:])

posicoes = {}

for posicao in stack.keys():
    conteiner = choice(lista_containers)
    while conteiner in posicoes:
        conteiner = choice(lista_containers)
    posicoes[conteiner] = posicao
    stack[posicao] = conteiner

print(posicoes)
print(stack)


def busca_acima(posicao=None, conteiner=None):
    if posicao is None:
        posicao = posicoes[conteiner]
    coluna = posicao[0]
    pilha = posicao[1]
    altura = int(posicao[2])
    """result = []
    for ind in range(altura, 6):
        print(coluna, pilha, ind)
        print(coluna+pilha)
        result.append(stack[coluna+pilha+str(ind)])
    """
    return [(coluna+pilha+str(ind),
            stack[coluna+pilha+str(ind)]) for ind in range(altura, 6)]


print(busca_acima('Hb1'))
