import random
from collections import OrderedDict
from pprint import pprint

from busca.classes import Container, Patio
from busca.classes import GerenteRemocao

def busca_acima(posicoes, stack, posicao=None, conteiner=None):
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
    return [(coluna + pilha + str(ind),
             stack[coluna + pilha + str(ind)]) for ind in range(altura, 6)]


"""
lista_containers = ['{0:05d}'.format(num) for num in range(10000)]

stack = OrderedDict()
for coluna in COLUNAS:
    for pilha in PILHAS:
        for altura in ALTURAS:
            stack[coluna + pilha + altura] = None

print(lista_containers[1:10])
print(lista_containers[-9:])
print(stack)
print(len(stack))
posicoes = OrderedDict()
for posicao in stack.keys():
    conteiner = choice(lista_containers)
    while conteiner in posicoes:
        conteiner = choice(lista_containers)
    posicoes[conteiner] = posicao
    stack[posicao] = conteiner
print(posicoes)
print(stack)
print(busca_acima(posicoes, stack, 'Eb1'))
"""

patio = Patio()
patio.add_pilha('TESTE')
print(patio._pilhas['TESTE']._pilha)
for r in range(1, 33):
    container = Container('{0:03d}'.format(r))
    patio.add_container(container)
print(patio._pilhas['TESTE']._pilha)
container30 = Container('030')
print(patio.add_container(container30))
print(patio._pilhas['TESTE']._pilha)
container31 = Container('031')
print(patio.add_container(container31))
print(patio._pilhas['TESTE']._pilha)
print(patio._containers)

print(patio.remove_container(container30))
print(patio.add_container(container31))
print(patio._pilhas['TESTE']._pilha)
print(patio._containers)

container20 = patio.get_container_numero('20')
print(container20)
print(patio.remove_container(container20))
if not container20:
    container20 = patio.get_container_numero('020')
print(container20)
print(patio.remove_container(container20))
print(patio._pilhas['TESTE']._pilha)
print(patio._containers)

print(patio.remove_container(container30))
print(patio._pilhas['TESTE']._pilha)
print(patio._containers)
print(patio.remove_container(container31))
print(patio._pilhas['TESTE']._pilha)
print(patio._containers)
print('history: ', patio._history)

gerente = GerenteRemocao(patio)
print(gerente.monta_caminho_remocao('020'))
container003 = patio.get_container_numero('003')
print(gerente.monta_caminho_remocao('003'))

print(gerente.remove_caminho('020'))
print(gerente.remove_caminho('003'))
print(patio._history)

lista_containers = ['{:05d}'.format(num) for num in range(99999)]

# TODO: criar metodos:
# 1. Teste de pilha e patio confirmando comportamento esperado
# 2. "Reserva" na reposicao (se esta na fila, deixar em cima
# 3. Criar tempo randomico, e colocar de volta na pilha de tempo medio mais proximo,
# na selecao de fila para retirada, criar uma probabilidade de curva normal para priorizar
# os de tempo estimado menores

containeres_criados = 0


def test_gerente(gerente, mode, turns=300, fila=40):
    global containeres_criados
    totalgeral = 0
    for turn in range(turns):
        for add_cc in range(fila):
            # ind = random.randint(0, len(lista_containers) - 1)
            # numero = lista_containers.pop(ind)
            containeres_criados += 1
            numero = '{0:07d}'.format(containeres_criados)
            posicao = gerente.add_container(Container(numero))
            # print('numero', numero)
            # print('Posição',  posicao)
        # print('Turn: %s Containers: %s' % (turn, patio_carlo._containers.keys()))

        totalremocoes = 0
        caminhos = []
        numeros = [k for k in patio_carlo._containers.keys()]
        # print(numeros)
        numeros_previstos = []
        for remove_cc in range(fila):
            numero = numeros.pop(random.randint(0, len(numeros) - 1))
            # print(numero)
            caminho = gerente.monta_caminho_remocao(numero)
            caminhos.append((len(caminho), numero))
            numeros_previstos.append(numero)
        if mode == 'ordered':
            caminhos = sorted(caminhos, key=lambda x: x[0])
        for _, numero in caminhos:
            caminho2 = gerente.remove_caminho(numero)
            totalremocoes += len(caminho2)
            # Algoritmo de recolocação de containers
            # TODO: mover este algoritmo para Gerente
            # 1. Limpar container já retirado
            caminho_limpo = [
                container for container in caminho2
                if container._numero !=numero
            ]
            # Algoritmo stay - colocar conteiners previstos "por cima"
            if mode == 'stay':
                filaum = []
                filadois = []
                for container in caminho_limpo:
                    if container._numero in numeros_previstos:
                        # print('Stay ativado!!!')
                        filadois.append(container)
                    else:
                        filaum.append(container)
                caminho_limpo = [*filaum, *filadois]
            # 2. Recolocar containers
            for container in caminho_limpo:
                gerente.add_container(container)
            # print('caminho', caminho)
        # print('Turn: %s Remoções: %s' % (turn, totalremocoes))
        totalgeral += totalremocoes
    print('Média de remoções: %s' % (totalgeral / (turn + 1)))
    return (totalgeral / (turn + 1))


# Testa inclusão automatica de pilhas
patio_carlo = Patio()
gerente = GerenteRemocao(patio_carlo)
print(len(patio_carlo._containers))
print(len(patio_carlo._pilhas))

for add_cc in range(32):
    ind = random.randint(0, len(lista_containers) - 1)
    numero = lista_containers.pop(ind)
    gerente.add_container(Container(numero))

print(len(patio_carlo._containers))
print(len(patio_carlo._pilhas))

for nome, pilha in patio_carlo._pilhas.items():
    print(nome)
    pprint(pilha._pilha)

PRE_LOADS = [0, 60, 150, 400, 1000]  # , 5000]:
FILAS = [10, 20, 30, 45, 60]
results = OrderedDict()
for pre_load in PRE_LOADS:
    results[pre_load] = OrderedDict()
    for fila in FILAS:
        results[pre_load][fila] = OrderedDict()
        print('Pre-load de %s' % pre_load)
        patio_carlo = Patio()
        gerente = GerenteRemocao(patio_carlo)
        for add_cc in range(pre_load):
            ind = random.randint(0, len(lista_containers) - 1)
            numero = lista_containers.pop(ind)
            gerente.add_container(Container(numero))
        for mode in [None, 'ordered', 'stay']:
            print('Gerente criado: %s containers' % len(patio_carlo._containers))
            print('Gerente criado: %s pilhas' % len(patio_carlo._pilhas))
            media_remocoes = test_gerente(gerente, mode, turns=1000, fila=fila)
            results[pre_load][fila][mode] = media_remocoes
            print('Gerente pos teste: %s containers' % len(patio_carlo._containers))
            print('Gerente pos teste: %s pilhas' % len(patio_carlo._pilhas))

x = FILAS
Y = OrderedDict()
for pre_load, pre_load_value in results.items():
    y = []
    for fila, fila_value in pre_load_value.items():
        y_ = fila_value['ordered'] / fila_value[None]
        y.append(y_)
        print(pre_load, fila,
              '{:1.0f}'.format(fila_value[None]),
              '{:1.0f}'.format(fila_value['ordered']),
              '{:02.4f}'.format(y_)
              )
    Y[pre_load] = y

print(results)
print(y)
print(Y)

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
for pre_load, y in Y.items():
    ax = fig.add_subplot(111)
    plt.plot(x, y, label='Preload de %s containers' % pre_load)
    for i, j in zip(x, y):
        ax.annotate('{:00.02f} %'.format(j*100), xy=(i, j))
plt.legend()
plt.ylabel('Original / Ordenado')
plt.xlabel('Tamanho da fila utilizada')
plt.title('Percentual de remocões ordenando os caminhos')
plt.show()



x = FILAS
Y = OrderedDict()
for pre_load, pre_load_value in results.items():
    y = []
    for fila, fila_value in pre_load_value.items():
        y_ = fila_value['stay'] / fila_value[None]
        y.append(y_)
        print(pre_load, fila,
              '{:1.0f}'.format(fila_value[None]),
              '{:1.0f}'.format(fila_value['stay']),
              '{:02.4f}'.format(y_)
              )
    Y[pre_load] = y

print(results)
print(y)
print(Y)

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
for pre_load, y in Y.items():
    ax = fig.add_subplot(111)
    plt.plot(x, y, label='Preload de %s containers' % pre_load)
    for i, j in zip(x, y):
        ax.annotate('{:00.02f} %'.format(j*100), xy=(i, j))
plt.legend()
plt.ylabel('Original / Ordenado')
plt.xlabel('Tamanho da fila utilizada')
plt.title('Percentual de remocões segurando para frente containers previstos')
plt.show()
