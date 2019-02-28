import random
from collections import OrderedDict
from pprint import pprint

COLUNAS = 'ABCDEF'
PILHAS = 'abcde'
ALTURAS = '12345'


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


class Container():
    def __init__(self, numero):
        self._numero = numero

    def time_to_leave(self):
        # TODO: implement time regressor
        return 5

    def __str__(self):
        return self._numero

    def __repr__(self):
        return self._numero


class Pilha():
    """Define uma pilha de largura [A-E] e altura [0-7]"""

    def __init__(self, nome):
        self._pilha = OrderedDict()
        self._nome = nome
        for coluna in COLUNAS:
            for altura in ALTURAS:
                if self._pilha.get(coluna) is None:
                    self._pilha[coluna] = OrderedDict()
                self._pilha[coluna][altura] = None

    def mean(self):
        soma = 0
        qtde = 0
        for coluna in self.pilha.values():
            for container in coluna:
                if container:
                    soma += container.time_to_leave()
                    qtde += 1
        return soma / qtde

    def position_totuple(self, position):
        coluna = position[0]
        altura = position[1]
        return coluna, altura

    def get_containerinposition(self, position):
        coluna, altura = self.position_totuple(position)
        return self._pilha[coluna][altura]

    def side_locked(self, pcoluna, paltura):
        firstcol = COLUNAS.find(pcoluna)
        firstheight = ALTURAS.find(paltura)
        for coluna in COLUNAS[firstcol + 1:]:
            for altura in ALTURAS[firstheight:]:
                if self._pilha[coluna][altura] is not None:
                    return True
        return False

    def up_locked(self, pcoluna, paltura):
        firstheight = ALTURAS.find(paltura)
        for altura in ALTURAS[firstheight + 1:]:
            if self._pilha[pcoluna][altura] is not None:
                return True
        return False

    def is_position_locked(self, position):
        """Retorna posicao se livre, senao None

        :param posicao: String 'coluna'+'altura'. Caso nao passada,
        retorna primeira livre
        """
        coluna, altura = self.position_totuple(position)
        if self._pilha[coluna][altura] is not None:
            if not (self.up_locked(coluna, altura) or
                    self.side_locked(coluna, altura)):
                return coluna, altura
        return False, False

    def remove(self, position, container):
        coluna, altura = self.is_position_locked(position)
        # print(coluna, altura)
        if coluna:
            stacked_container = self._pilha[coluna][altura]
            # print(stacked_container)
            if stacked_container == container:
                self._pilha[coluna][altura] = None
                return True
        return False

    def first_free_position(self):
        for coluna in COLUNAS:
            for altura in ALTURAS:
                if self._pilha[coluna][altura] == None:
                    return coluna, altura
        return False, False

    def is_position_free(self, position=None):
        """Retorna posicao se livre, senao None

        :param posicao: String 'coluna'+'altura'. Caso nao passada,
        retorna primeira livre
        """
        if position:
            coluna, altura = self.position_totuple(position)
            if self._pilha[coluna][altura] is None:
                return coluna, altura
        else:
            return self.first_free_position()

    def stack(self, container, posicao):
        coluna, altura = self.is_position_free(posicao)
        if coluna:
            self._pilha[coluna][altura] = container
            return coluna + altura
        return False


class Patio():
    def __init__(self, nome=''):
        self._nome = nome
        self._pilhas = OrderedDict()
        self._containers = OrderedDict()
        self._history = OrderedDict()

    def add_pilha(self, nome_pilha=None):
        self._pilhas[nome_pilha] = Pilha(nome_pilha)

    def stack(self, container, nome_pilha, posicao=None):
        pilha = self._pilhas[nome_pilha]
        posicao = pilha.stack(container, posicao)
        if posicao:
            self._containers[container._numero] = (nome_pilha, posicao, container)
        return posicao

    def unstack(self, nome_pilha, position, container):
        pilha = self._pilhas.get(nome_pilha)
        if pilha:
            sucess = pilha.remove(position, container)
            if sucess:
                self._history[container._numero] = \
                    self._containers.pop(container._numero)
            return True
        return False

    def add_container(self, container, nome_pilha=None, posicao=None):
        """Adiciona container na pilha, ou no pátio.

        Retorna None se pilha cheia ou pátio cheio.

        :param container: Objeto Container
        :param nome_pilha: Nome da pilha a utilizar.
        Se não passado, procura em todas
        :param posicao: String  'B5' 'coluna_altura'
        :return: None se pilha/pátio cheio, senão posição
        """
        # print(len(self._pilhas), len(self._containers), nome_pilha)
        if nome_pilha is None:
            for pilha in self._pilhas.values():
                posicao = self.add_container(container, pilha._nome, posicao)
                if posicao:
                    break
            # if len(self._containers) >= 30:
            # print(posicao, nome_pilha)
            if not posicao:  # pilhas cheias, criar nova
                nome_pilha = '{0:04d}'.format(len(self._pilhas) + 1)
                # print('Add pilha %s ' % nome_pilha)
                self.add_pilha(nome_pilha)
                posicao = self.stack(container, nome_pilha, posicao)
        else:
            posicao = self.stack(container, nome_pilha, posicao)
        return posicao

    def get_container_tuple(self, numero):
        nome_pilha, position, container = self._containers.get(numero, (None, None, None))
        return nome_pilha, position, container

    def get_container_numero(self, numero):
        nome_pilha, position, container = self.get_container_tuple(numero)
        if nome_pilha:
            return container
        return None

    def remove_container(self, container):
        if container is None or not (isinstance(container, Container)):
            return False
        nome_pilha, position, container = self.get_container_tuple(container._numero)
        if position is None:
            return False
        return self.remove_position(nome_pilha, position, container)

    def remove_position(self, nome_pilha, position, container):
        return self.unstack(nome_pilha, position, container)


class GerenteRemocao:

    def __init__(self, patio: Patio):
        self._patio = patio

    def add_container(self, container, nome_pilha=None, posicao=None):
        return self._patio.add_container(container, nome_pilha, posicao)

    def monta_caminho_remocao(self, numero: str) -> list:
        """Analisa caminho mínimo para remoção do container."""
        nome_pilha, position, container = self._patio.get_container_tuple(numero)
        pilha = self._patio._pilhas.get(nome_pilha)
        caminho = []
        if pilha:
            if numero == container._numero:
                coluna = position[0]
                altura = position[1]
                firstcol = COLUNAS.find(coluna)
                firstheight = ALTURAS.find(altura)
                for coluna in reversed(COLUNAS[firstcol:]):
                    for altura in reversed(ALTURAS[firstheight:]):
                        if pilha._pilha[coluna][altura] is not None:
                            caminho.append(pilha._pilha[coluna][altura])
        return caminho

    def remove_caminho(self, numero: str) -> list:
        caminho = self.monta_caminho_remocao(numero)
        for container in caminho:
            self._patio.remove_container(container)
        return caminho


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

lista_containers = ['{0:06d}'.format(num) for num in range(200000)]


# TODO: criar metodos:
# 1. Teste de pilha e patio confirmando comportamento esperado
# 2. "Reserva" na reposicao (se esta na fila, deixar em cima
# 3. Criar tempo randomico, e colocar de volta na pilha de tempo medio mais proximo,
# na selecao de fila para retirada, criar uma probabilidade de curva normal para priorizar
# os de tempo estimado menores
def test_gerente(gerente, mode, turns=200, fila=30):
    totalgeral = 0
    for turn in range(turns):
        for add_cc in range(fila):
            ind = random.randint(0, len(lista_containers) - 1)
            numero = lista_containers.pop(ind)
            posicao = gerente.add_container(Container(numero))
            # print('numero', numero)
            # print('Posição',  posicao)
        # print('Turn: %s Containers: %s' % (turn, patio_carlo._containers.keys()))

        totalremocoes = 0
        caminhos = []
        numeros = [k for k in patio_carlo._containers.keys()]
        # print(numeros)
        for remove_cc in range(fila):
            numero = numeros.pop(random.randint(0, len(numeros) - 1))
            # print(numero)
            caminho = gerente.monta_caminho_remocao(numero)
            caminhos.append((len(caminho), numero))
        if mode == 'ordered':
            caminhos = sorted(caminhos, key=lambda x: x[0])
        for _, numero in caminhos:
            caminho = gerente.remove_caminho(numero)
            totalremocoes += len(caminho)
            for container in caminho:
                if container._numero != numero:
                    gerente.add_container(container)
            # print('caminho', caminho)
            totalremocoes += len(caminho)
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

PRE_LOADS = [0, 60, 150, 1000]  # , 5000]:
FILAS = [10, 20, 30, 60]
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
        for mode in [None, 'ordered']:
            print('Gerente criado: %s containers' % len(patio_carlo._containers))
            print('Gerente criado: %s pilhas' % len(patio_carlo._pilhas))
            media_remocoes = test_gerente(gerente, mode, turns=100, fila=fila)
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

fig = plt.figure(figsize=(10,6))
for pre_load, y in Y.items():
    ax = fig.add_subplot(111)
    plt.plot(x, y, label='Preload de %s containers' % pre_load)
    for i, j in zip(x, y):
        ax.annotate('{:00.02f} %'.format(j), xy=(i, j))
plt.legend()
plt.ylabel('Original / Ordenado')
plt.xlabel('Tamanho da fila utilizada')
plt.title('Percentual de remocões ordenando os caminhos')
plt.show()

