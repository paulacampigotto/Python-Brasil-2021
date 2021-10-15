import ag_py.operadores as operadores
import ag_py.aux as aux
import ag_py.grafico as grafico
from ag_py.classes import *
from ag_py.globais import *
import ag_py.metricas as metricas
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


def otimizar_carteira():

    retornos_medios_por_dia = []
    desv_padrao_por_dia = []

    total_iterations = EXECUCOES * ITERACOES * QUANTIDADE_METRICAS 
    progress = 0


    with open('arquivos/selected.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    dias = []
    dia=0
    for line in content:
        dias.append([])
        assets = line.split(',')
        for asset in assets:
            dias[dia].append(asset.replace("\'", "").replace(" ", "").replace("[", "").replace("]", ""))
        dia+=1


    pontos_x = []
    pontos_y = []
    solucao_final = []
    lista_fitness = []

    execut_acum = []
    lista_ret_acumulado = []
    for risco in range(QUANTIDADE_METRICAS):
        lista_ret_acumulado.append([])
        retornos_medios_por_dia.append([])
        desv_padrao_por_dia.append([])

        # cada dia
        melhor_do_dia = []

        day_index = -1

        pontos_x_dia = []
        pontos_y_dia = []	
        lista_retornos = []
        for dia in dias:
            lista_retornos.append([])
            lista_todas_carteiras_execucoes = []


            all_assets = []
            dias_label = pd.read_csv('cotacoes/ABEV3.SA.csv')['Date'].values[-len(dias):]
            ativos_label = ["ABEV3.SA", "BTOW3.SA", "B3SA3.SA","BBSE3.SA", "BRML3.SA", "BBDC3.SA", "BBDC4.SA","BRAP4.SA","BBAS3.SA","BRKM5.SA","BRFS3.SA", "CCRO3.SA","CMIG4.SA","HGTX3.SA","CIEL3.SA","COGN3.SA","CSAN3.SA","CVCB3.SA","CYRE3.SA","ECOR3.SA","ELET3.SA","ELET6.SA","EMBR3.SA","ENBR3.SA","EGIE3.SA","EQTL3.SA","FLRY3.SA","GGBR4.SA","GOAU4.SA","GOLL4.SA","HYPE3.SA","IGTA3.SA","ITSA4.SA","ITUB4.SA","JBSS3.SA","KLBN11.SA","RENT3.SA","LAME4.SA","LREN3.SA","MGLU3.SA","MRFG3.SA","MRVE3.SA","MULT3.SA","PETR3.SA","PETR4.SA","QUAL3.SA","RADL3.SA","SBSP3.SA","SANB11.SA","CSNA3.SA","SMLS3.SA","SULA11.SA","TAEE11.SA","VIVT3.SA","TOTS3.SA","UGPA3.SA","USIM5.SA","VALE3.SA","WEGE3.SA","YDUQ3.SA","^BVSP"]
            for ativo_label in ativos_label:
                csv = pd.read_csv('cotacoes/' + ativo_label + '.csv')
                cotacoes = csv['Close'].tolist()[len(csv.index)-len(dias)+day_index-30:len(csv.index)-len(dias)+day_index]
                all_assets.append(Ativo(ativo_label,cotacoes))


            carteira = []
            for ativo in dia:
                for item in all_assets:
                    if item.codigo == ativo:
                        carteira.append(item)

            melhor_do_dia.append(None)
            day_index+=1


            lista_fitness.append([])
            lista_ativos = carteira
            lista_ativos_metrica = metricas.metrica_risco(lista_ativos, risco)


            pontos_x.append([])
            pontos_y.append([])
            solucao_final.append(None)
            x_soma_execucoes = []
            y_soma_execucoes = []
            primeira_execucao = True

            # EXECUÇÕES

            for j in range(EXECUCOES):
                melhor_exec = None

                x_iteracao = []
                y_iteracao = []

                # INICIALIZAÇÃO
                populacao = operadores.populacao_inicial(lista_ativos_metrica)



                pop_filtrada = operadores.filtragem(populacao, True)

                # ITERAÇÕES
                for i in range(ITERACOES):
                    sys.stdout.flush()
                    progress+=1

                    porcentagem = ' ( ' + str(int(progress/(total_iterations * len(dias_label))*100)) + '% )'
                    sys.stdout.write("\r RISCO: " + str(risco + 1) + " EXEC: " + str(j + 1) + " ITERACOES: " + str(i) + "  DIA: " + str(dias_label[day_index]) + porcentagem)
                    
                    pop = operadores.otimiza(pop_filtrada, lista_ativos_metrica)
                    pop_filtrada = pop.copy()
                    solucao_parcial = aux.melhor_carteira(pop_filtrada)
                    if(melhor_exec == None or solucao_parcial.fitness() > melhor_exec.fitness()):
                        melhor_exec = solucao_parcial

                    if solucao_final[risco] == None or solucao_parcial.fitness() > solucao_final[risco].fitness():
                        solucao_final[risco] = solucao_parcial
                    lista_fitness[risco].append(solucao_final[risco].fitness())

                    if melhor_do_dia[day_index] == None or solucao_parcial.fitness() > melhor_do_dia[day_index].fitness():
                        melhor_do_dia[day_index] = solucao_parcial

                lista_todas_carteiras_execucoes.append(melhor_exec)

                

                # GRAFICO FINAL DA ITERAÇÃO
                for carteira in pop_filtrada:
                    x_iteracao.append(carteira.getRisco())
                    y_iteracao.append(carteira.getRetorno())

                x_iteracao.sort()
                y_iteracao.sort()

                if primeira_execucao:
                    x_soma_execucoes = x_iteracao
                    y_soma_execucoes = y_iteracao
                    primeira_execucao = False
                else:
                    for i in range(len(pop_filtrada)):
                        x_soma_execucoes[i] += x_iteracao[i]
                        y_soma_execucoes[i] += y_iteracao[i]

            # GRAFICO FINAL DA EXECUÇÃO
            for i in range(len(pop_filtrada)):
                x_soma_execucoes[i] /= EXECUCOES
                y_soma_execucoes[i] /= EXECUCOES

            pontos_x_dia.append([])
            pontos_y_dia.append([])
            pontos_x_dia[day_index] = x_soma_execucoes
            pontos_y_dia[day_index] = y_soma_execucoes
                    
            
            with open ('final.txt', 'a+') as f:
                if(dias_label[day_index].startswith('2019')):
                    f.write(dias_label[day_index] +  ' '+str(risco) + ' -> ')
                    cart = []
                    exec=0
                    for execucao in lista_todas_carteiras_execucoes:
                        cart.append([])
                        for ativo in execucao.ativos:
                            f.write('(' + str(ativo[0].codigo) + ' ' + str(round(ativo[1],2))+ ')')
                            cart[exec].append(((ativo[0].codigo), (round(ativo[1],2))))
                        lista_retornos[day_index].append(((dias_label[day_index]),(cart[exec])))
                        f.write('\n\n')
                        exec+=1
        
        count_day=-1
        for dia in lista_retornos:
            execut=-1
            count_day+=1
            lista_ret_acumulado[risco].append([])
            for carteira_retorno in dia:
                execut+=1
                lista_ret_acumulado[risco][count_day].append([])
                lista_ret_acumulado[risco][count_day][execut]=0
                for ativo1 in carteira_retorno[1]:
                    cot = pd.read_csv('cotacoes/'+ativo1[0]+'.csv')
                    if(count_day>0 and len(lista_retornos[count_day-1])>0):
                        anterior = float(cot.loc[cot['Date'] == lista_retornos[count_day-1][0][0]]['Close'])
                        atual = float(cot.loc[cot['Date'] == lista_retornos[count_day][0][0]]['Close'])
                        lista_ret_acumulado[risco][count_day][execut]+=((atual-anterior)/atual*float(ativo1[1])*100)

        ax=[]
        bx=[]
        for ik in range(len(pontos_x_dia[0])):
            ax.append([])
            bx.append([])
            ax[ik]=0
            bx[ik]=0
            for px in range(len(pontos_x_dia)):
                ax[ik]+=pontos_x_dia[px][ik]
                bx[ik]+=pontos_y_dia[px][ik]
            ax[ik]/=len(pontos_x_dia)
            bx[ik]/=len(pontos_x_dia)
        pontos_x[risco] = ax
        pontos_y[risco] = bx

    ibov = pd.read_csv('cotacoes/^BVSP.csv')['Close'].tolist()[-len(lista_ret_acumulado[risco]):]
    ibov_ret_acum =[]
    for i in range(len(ibov)):
        if(i>0):
            ibov_ret_acum.append(ibov_ret_acum[i-1]+((ibov[i]-ibov[i-1])/ibov[i])*100)
        else:
            ibov_ret_acum.append(0)
  

    # r = risk metric
    for r in range(QUANTIDADE_METRICAS):
        execut_acum.append([])
        for _ in range(EXECUCOES):
            execut_acum[r].append([])


    for r in range(QUANTIDADE_METRICAS):
        for execution_index in range(EXECUCOES):
            for days_index in range(len(lista_ret_acumulado[r])):  
                if(days_index>0 and len(lista_ret_acumulado[r][days_index-1])>0):
                    lista_ret_acumulado[r][days_index][execution_index] += lista_ret_acumulado[r][days_index-1][execution_index]

    
    for r in range(QUANTIDADE_METRICAS):
        for execution_index in range(EXECUCOES):
            for days_index in range(len(lista_ret_acumulado[r])):  
                if(days_index>0):
                    execut_acum[r][execution_index].append(lista_ret_acumulado[r][days_index][execution_index])
                else:
                    execut_acum[r][execution_index].append(0)
        
    medias =[]
    dv_p = []    
    for r in execut_acum:
        arrays = [np.array(x) for x in r]
        medias.append([np.mean(k) for k in zip(*arrays)])
        dv_p.append([np.std(k) for k in zip(*arrays)])
                    

    for itera in range(len(retornos_medios_por_dia[risco])):
        if(itera>0):
            retornos_medios_por_dia[risco][itera]+=retornos_medios_por_dia[risco][itera-1]

    

    plt.plot(range(len(medias[0])), medias[0], linestyle='solid',
             color='#66ff66', label='CVaR')
    plt.fill_between(range(len(dv_p[0])),np.array(medias[0])-np.array(dv_p[0]),np.array(medias[0])+np.array(dv_p[0]),alpha=.2, color='#66ff66')
   
    plt.plot(range(len(medias[1])), medias[1], linestyle='solid', color='#ff66c7', label='VaR')
    plt.fill_between(range(len(dv_p[1])),np.array(medias[1])-np.array(dv_p[1]),np.array(medias[1])+np.array(dv_p[1]),alpha=.2, color='#ff66c7')


    plt.plot(range(len(medias[2])), medias[2], linestyle='solid',
             color='#c457ff', label='EWMA')
    plt.fill_between(range(len(dv_p[2])),np.array(medias[2])-np.array(dv_p[2]),np.array(medias[2])+np.array(dv_p[2]),alpha=.2, color='#c457ff')


    plt.plot(range(len(medias[3])), medias[3], linestyle='solid',
             color='red', label='GARCH')
    plt.fill_between(range(len(dv_p[3])),np.array(medias[3])-np.array(dv_p[3]),np.array(medias[3])+np.array(dv_p[3]),alpha=.2, color='red')

             
    plt.plot(range(len(medias[4])), medias[4], linestyle='solid',
             color='#66c2ff', label='LPM')
    plt.fill_between(range(len(dv_p[4])),np.array(medias[4])-np.array(dv_p[4]),np.array(medias[4])+np.array(dv_p[4]),alpha=.2, color='#66c2ff')

    plt.plot(range(len(ibov_ret_acum)),ibov_ret_acum, linestyle='solid', color='black', label='Ibovespa')

    plt.legend()
    plt.xlabel('Tempo')
    plt.ylabel('Retorno acumulado (%)')
    plt.title("Retorno Acumulado das carteiras em 2019")
    plt.savefig('graficos/return.png')
    plt.show()


    
    print("Retorno acumulado cvar: ", medias[0][-1])
    print("Desvio padrão cvar: ", dv_p[0][-1])
    print("Retorno acumulado var: ", medias[1][-1])
    print("Desvio padrão var: ", dv_p[1][-1])
    print("Retorno acumulado ewma: ", medias[2][-1])
    print("Desvio padrão ewma: ", dv_p[2][-1])
    print("Retorno acumulado garch: ", medias[3][-1])
    print("Desvio padrão garch: ", dv_p[3][-1])
    print("Retorno acumulado lpm: ", medias[4][-1])
    print("Desvio padrão lpm: ", dv_p[4][-1])

 

if __name__ == "__main__":
    otimizar_carteira()

