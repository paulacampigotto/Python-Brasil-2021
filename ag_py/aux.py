import copy
import math
import random
import sys
from ag_py.classes import *
from ag_py.globais import *


def ativo_aux(carteira):
    while True:
        flag = True
        aleatorio = random.randint(0, QUANTIDADE_ATIVOS - 1)
        for i in carteira:
            if i[0] == aleatorio:
                flag = False
                break
        if flag:
            return aleatorio


def soma_aux(retorno, indice):
    s = 0
    for i in range(indice):
        s += retorno[i]
    return s


def fitnessKey(x):
    return x.fitness()


def retornoKey(x):
    return x.getRetorno()


def riscoKey(x):
    return x.getRisco()


def printPopulacao(pop):
    for carteira in pop:
        carteira.printCarteira()
        print()


def seleciona_dois_ativos(populacao):
    a = random.choice(populacao)
    while (True):
        b = random.choice(populacao)
        if (a.getId() != b.getId()):
            return a, b


def eleicao(pop):
    pop_ord = sorted(pop, key=fitnessKey)
    return pop_ord


def domina(carteira1, carteira2):  
    if (carteira1.getRisco() < carteira2.getRisco() and carteira1.getRetorno() > carteira2.getRetorno()):
        return True
    return False


def melhor_carteira(pop):
    melhor = pop[0]
    for carteira in pop:
        if carteira.fitness() > melhor.fitness():
            melhor = carteira
    return carteira


def le_arquivo_retorna_lista_ativos(data_inicial, data_final, ibovespa):
    lista = []
    nomeAtivos = []
    primeira = True
    flag = False

    with open("arquivos/ativos.csv", "r+") as f:
        linhas = f.readlines()
        listaCotacoes = []

        # PERCORRE LINHAS
        for linha in linhas:
            valores = linha.split(",")
            j = -1
            # PERCORRE CADA ATIVO
            for valor in valores:
                if (valores[0] == 'CODIGOS' and valor != valores[0]):
                    if (valor == 'IBOV\n'):
                        nome = 'IBOV'
                        nomeAtivos.append(nome)
                    else:
                        nomeAtivos.append(valor)
                else:
                    if primeira and valor != 'CODIGOS':
                        for i in range(len(nomeAtivos)):
                            listaCotacoes.append([])
                        primeira = False
                    if data_inicial == valores[0]:
                        flag = True
                    if (flag and valor != valores[0]) and valor != '-' and valor != '-\n':
                        listaCotacoes[j].append(float(valor))
                j += 1
            if data_final == valores[0]:
                flag = False

        lista_ibovespa = []
        for i in range(len(nomeAtivos)):
            codigoAtivo = nomeAtivos[i]
            if (codigoAtivo == "IBOV"):
                lista_ibovespa = copy.copy(listaCotacoes[i])
            else:
                lista.append(Ativo(codigoAtivo, listaCotacoes[i]))

    if ibovespa:
        return lista_ibovespa
    else:
        return lista


def escolhe_ativo(carteira, lista_ativos):
    verifica = True
    while (verifica):
        novoAtivo1 = random.choice(lista_ativos)  # gera um ativo novoAtivo1 para substituir o ativo atual
        for i in carteira.getAtivos():
            if i[0].getCodigo() == novoAtivo1.getCodigo():
                verifica = False
        if verifica:
            return novoAtivo1
        else:
            verifica = True


def retorno(ativo):
    retorno = []
    for i in range(len(ativo) - 1):
        retorno.append((ativo[i + 1] - ativo[i]) / ativo[i])
    return retorno


def retorno_acumulado(ativo):
    retorno = []
    for i in range(len(ativo) - 1):
        if (i == 0):
            retorno.append(((ativo[i + 1] / ativo[i]) - 1) * 100)
        else:
            retorno.append(retorno[i - 1] + ((ativo[i + 1] / ativo[i]) - 1) * 100)

    return retorno


def soma_aux(retorno, indice):
    s = 0
    for i in range(indice):
        s += retorno[i]
    return s


def retorno_acumulado_barras(ativo, proxima_cotacao):
    retorno = []
    x = 0
    for i in range(len(ativo) - 1):
        if (i == 0):
            retorno.append(((ativo[i + 1] / ativo[i]) - 1) * 100)
        else:
            retorno.append(retorno[i - 1] + ((ativo[i + 1] / ativo[i]) - 1) * 100)
            x = ativo[i + 1]
    tam = len(retorno) - 1
    retorno.append(retorno[tam] + ((proxima_cotacao / x) - 1) * 100)
    return retorno


def encontraIndexAtivo(codigo_ativo, lista):
    index = 0
    for i in lista:
        if (i.getCodigo() == codigo_ativo):
            return index
        index += 1


def calcula_cotacoes_carteira(carteira, lista):
    numero_cotacoes = len(lista[0].getCotacoes())
    matriz = []
    for i in range(carteira.cardinalidade()):
        matriz.append([0] * numero_cotacoes)

    for index_ativo in range(carteira.cardinalidade()):
        ativo = carteira.getAtivoPeloIndex(index_ativo)
        for cotacao in range(numero_cotacoes):
            matriz[index_ativo][cotacao] += lista[encontraIndexAtivo(ativo[0].getCodigo(), lista)].getCotacoes()[
                                                cotacao] * ativo[1]

    y = [0] * numero_cotacoes
    for i in range(numero_cotacoes):
        for ativo in range(len(matriz)):
            y[i] += matriz[ativo][i]

    return y


def desvio_padrao(lista):
    n = len(lista)
    media = sum(lista) / n
    cont = 0
    for i in lista:
        cont += (abs(i - media)) ** 2
    cont /= n
    cont = math.sqrt(cont)
    return cont


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
