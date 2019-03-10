from collections import OrderedDict

from busca.classes import ALTURAS, COLUNAS
from busca.utils.logconf import logger

colunas_dict = {k: ind for ind, k in enumerate(COLUNAS)}
alturas_dict = {k: ind for ind, k in enumerate(ALTURAS)}


class Container():
    def __init__(self, numero, time_to_leave=5):
        self._numero = numero
        self._time_to_leave = time_to_leave

    @property
    def time_to_leave(self):
        return self._time_to_leave

    @time_to_leave.setter
    def time_to_leave(self, time_to_leave):
        self._time_to_leave = time_to_leave

    def __str__(self):
        return self._numero

    def __repr__(self):
        return self._numero


class Pilha():
    """Define uma pilha de largura [A-E] e altura [0-7]"""

    LEFT = 2
    UP = 3
    RIGHT = 4

    def __init__(self, nome, altura=len(ALTURAS), largura=len(COLUNAS)):
        self._pilha = OrderedDict()
        self._nome = nome
        self._altura = altura
        self._largura = largura
        for coluna in COLUNAS:
            self._pilha[coluna] = OrderedDict()
            for altura in ALTURAS:
                self._pilha[coluna][altura] = None

    def position_totuple(self, position):
        coluna = None
        altura = None
        try:
            coluna = position[0]
            altura = position[1]
        except:
            pass
        return coluna, altura

    def get_containerinposition(self, position):
        coluna, altura = self.position_totuple(position)
        if coluna is not None:
            _coluna = self._pilha.get(coluna)
            if _coluna:
                return _coluna.get(altura)
        return None

    def side_locked_position(self, position):
        coluna, altura = self.position_totuple(position)
        return self.side_locked(coluna, altura)

    def side_locked(self, pcoluna, paltura):
        ind_col = colunas_dict[pcoluna]
        ind_alt = alturas_dict[paltura]
        sides_locked = set()
        if ind_col + 1 < len(COLUNAS):
            coluna = COLUNAS[ind_col + 1]
            altura = ALTURAS[ind_alt]
            if self._pilha[coluna][altura] is not None:
                sides_locked.add(Pilha.RIGHT)
        if ind_col > 0:
            coluna = COLUNAS[ind_col - 1]
            altura = ALTURAS[ind_alt]
            if self._pilha[coluna][altura] is not None:
                sides_locked.add(Pilha.LEFT)
        return sides_locked

    def up_locked_position(self, position):
        coluna, altura = self.position_totuple(position)
        return self.up_locked(coluna, altura)

    def up_locked(self, pcoluna, paltura):
        ind_alt = alturas_dict[paltura]
        if ind_alt == len(ALTURAS) - 1:
            return True
        altura = ALTURAS[ind_alt + 1]
        if self._pilha[pcoluna][altura] is not None:
            return True
        return False

    def time_mean(self):
        soma = 0
        qtde = 0
        for coluna in self._pilha.values():
            for container in coluna.values():
                if container:
                    soma += container.time_to_leave
                    qtde += 1
        if qtde == 0:
            return 0
        return soma / qtde

    def sides_locked(self, coluna, altura):
        """Retorna posicoes livres se tem carga na posicao, senao True
        :param posicao: String 'coluna'+'altura'. Caso nao passada,
        retorna primeira livre
        """
        sides_free = set({Pilha.LEFT, Pilha.UP, Pilha.RIGHT})
        if coluna and altura:
            if self.up_locked(coluna, altura):
                sides_free.remove(Pilha.UP)
            sides_locked = self.side_locked(coluna, altura)
            if sides_locked:
                sides_free.remove(sides_locked)
        return sides_free

    def is_locked(self, coluna, altura):
        if self.up_locked(coluna, altura) or \
                self.sides_locked(coluna, altura) == {Pilha.LEFT, Pilha.RIGHT}:
            return True
        return False

    def is_position_locked(self, position):
        coluna, altura = self.position_totuple(position)
        return self.is_locked(coluna, altura)

    def is_acessible(self, coluna, altura):
        """Testa se é uma posição válida para armazenagem"""
        ind_alt = alturas_dict[altura]
        if ind_alt == len(ALTURAS) - 1:
            return False
        up = ALTURAS[ind_alt + 1]
        if ind_alt == 0:
            down = -1
        else:
            down = ALTURAS[ind_alt - 1]
        col_right = colunas_dict[coluna] + 1
        col_left = colunas_dict[coluna] - 1
        # print(up, down, col_left, col_right)
        if (col_left > 0):
            left = COLUNAS[col_left]
            if self._pilha[col_left].get(up) is not None:
                logger.debug('Lado esquerdo ocupado!!!')
                return False
        if (col_right < len(COLUNAS)):
            right = COLUNAS[col_right]
            if self._pilha[right].get(up) is not None:
                logger.debug('Lado direito ocupado!!!')
                return False
        if self._pilha[coluna].get(up) is not None:
            logger.debug('Em cima ocupado!!!')
            return False
        if int(down) >= 0 and self._pilha[coluna].get(down) is None:
            logger.debug('Embaixo vazio!!!')
            return False
        return True

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
            if self._pilha[coluna][altura] is None and \
                    self.is_acessible(coluna, altura):
                return coluna, altura
            return False, False
        else:
            return self.first_free_position()

    def _atualiza_posicao(self, coluna, altura, container):
        self._pilha[coluna][altura] = container

    def remove(self, position, container):
        coluna, altura = self.position_totuple(position)
        if not coluna or self.is_locked(coluna, altura):
            return False
        # print(coluna, altura)
        if coluna:
            stacked_container = self._pilha[coluna][altura]
            # print(stacked_container)
            if stacked_container == container:
                self._atualiza_posicao(coluna, altura, None)
                return True
        return False

    def stack(self, container, position=None):
        coluna, altura = self.is_position_free(position)
        if coluna:
            self._atualiza_posicao(coluna, altura, container)
            return coluna + altura
        return False

    def has_space(self):
        for coluna in COLUNAS:
            for altura in ALTURAS:
                if self._pilha[coluna][altura] == None:
                    return True
        return False


class Patio():
    def __init__(self, nome=''):
        self._nome = nome
        self._pilhas = OrderedDict()
        self._containers = OrderedDict()
        self._history = OrderedDict()

    def add_pilha(self, nome_pilha=None):
        self._pilhas[nome_pilha] = Pilha(nome_pilha)

    def stack(self, container, nome_pilha=None, position=None):
        pilha = self._pilhas.get(nome_pilha)
        if pilha:
            position = pilha.stack(container, position)
            if position:
                self._containers[container._numero] = (nome_pilha, position, container)
            return position
        return False

    def unstack(self, container, nome_pilha=None, position=None):
        pilha = self._pilhas.get(nome_pilha)
        if pilha is not None:
            success = pilha.remove(position, container)
            if success:
                self._history[container._numero] = \
                    self._containers.pop(container._numero)
            return True
        return False

    def add_container(self, container, nome_pilha=None, posicao=None):
        """Adiciona container na pilha, ou no pátio.
        Adiciona pilha se pilha cheia.
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
        return self.remove_position(container, nome_pilha, position)

    def remove_position(self, container: Container, nome_pilha: str, position: str):
        return self.unstack(container, nome_pilha, position)

    def pilhas_com_espaco(self):
        result = []
        for pilha in self._pilhas.values():
            if pilha.has_space():
                result.append(pilha)
        return result
