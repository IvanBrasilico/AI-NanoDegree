from copy import copy
from random import randint, sample

from busca.classes.gerente import GerenteRemocao
from busca.classes.patio import Patio
from busca.utils import gera_agendamento_containers, gera_containers_transito


class Simulador:

    def __init__(self, turns=100, tamanho_fila=30):
        self.turns = turns
        self.tamanho_fila = tamanho_fila

    def generate_env(self, perc_pre_load=.5):
        self.containers_transito = gera_containers_transito()
        self.containers_agendados = \
            gera_agendamento_containers(self.containers_transito)
        self.pre_load = []
        qtde = 0
        len_containers = [len(containers) for containers in
                          self.containers_agendados.values()]
        limit = sum(len_containers) * perc_pre_load
        for dia, containers in self.containers_agendados.items():
            for c in containers:
                self.pre_load.append(c)
                containers.pop(containers.index(c))
                self.containers_transito.pop(self.containers_transito.index(c))
                qtde += 1
                if qtde > limit:
                    break
        return self.containers_transito, self.containers_agendados, self.pre_load

    def initialize_gerente(self, mode=None):
        if mode is None or mode == 'nenhum':
            load = sample(self.pre_load, len(self.pre_load))
            print('Modo nenhum')
        else:
            print('Modo like')
            load = copy(self.pre_load)
        self.gerente = GerenteRemocao(Patio())
        self.gerente.processa_fila_gatein(load, mode)

    def run_monte_carlo(self, mode_in=None, mode_out=None):
        totalgeral = 0
        totalgatein = totalgateout = 0
        for turn in range(self.turns):
            # GATE-OUT
            fila_out = []
            random_dia = randint(0, len(self.containers_agendados.keys()))
            containers_dentro = self.containers_agendados[random_dia]
            if containers_dentro:
                for ccs_gate_out in range(self.tamanho_fila):
                    if len(containers_dentro) == 0:
                        if random_dia < 10:
                            random_dia += 1
                        else:
                            random_dia -= 1
                        containers_dentro = self.containers_agendados.get(random_dia, [])
                        continue
                    totalgateout += 1
                    random_ind = randint(0, len(containers_dentro) - 1)
                    fila_out.append(containers_dentro.pop(random_ind))
                totalremocoes = self.gerente.processa_fila_gateout(fila_out, mode=mode_out)
                self.containers_transito.extend(fila_out)
                for cc_out in fila_out:
                    self.containers_agendados[int(cc_out.time_to_leave)].append(cc_out)
                totalgeral += totalremocoes / len(fila_out)
            # GATE-IN
            # Entrar somente o que conseguiu sair, usando len(fila_out)
            fila_in = []
            for ccs_gate_in in range(len(fila_out)):
                totalgatein += 1
                random_ind = randint(0, len(self.containers_transito) - 1)
                cc_in = self.containers_transito.pop(random_ind)
                fila_in.append(cc_in)
            self.gerente.processa_fila_gatein(fila_in, mode=mode_in)
        print('Média de remoções: %s' % (totalgeral / self.turns))
        print('Total gatein: %s gateout:%s' % (totalgatein, totalgateout))
        return totalgeral / self.turns
