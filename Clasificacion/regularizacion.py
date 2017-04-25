import sys
import math
from random import uniform, randint
import matplotlib.pyplot as plt
import numpy as np
from normalizar import normalizarMatrizPorColumnas
from normalizar import normalizarLista
lista = []
salidas = []

lista = [[0.1,0.6],[0.1,0.8],[0.2,0.5],[0.2,0.7],[0.2,0.8],[0.3,0.6],[0.3,0.7],[0.3,0.8],[0.6,0.2],[0.6,0.4],[0.7,0.3],[0.8,0.2],[0.8,0.4]]
salidas = [0,0,0,0,0,0,0,0,1,1,1,1,1]

pruebaEntrada = [[0.1,0.6],[0.1,0.8],[0.8,0.4], [0.7,0.4]]
pruebaSalida = [0,0,1,1]

theta = []

def prod(v1,v2):
    return sum([e[0]*e[1] for e in zip(v1,v2)])

def h(X):
    global theta
    return [prod(theta, e) for e in X]

def prediccion(x):
    global theta
    x.insert(0,1)
    return s(prod(theta, x))
    

def s(h):
    return 1 / (1 + math.exp(-1 * h))

def calcularError(y, h):
    #return (1/len(y)) * sum([(-e[0]*math.log(s(e[1])))-((1-e[0])*math.log(1-s(e[1]))) for e in zip(y,h)])

    return (-1 / len(y)) * sum([(e[0] * math.log(s(e[1]))) + ((1-e[0])*math.log(1 - s(e[1])))  for e in zip(y,h)])
    #return sum([(e[0] - e[1])**2 for e in zip(y,h)]) / (2 * len(h))

def changeTheta(h, X, y, alpha):
    global theta
    thetaRes = [i for i in theta]
    for j in range(len(X[0])):
        #res = alpha * (sum([((y[i] - s(h[i])) * (X[i][j])) for i in range(len(X))])) / len(X)
        thetaRes[j] = theta[j] - alpha * (sum([((s(h[i]) - y[i]) * (X[i][j])) for i in range(len(X))])) / len(X)
    return thetaRes

errores = []

def guardarError(error):
    errores.append(error)

def dibujarError():
    plt.plot([i for i in range(len(errores))], errores)
    plt.show()

def clasificacion(X, y, alpha = 0.5, diferenciaMinima = 0.0001):
    for i in range(len(X)):
        X[i].insert(0,1)
    global theta
    theta = [uniform(0,1) for i in range(len(X[0]))]
    temp = [i for i in theta]
    error = calcularError(y, h(X))
    errorAnterior = 0
    errorAnterior = error
    cont = 0
    while(True):
        theta = changeTheta(h(X), X, y, alpha)
        error = calcularError(y, h(X))
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

x = np.arange(0,1,0.1)

y = [X * (theta[1]/theta[2])*-1 for X in x]


plt.plot(x,y)
plt.plot([i[0] for i in lista],[i[1] for i in lista],'ro')
plt.show()