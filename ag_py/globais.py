TAM_POP = 4
CARDINALIDADE = 9
ITERACOES = 10
EXECUCOES = 5
QUANTIDADE_ATIVOS = 9
QUANTIDADE_METRICAS = 5
PROBABILIDADE_MUTACAO = 0.1
PROPORCAO_MAXIMA_CARTEIRA = 1 / 3

# lista_ativos = []
lista_ibovespa = []
lista_ativos_proximo_semestre = []
lista_ibovespa_proximo_semestre = []

### EWMA
λ = 0.94

### GARCH
ω = 0.0001
α = 0.75
β = 0.1

###LPM
τ = 0  # retorno-alvo: média do ativo, taxa livre de risco, um benchmarking (como o Ibovespa) ou mesmo o zero.
k = 0.0000000001  # nível de aversão ao risco do investidor
# k = 0 (safety first) maior nível de aversão ao risco do investidor
# k = 1 (regret)
# k = 2 (second order)
# k = 3 (semi-skewness)
# k = 4 (semi-kurtosis)  menor nível de aversão ao risco do investidor
