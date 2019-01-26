import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import copy
from scipy import stats


'''
Created on 22 ene. 2019

@author: USUARIO
'''

if __name__ == '__main__':
    '''
        Extraer datos de las exportaciones totales por año
    '''
    with open('exportaciones totales.txt', 'r') as myfile:
        exportaciones = myfile.read()
    exportaciones = exportaciones.split(',')
    exportaciones = exportaciones[13::]
    exportaciones = exportaciones[::-1]
    expPorAno = [[],[], []]
    expPorAno[0] = [2012,2013,2014,2015,2016,2017]
    expPorAno[1] = exportaciones
    c = 0
    for i in exportaciones:
        expPorAno[1][c] = float(i)
        c += 1
    '''
        Extraer datos del paro
    '''
    expPorAno[2] = [0,0,0,0,0,0]
    with open('paro.tsv', 'r') as myfile:
        paro = myfile.read()
    paro = paro.split('\n')
    paromatriz = [1] * (len(paro))
    i = 0
    for p in paro:
        paromatriz[i] = p.split('\t')
        i+=1
    justData = []
    for p in paromatriz:
        if (len(p) > 1):
            if(p[2] == 'Dato' and p[0] == 'Canarias'):
                justData.append(p)
    for a in expPorAno[0]:
        for data in justData:
            if(str(a) == data[1][0:4]):
                expPorAno[2][expPorAno[0].index(a)] += int(data[3])
    for a in expPorAno[2]:
        a = a/12
    print(expPorAno)
    
    comparative = [[],[]]
    comparative[0] = expPorAno[0]
    comparative[1] = ['']*6
    for i in range(0,6):
        comparative[1][i] = expPorAno[1][i]/expPorAno[2][i]
    
    print(comparative)
    
    # data
    df=pd.DataFrame({'Año': expPorAno[0][0::], 'Exportaciones totales': expPorAno[1][0::], 'Parados medios por mes': expPorAno[2][0::] })
 
    # style
    plt.style.use('seaborn-darkgrid')
 
    # create a color palette
    palette = plt.get_cmap('Set1')
     
    # multiple line plot
    plt.subplot(321)

    num=0
    for column in df.drop('Año', axis=1):
        num+=1
        plt.plot(df['Año'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
     
    # Add legend
    plt.legend(loc=2, ncol=2)
    plt.title("Grafico", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Años")
    plt.ylabel("Cantidad")
     
    
    #Normalizado
    expPorAnoNor = copy.deepcopy(expPorAno)
    acumParo = 0
    acumExp = 0
    for i in range(0,6):
        acumExp += expPorAno[1][i]
        acumParo += expPorAno[2][i]
    for i in range(0,6):
        expPorAnoNor[1][i] = expPorAno[1][i]/acumExp
        expPorAnoNor[2][i] = expPorAno[2][i]/acumParo
        
    df1=pd.DataFrame({'Año': expPorAnoNor[0][0::], 'Exportaciones totales': expPorAnoNor[1][0::], 'Parados medios por mes': expPorAnoNor[2][0::] })
    plt.subplot(322)

    num=0
    for column in df1.drop('Año', axis=1):
        num+=1
        plt.plot(df1['Año'], df1[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
     
    # Add legend
    plt.legend(loc=2, ncol=2)
    
    # Add titles
    plt.title("Grafico Normalizado", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Años")
    plt.ylabel("Cantidad")
    
    df2=pd.DataFrame({'Año': comparative[0][0::], 'Exportaciones/Paro': comparative[1][0::] })
    plt.subplot(323)

    num=0
    for column in df2.drop('Año', axis=1):
        num+=1
        plt.plot(df2['Año'], df2[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)
     
    # Add legend
    plt.legend(loc=2, ncol=2)
    
    # Add titles
    plt.title("Grafico Comparativo", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Años")
    plt.ylabel("Cantidad")
    df3=pd.DataFrame({'Paro': expPorAno[2][0::], 'Exportaciones': expPorAno[1][0::] })
    plt.subplot(324)

    num=0
    for column in df3.drop('Paro', axis=1):
        num+=1
        plt.plot(df3['Paro'], df3[column], marker='.', color=palette(num), linewidth=0, alpha=0.9, label=column)
     
    # Add legend
    plt.legend(loc=2, ncol=2)
    
    # Add titles
    plt.title("Grafico Comparativo", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Paro")
    plt.ylabel("Exportaciones")
    
    
    #Pearson
    mediaParo = np.average(expPorAno[2])
    mediaExp = np.average(expPorAno[1])
    covarianza = 0
    expPorAnoPearson = copy.deepcopy(expPorAno)
    expPorAnoPearson.append([])
    for i in range(0,6):
        expPorAnoPearson[1][i] = expPorAno[1][i] - mediaExp
        expPorAnoPearson[2][i] = expPorAno[2][i] - mediaParo
        expPorAnoPearson[3].append(expPorAnoPearson[1][i] * expPorAnoPearson[2][i])
        covarianza += expPorAnoPearson[3][i]
    covarianza /= 5
    tDP = np.std(expPorAno[2])
    tDE = np.std(expPorAno[1])
    correlacion = covarianza/(tDE*tDP)
    print(correlacion)
    print(correlacion**2*100)
    
    
    #Student test
    
    print (stats.t.ppf(0.05,4))
    
    t2, p2 = stats.ttest_ind(expPorAno[2],expPorAno[1])
    s ="t = " + str(t2)
    s += " p = " + str(2*p2)
    
    limInf = correlacion +(-stats.t.ppf(0.05,4)*np.sqrt((1-correlacion**2)/4))
    limSup = correlacion +(stats.t.ppf(0.05,4)*np.sqrt((1-correlacion**2)/4))
    
    s += "\n [" + str(limSup) + "," + str(limInf) + "]"
    
    plt.subplot(325)
     
    # Add legend
    df4 = pd.DataFrame({'group':["t"], 'values': [t2]})
    plt.stem(df4['values'])
    
    # Add titles
    plt.title("T valor", loc='left', fontsize=12, fontweight=0, color='orange')
    
    plt.subplot(326)
     
    # Add legend
    df5 = pd.DataFrame({'group':["p","limInf","limSup"], 'values': [p2, limInf, limSup]})
    plt.stem(df5['values'])
    
    # Add titles
    plt.title("P -Valor y limites", loc='left', fontsize=12, fontweight=0, color='orange')
    
    plt.show()
    
    
