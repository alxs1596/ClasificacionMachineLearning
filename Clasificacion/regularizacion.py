import sys
import math
from random import uniform, randint
import matplotlib.pyplot as plt
import numpy as np
from normalizar import normalizarMatrizPorColumnas
from normalizar import normalizarLista

from tkinter import *

lista = []
salidas = []

lista = [[0.1,0.6],[0.1,0.8],[0.2,0.5],[0.2,0.7],[0.2,0.8],[0.3,0.6],[0.3,0.7],[0.3,0.8],[0.6,0.2],[0.6,0.4],[0.7,0.3],[0.8,0.2],[0.8,0.4]]
salidas = [0,0,0,0,0,0,0,0,1,1,1,1,1]

pruebaEntrada = [[0.1,0.6],[0.1,0.8],[0.8,0.4], [0.7,0.4]]
pruebaSalida = [0,0,1,1]

theta = []
grado = 1

def prod(v1,v2):
    return sum([e[0]*e[1] for e in zip(v1,v2)])

def h(X):
    global theta
    return [prod(theta, e) for e in X]

def prediccion(x):
    global theta, grado
    n = len(x)
    for i in range(2, grado + 1):
        for j in range(n):
            x.append(x[j]**i)
    x.insert(0,1)
    return s(prod(theta, x))
    

def s(h):
    return 1 / (1 + math.exp(-1 * h))

def calcularError(y, h, parametroR):
    #return (1/len(y)) * sum([(-e[0]*math.log(s(e[1])))-((1-e[0])*math.log(1-s(e[1]))) for e in zip(y,h)])
    global theta
    a = (parametroR/(2 * len(y)) * sum([theta[j]**2 for j in range(1, len(theta))]))
    #print(a)
    return (-1 / len(y)) * sum([(e[0] * math.log(s(e[1]))) + ((1-e[0])*math.log(1 - s(e[1])))  for e in zip(y,h)])# +a
    #return sum([(e[0] - e[1])**2 for e in zip(y,h)]) / (2 * len(h))

def changeTheta(h, X, y, alpha, parametroR):
    global theta
    thetaRes = [i for i in theta]
    thetaRes[0] =theta[0] - (alpha * (sum([((s(h[i]) - y[i]) * (X[i][0])) for i in range(len(X))])) / len(X))
    for j in range(1, len(X[0])):
        #res = alpha * (sum([((y[i] - s(h[i])) * (X[i][j])) for i in range(len(X))])) / len(X)
        thetaRes[j] = theta[j] - (alpha * (sum([((s(h[i]) - y[i]) * (X[i][j])) for i in range(len(X))])) / len(X))# + (parametroR/len(y))*theta[j]
    return thetaRes

errores = []

def guardarError(error):
    errores.append(error)

def dibujarError():
    plt.plot([i for i in range(len(errores))], errores)
    plt.show()

def clasificacion(X, y,_grado = 1, parametroR = 0.99, alpha = 0.5, diferenciaMinima = 0.0001):
    global grado
    grado = _grado
    if grado > 1:
        for x in range(len(X)):
            for i in range(2, grado + 1):
                n = len(X[x])
                for j in range(n):
                    X[x].append(X[x][j]**i)
                
    for i in range(len(X)):
        X[i].insert(0,1)
    global theta
    theta = [uniform(0,1) for i in range(len(X[0]))]
    temp = [i for i in theta]
    error = calcularError(y, h(X), parametroR)
    errorAnterior = 0
    errorAnterior = error
    cont = 0
    while(True):
        theta = changeTheta(h(X), X, y, alpha, parametroR)
        error = calcularError(y, h(X), parametroR)
        cont = cont + 1
        print(cont,end = " : ")
        print(error)
        guardarError(error)
        if (math.fabs(error - errorAnterior) < diferenciaMinima):
            break
        errorAnterior = error

    #print(h(X))

#clasificacion(lista, salidas)
theta = [-0.8558798606792295, 7.881821356390523, -6.022845328731978]


print ("Prueba")

for i in range(len(pruebaEntrada)):
    res = 0
    if (prediccion(pruebaEntrada[i]) >= 0.5):
        res = 1
    print(pruebaSalida[i], end=" - ")
    print(res)

print(theta)

#x = np.arange(0,1,0.1)

#y = [X * (theta[1]/theta[2])*-1 for X in x]


#plt.plot(x,y)
#plt.plot([i[1] for i in lista],[i[2] for i in lista],'ro')
#plt.show()

root = Tk()
frame = Frame(root, width=500,height=500)
frame.pack()
root.mainloop()