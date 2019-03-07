from busca.classes import ALTURAS, COLUNAS
from busca.classes.patio import Patio


class GerenteRemocao:

    def __init__(self, patio: Patio):
        self._patio = patio

    def pilha_mesmo_tempo(self, container):
        tempo = container.time_to_leave
        # print(self._patio._pilhas)
        means = sorted([(abs(pilha.time_mean() - tempo), pilha) for pilha in self._patio.pilhas_com_espaco()])
        # print(means)
        if means:
            return means[0][1]
        return None

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

    def processa_fila_gatein(self, fila, mode=None):
        posicoes = []
        for container in fila:
            nome_pilha = None
            if mode == 'like':
                pilha = self.pilha_mesmo_tempo(container)
                if pilha:
                    nome_pilha = pilha._nome
            posicoes.append(self.add_container(container, nome_pilha))
        return posicoes

    def processa_fila_gateout(self, fila, mode=None):
        totalremocoes = 0
        caminhos = []
        for container in fila:
            caminho = self.monta_caminho_remocao(container._numero)
            caminhos.append((len(caminho), container._numero))
        if  mode and 'ordered' in mode:
            caminhos = sorted(caminhos, key=lambda x: x[0])
        for _, numero in caminhos:
            caminho2 = self.remove_caminho(numero)
            if caminho2:
                totalremocoes += len(caminho2)
                del caminho2[-1]  # Elimina container entregue
                # Algoritmo stay - colocar conteiners previstos "por cima"
                if mode and 'stay' in mode:
                    caminho_stay = []
                    for container in reversed(fila):
                        try:
                            ind = caminho2.index(container)
                            caminho_stay.append(caminho2.pop(ind))
                        except IndexError:
                            pass
                    caminho2.extend(caminho_stay)
                # Recolocar containers
                for container in caminho2:
                    self.add_container(container)
        return totalremocoes
