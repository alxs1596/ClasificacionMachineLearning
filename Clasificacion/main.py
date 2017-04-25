import sys
import math
from random import uniform, randint
import matplotlib.pyplot as plt
import csv
from normalizar import normalizarMatrizPorColumnas
from normalizar import normalizarLista
lista = []
salidas = []
with open('datos.csv', 'r') as f:
    reader = csv.reader(f)
    lista = list(reader)

for i in range(len(lista)):
    lista[i] = [float(j) for j in lista[i]]
    salidas.append(lista[i][0] - 1)
    del lista[i][0]

lista = normalizarMatrizPorColumnas(lista)

#Separar 0 y 1
l0entrada = [x[0] for x in zip(lista, salidas) if x[1] == 0]
l1entrada = [x[0] for x in zip(lista, salidas) if x[1] == 1]
l0salida = [0 for i in l0entrada]
l1salida = [1 for i in l1entrada]


#cantidad 60%
sesentaPorcientoL0 = int(len(l0entrada) * 0.6)
sesentaPorcientoL1 = int(len(l1entrada) * 0.6)

#separar el 60% y juntar ambas listas
listaEntrenamientoL0entrada = []
listaEntrenamientoL1entrada = []
listaEntrenamientoL0salida = []
listaEntrenamientoL1salida = []
for i in range(sesentaPorcientoL0):
    indice = randint(0, len(l0entrada) - 1)
    listaEntrenamientoL0entrada.append(l0entrada[indice])
    listaEntrenamientoL0salida.append(l0salida[indice])
    del l0entrada[indice]
    del l0salida[indice]

for i in range(sesentaPorcientoL1):
    indice = randint(0, len(l1entrada) - 1)
    listaEntrenamientoL1entrada.append(l1entrada[indice])
    listaEntrenamientoL1salida.append(l1salida[indice])
    del l1entrada[indice]
    del l1salida[indice]


#juntar entradas y salidas
entrada = []
entrada.extend(listaEntrenamientoL0entrada)
entrada.extend(listaEntrenamientoL1entrada)

salida = []
salida.extend(listaEntrenamientoL0salida)
salida.extend(listaEntrenamientoL1salida)

#Desordenar

nuevaEntrada = []
nuevaSalida = []
for i in range(len(entrada)):
    indice = randint(0,len(entrada) - 1)
    nuevaEntrada.append(entrada[indice])
    nuevaSalida.append(salida[indice])
    
entrada = nuevaEntrada
salida = nuevaSalida


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

clasificacion(entrada, salida)
#theta = [3.413676059618291, -4.289545087626268, -0.7075238260278812, -2.024294876232655, 3.8311769222181593, -0.4377084582797507, 0.29654066315614885, -0.7715957195798608, 2.475304245763588, 2.0371205439115334, -1.8159204800062063, 1.5551438290254826, -0.5534141027398616, -6.498541675952927]


print ("Prueba")

_0_0 = 0
_0_1 = 0
_1_0 = 0
_1_1 = 0

for i in range(len(l0entrada)):
    res = 0
    if (prediccion(l0entrada[i]) >= 0.5):
        res = 1
        _0_1 = _0_1 + 1
    else:
        _0_0 = _0_0 + 1
    print(l0salida[i], end=" - ")
    print(res)

for i in range(len(l1entrada)):
    res = 0
    if (prediccion(l1entrada[i]) >= 0.5):
        res = 1
        _1_1 = _1_1 + 1
    else:
        _1_0 = _1_0 + 1
    print(l1salida[i], end=" - ")
    print(res)


def porcentaje(num, total):
    return (num*100)/total

print("---------------")

print(_0_0 , end="\t")
print(_0_1)
print(_1_0 , end="\t") 
print(_1_1)

print("---------------")

print(porcentaje(_0_0, len(l0entrada)) , end="\t")
print(porcentaje(_0_1, len(l0entrada)))
print(porcentaje(_1_0, len(l1entrada)) , end="\t") 
print(porcentaje(_1_1, len(l1entrada)))

print("Porcentaje de precision: ")
print((porcentaje(_0_0, len(l0entrada)) + porcentaje(_1_1, len(l1entrada)))/2)

dibujarError()