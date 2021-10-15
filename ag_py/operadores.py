import copy
import random
import sys

from ag_py.aux import *
from ag_py.classes import *
from ag_py.globais import *


def otimiza(populacao_filtrada, lista_ativos):
    # global populacao
    popCrossover = crossover(populacao_filtrada)
    populacaoMutada = mutacao(popCrossover, lista_ativos)
    return filtragem(populacaoMutada, False).copy()


def populacao_inicial(lista_ativos):
    populacao = []
    for j in range(TAM_POP):
        carteira = []
        total = 0
        index = len(lista_ativos)-1
        for i in range(len(lista_ativos)):
            if(index == 0):
                proporcao = 1-total
                ativo = (lista_ativos[index], proporcao)
            else:
                proporcao = random.uniform(0.09,1/CARDINALIDADE)
                ativo = (lista_ativos[index], proporcao)  ##### satisfazer a soma dos pesos = 1
            index-=1
            total+=proporcao
            carteira.append(ativo)
        populacao.append(Carteira(carteira))
    return populacao


def crossover(pop):
    pares = selecao(pop)
    novaPop = []
    novaPop = copy.copy(pop)

    for par in pares:
        pai1 = copy.copy(par[0])
        pai2 = copy.copy(par[1])
        probabilidade = random.random()
        ativosFilho1 = []
        ativosFilho2 = []
        for j in range(CARDINALIDADE):  # percorre a carteira j da população

            ativosFilho1.append((pai1.getAtivos()[j][0], pai1.getProporcao(j) *
                                 probabilidade + pai2.getProporcao(j) * (1 - probabilidade)))

            ativosFilho2.append((pai2.getAtivos()[j][0], pai2.getProporcao(j) *
                                 probabilidade + pai1.getProporcao(j) * (1 - probabilidade)))

        filho1 = Carteira(ativosFilho1)
        filho2 = Carteira(ativosFilho2)
        novaPop.append(filho1)
        novaPop.append(filho2)

    return novaPop


def mutacao(pop, lista_ativos):
    for carteira in pop:
        index1 = 0
        for ativo in carteira.getAtivos():
            probabili = random.random()
            if (probabili <= PROBABILIDADE_MUTACAO):
                while(True):
                    r = random.uniform(0, ativo[1])  # gera um valor r aleatório para ser subtraído da proporção atual
                    index2 = random.randint(0,8)
                    ativo2 = carteira.getAtivoPeloIndex(index2)
                    if(index1 != index2 and ativo2[1]+r < 1 and ativo2[1]+r >0):
                        carteira.setAtivoPeloIndex(index1, (ativo[0], ativo[1] - r))
                        carteira.setAtivoPeloIndex(index2, (ativo2[0], ativo2[1] + r))
                        break
            index1 += 1

    return pop


def selecao(pop):
    popu = pop.copy()
    pares = []
    p_a = []
    p_b = []
    tam = len(pop)
    qtd_pares = tam // 2
    for i in range(qtd_pares):
        ind_a, ind_b = seleciona_dois_ativos(popu)
        if ind_a.getRank() < ind_b.getRank():
            p_a = copy.copy(ind_a)
        else:
            p_a = copy.copy(ind_b)
        for k in popu:
            if k.getId() == p_a.getId():
                popu.remove(k)
        ind_c, ind_d = seleciona_dois_ativos(popu)

        if ind_c.getRank() < ind_d.getRank():
            p_b = copy.copy(ind_c)
        else:
            p_b = copy.copy(ind_d)
        pares.append((p_a, p_b))

    return pares


def nds(popu):
    fronteira = [[]]
    for p in popu:
        p.setContador_n(0)
        for q in popu:
            if p != q:
                if domina(p, q):
                    p.appendDominadas(q)
                else:
                    if (domina(q, p)):
                        p.setContador_n(p.getContador_n() + 1)
        if p.getContador_n() == 0:
            p.setRank(1)
            fronteira[0].append(p)

    i = 0
    while (fronteira[i]):
        Q = []
        for p in fronteira[i]:
            for q in p.getDominadas():
                q.setContador_n(q.getContador_n() - 1)
                if q.getContador_n() == 0:
                    q.setRank(i + 1)
                    Q.append(q)
        i += 1
        fronteira.append([])
        fronteira[i] = Q.copy()

    return fronteira


def crowding_distance(fronteira):
    n = len(fronteira)
    pop_ord = []
    for i in fronteira:
        i.setDist_crowd(0)

    for m in range(2):
        if m == 1:
            pop_ord = sorted(fronteira, key=retornoKey)
            # for i in pop_ord:
            pop_ord[0].setDist_crowd(sys.maxsize)
            pop_ord[n - 1].setDist_crowd(sys.maxsize)
            for j in range(1, n - 2, 1):
                pop_ord[j].setDist_crowd(pop_ord[j].getDist_crowd() +
                                         (pop_ord[j + 1].getDist_crowd() - pop_ord[j - 1].getDist_crowd()) / (
                                                     pop_ord[n - 1].getRetorno() - pop_ord[0].getRetorno()))

        else:
            pop_ord = sorted(fronteira, key=riscoKey)
            pop_ord[0].setDist_crowd(sys.maxsize)
            pop_ord[n - 1].setDist_crowd(sys.maxsize)
            for j in range(1, n - 2, 1):
                pop_ord[j].setDist_crowd(pop_ord[j].getDist_crowd() +
                                         (pop_ord[j + 1].getDist_crowd() - pop_ord[j - 1].getDist_crowd()) / (
                                                     pop_ord[n - 1].getRisco() - pop_ord[0].getRisco()))

    return pop_ord


def filtragem(populacao_entrada, primeira_iteracao):
    pop = copy.copy(populacao_entrada)
    if primeira_iteracao:
        p = len(pop)
    else:
        p = len(pop) // 2
    fronteiras = nds(pop)
    fronteiras.pop(len(fronteiras) - 1)
    pop_linha = []
    i = 0
    cont = 0
    while (True):
        tam = len(fronteiras[i])
        if (tam + cont < p):
            pop_linha.append(fronteiras[i])
            cont += tam
        else:
            aux = crowding_distance(fronteiras[i])
            pop_linha.append(aux[0:p - cont])
            cont += (p - cont)
        i += 1
        if (cont == p):
            break

    pop = []
    for i in pop_linha:
        for j in i:
            pop.append(j)

    return pop
