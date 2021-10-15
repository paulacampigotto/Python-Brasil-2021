import itertools


class Ativo:
    idAtivo = itertools.count()

    def __init__(self, codigo, cotacoes):
        self.codigo = codigo
        self.cotacoes = []
        for cotacao in cotacoes:
            self.cotacoes.append(float(cotacao))
        self.risco = 0
        self.retorno = 0
        self.id = next(Ativo.idAtivo)
        self.dividendo = 0

    def getId(self):
        return self.id

    def getCodigo(self):
        return self.codigo

    def getCotacoes(self):
        return self.cotacoes

    def getRisco(self):
        return self.risco

    def setRisco(self, risco):
        self.risco = risco

    def getRetorno(self):
        return self.retorno

    def setRetorno(self, retorno):
        self.retorno = retorno

    def getDividendo(self):
        return self.dividendo

    def setDividendo(self, dividendo):
        self.dividendo = dividendo


class Carteira:
    idCarteira = itertools.count()

    def __init__(self, ativos):
        self.ativos = ativos.copy()  # ativos = (Ativo, proporção)
        self.risco = self.defineRisco()
        self.retorno = self.defineRetorno()
        self.dividendo = self.defineDividendo()
        self.id = next(Carteira.idCarteira)
        self.contador_n = 0  # contador_n utilizado no nds()
        self.rank = 0
        self.dist_crowd = 0
        self.rank = 0
        self.dominadas = []  # lista s de carteiras dominadas no nds()

    def getDominadas(self):
        return self.dominadas

    def setDominadas(self, lista):
        self.dominadas = lista

    def appendDominadas(self, x):
        self.dominadas.append(x)

    def setRank(self, valor):
        self.rank = valor

    def getRank(self):
        return self.rank

    def setDist_crowd(self, valor):
        self.dist_crowd = valor

    def getDist_crowd(self):
        return self.dist_crowd

    def setContador_n(self, valor):
        self.contador_n = valor

    def getContador_n(self):
        return self.contador_n

    def getId(self):
        return self.id

    def getAtivos(self):
        return self.ativos

    def setAtivos(self, ativos):
        self.ativos = ativos

    def defineRisco(self):
        r = 0
        for i in self.getAtivos():
            r += i[0].getRisco() * i[1]  # i[0] = Ativo | [1] = Proporção
        return r

    def defineRetorno(self):
        r = 0
        for i in self.getAtivos():
            r += i[0].getRetorno() * i[1]  # i[0] = Ativo | [1] = Proporção
        return r

    def defineDividendo(self):
        d = 0
        for i in self.getAtivos():
            d += i[0].getDividendo() * i[1]
        return d

    def getDividendo(self):
        return self.dividendo

    def getRisco(self):
        return self.risco

    def getRetorno(self):
        return self.retorno

    def getProporcao(self, index):
        return self.ativos[index][1]

    def setProporcao(self, index, proporcao):
        self.ativos[index] = (self.ativos[index][0], proporcao)

    def printCarteira(self):
        for i in self.ativos:
            print(i[0].getCodigo(), round(i[1], 4))

    def fitness(self):
        return self.retorno / self.risco

    def getIndexPeloAtivo(self, ativo):
        j = 0
        for i in self.getAtivos():
            if (i == ativo):
                return j
            j += 1

    def getAtivoPeloIndex(self, index):
        return self.ativos[index]

    def setAtivoPeloIndex(self, index, ativo):
        self.ativos[index] = ativo

    def cardinalidade(self):
        cont = 0
        for i in self.ativos:
            cont += 1
        return cont
