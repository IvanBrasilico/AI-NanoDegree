from collections import OrderedDict

import numpy as np

from busca.classes import ALTURAS, COLUNAS


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

    def __init__(self, nome, altura=len(ALTURAS), largura=len(COLUNAS)):
        self._pilha = OrderedDict()
        self._nome = nome
        self._altura = altura
        self._largura = largura
        self._capacity = self._altura * self._largura
        for coluna in COLUNAS:
            self._pilha[coluna] = OrderedDict()
            for altura in ALTURAS:
                self._pilha[coluna][altura] = None
        self._pilhanp = np.zeros((self._largura, self._altura),
                                 dtype=np.float32)

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
        if coluna:
            return self._pilha[coluna][altura]
        return None

    def side_locked(self, position):
        coluna, altura = self.position_totuple(position)
        return self.side_locked(coluna, altura)

    def side_locked(self, pcoluna, paltura):
        firstcol = COLUNAS.find(pcoluna)
        firstheight = ALTURAS.find(paltura)
        for coluna in COLUNAS[firstcol + 1:]:
            for altura in ALTURAS[firstheight:]:
                if self._pilha[coluna][altura] is not None:
                    return True
        return False

    def up_locked(self, position):
        coluna, altura = self.position_totuple(position)
        return self.up_locked(coluna, altura)

    def up_locked(self, pcoluna, paltura):
        firstheight = ALTURAS.find(paltura)
        for altura in ALTURAS[firstheight + 1:]:
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

    def is_position_locked(self, position):
        """Retorna posicao se livre, senao None

        :param posicao: String 'coluna'+'altura'. Caso nao passada,
        retorna primeira livre
        """
        coluna, altura = self.position_totuple(position)
        if coluna:
            if self._pilha[coluna][altura] is not None:
                if not (self.up_locked(coluna, altura) or
                        self.side_locked(coluna, altura)):
                    return coluna, altura
        return False, False

    def first_free_position(self):
        for coluna in COLUNAS:
            for altura in ALTURAS:
                if self._pilha[coluna][altura] == None:
                    return coluna, altura
        return False, False

    def is_acessible(self, coluna, altura):
        up = str(int(altura) + 1)
        down = str(int(altura) - 1)
        col_right = COLUNAS.find(coluna) + 1
        col_left = COLUNAS.find(coluna) - 1
        if (col_left > 0) and (col_right < len(COLUNAS)):
            if self._pilha[col_right].get(up) is not None or \
                    self._pilha[col_left].get(up) is not None:
                # print('Lados ocupados!!!')
                return False
        if self._pilha[coluna].get(up) is not None:
            # print('Em cima ocupado!!!')
            return False
        if int(down) > 0 and self._pilha[coluna].get(down) is None:
            # print('Embaixo vazio!!!')
            return False
        # print(self._pilha[coluna].get(down))
        # print(col_left, col_right, coluna, altura, up, down)
        return True

    def is_position_free(self, position=None):
        """Retorna posicao se livre, senao None

        :param posicao: String 'coluna'+'altura'. Caso nao passada,
        retorna primeira livre
        """
        if position:
            coluna, altura = self.position_totuple(position)
            # print(coluna, altura)
            if self._pilha[coluna][altura] is None and \
                    self.is_acessible(coluna, altura):
                return coluna, altura
            return False, False
        else:
            return self.first_free_position()

    def has_space(self):
        '''
        for coluna in COLUNAS:
            for altura in ALTURAS:
                if self._pilha[coluna][altura] == None:
                    return True
        return False
        '''
        return np.count_nonzero(self._pilhanp) < self._capacity

    def _atualiza_posicao(self, coluna, altura, container):
        self._pilha[coluna][altura] = container
        if container is None:
            time_to_leave = 0
        else:
            time_to_leave = container.time_to_leave
        ind_coluna = COLUNAS.find(coluna)
        ind_altura = ALTURAS.find(altura)
        self._pilhanp[ind_coluna, ind_altura] = time_to_leave

    def remove(self, position, container):
        coluna, altura = self.is_position_locked(position)
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
        # print(coluna, altura, position, container)
        if coluna:
            self._atualiza_posicao(coluna, altura, container)
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
        pilha = self._pilhas.get(nome_pilha)
        if pilha:
            posicao = pilha.stack(container, posicao)
            if posicao:
                self._containers[container._numero] = (nome_pilha, posicao, container)
            return posicao
        return False

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

    def pilhas_com_espaco(self):
        result = []
        for pilha in self._pilhas.values():
            if pilha.has_space():
                result.append(pilha)
        return result
