NCONTAINERS = 20000

def gera_containers_transito(n=NCONTAINERS):
    tempos =  np.random.normal(20, 5, NCONTAINERS)
    containers_transito = [Container('{:05d}'.format(numero), tempos[i])
                       for i, numero in enumerate(range(1, NCONTAINERS))]
    return containers_transito
def gera_containers_transito(n=NCONTAINERS):
    tempos =  np.random.normal(20, 5, NCONTAINERS)
    containers_transito = [Container('{:05d}'.format(numero), tempos[i])
                       for i, numero in enumerate(range(1, NCONTAINERS))]
    return containers_transito
def gera_agendamento_containers(containers_transito, dias=30, qtdedia=200, erro=2):
    agendamentos = defaultdict(list)
    container_por_tempo = defaultdict(list)
    for c in containers_transito:
        container_por_tempo[int(c.time_to_leave)].append(c)
    for dia in range(1, dias):
        tempos_dia = np.random.normal(0, erro, qtdedia) + dia
        for t in tempos_dia:
            containers = container_por_tempo[int(t)]
            if containers:
                container_transito = containers.pop(randint(0, len(containers) - 1))
                if container_transito:
                    agendamentos[dia].append(container_transito)
    return agendamentos
