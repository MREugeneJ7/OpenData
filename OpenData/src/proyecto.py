'''
Created on 22 ene. 2019

@author: USUARIO
'''

if __name__ == '__main__':
    with open('exportaciones totales.txt', 'r') as myfile:
        exportaciones = myfile.read()
    exportaciones = exportaciones.split(',')
    exportaciones = exportaciones[13::]
    exportaciones = exportaciones[::-1]
    expPorAno = [[],[]]
    expPorAno[0] = [2012,2013,2014,2015,2016,2017]
    expPorAno[1] = exportaciones
    c = 0
    for i in exportaciones:
        expPorAno[1][c] = float(i)
        c += 1
    print(expPorAno)