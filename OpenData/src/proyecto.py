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
        comparative[1][i] = expPorAno[2][i]/expPorAno[1][i]
    
    print(comparative)
