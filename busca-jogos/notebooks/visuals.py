import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

from busca.classes import ALTURAS, COLUNAS


def plot_patio(patio, nome_pilha='0001'):
    fig = plt.figure(figsize=(15, 5))
    ax = plt.subplot(111)
    passo_x = 1 / len(COLUNAS)
    passo_y = .8 / len(ALTURAS)
    boxes = []
    for c, coluna in enumerate(patio._pilhas[nome_pilha]._pilha.items()):
        rect = Rectangle((passo_x * c, 0), passo_x * .9, .8)
        boxes.append(rect)
        posicao_x = passo_x * c
        ax.text(passo_x * c + (passo_x / 3), .9, coluna[0], fontsize=20)
        for altura, container in coluna[1].items():
            if container is not None:
                texto_container = f'{container._numero}-{container.time_to_leave:0.2f}'
                posicao_y = passo_y * (int(altura) - 1) + .01
                ax.text(posicao_x + .02, posicao_y + .02,
                        texto_container, fontsize=14)
                rect = Rectangle((posicao_x + .01,
                                  posicao_y),
                                 passo_x * .7, .12)

                boxes.append(rect)

    pc = PatchCollection(boxes, edgecolor='r')
    ax.add_collection(pc)
