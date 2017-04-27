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
    return sum([e[0]*(e[1]**2) for e in zip(v1,v2)])

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
        thetaRes[j] = theta[j] - (alpha * (sum([((s(h[i]) - y[i]) * (X[i][j])**2) for i in range(len(X))])) / len(X))# + (parametroR/len(y))*theta[j]
    return thetaRes

errores = []

def guardarError(error):
    errores.append(error)

def dibujarError():
    plt.plot([i for i in range(len(errores))], errores)
    plt.show()

def clasificacion(X, y,_grado = 1, parametroR = 0.99, alpha = 0.5, diferenciaMinima = 0.000001):
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
#theta = [-0.8558798606792295, 7.881821356390523, -6.022845328731978]


#print ("Prueba")

#for i in range(len(pruebaEntrada)):
#    res = 0
#    if (prediccion(pruebaEntrada[i]) >= 0.5):
#        res = 1
#    print(pruebaSalida[i], end=" - ")
#    print(res)

#print(theta)

#x = np.arange(0,1,0.1)

#y = [X * (theta[1]/theta[2])*-1 for X in x]


#plt.plot(x,y)
#plt.plot([i[1] for i in lista],[i[2] for i in lista],'ro')
#plt.show()

entrada = []
salida = []

def norm(x):
    return x/500
def desnorm(n):
    return n*500


root = Tk()


var = StringVar()
var.set("#00FF00")
R1 = Radiobutton(root, text="Rojo", variable=var, value = "#FF0000")
R2 = Radiobutton(root, text="Verde", variable=var, value = "#00FF00")
R1.pack(anchor=W)
R2.pack(anchor=W)

#frame = Frame(root, width=500,height=500)
#frame.pack()

def dibujarPunto(canvas, x, y, color, radio = 5):
    x1, y1 = (x - radio), (y - radio)
    x2, y2 = (x + radio), (y + radio)
    canvas.create_oval(x1, y1, x2, y2, fill = color)

def guardarPunto(x,y, s):
    global entrada, salida
    entrada.append([norm(x),norm(y)])
    salida.append(s)

procesado = False

def callback(event):
    global procesado
    if procesado == False:
        s = 1 #verde
        if var.get() == "#FF0000":
            s = 0 # rojo
        print("x: " + str(event.x) + " y: " + str(event.y))
        color = var.get()
        dibujarPunto(canvas, event.x, event.y, color)
        guardarPunto(event.x, event.y, s)
    else:
        s = prediccion([norm(event.x), norm(event.y)])
        if s >= 0.5:
            s = 1
        else:
            s = 0
        print(s)
        color = ""
        if s == 1:
            color = "#00FF00"
        elif s== 0:
            color = "#FF0000"
        dibujarPunto(canvas, event.x, event.y, color)

def dibujarLineas(canvas, X, Y):
    m = len(X)
    for i in range(m-1):
        canvas.create_line(X[i], Y[i], X[i+1], Y[i+1])


canvas = Canvas(root, width=500, height=500)
#canvas.create_line(15,15,515,15)
#canvas.create_line(15,515,515,515)
#canvas.create_line(15,15,15,515)
#canvas.create_line(515,15,515,515)
canvas.config(highlightbackground="#202020")
#dibujarPunto(canvas, 265, 265)

canvas.bind("<Button-1>", callback)
canvas.pack()

entrada = [[0.516, 0.422], [0.488, 0.416], [0.466, 0.418], [0.452, 0.432], [0.436, 0.452], [0.432, 0.466], [0.428, 0.492], [0.43, 0.506], [0.442, 0.514], [0.46, 0.526], [0.476, 0.528], [0.496, 0.53], [0.518, 0.53], [0.53, 0.524], [0.544, 0.502], [0.548, 0.488], [0.548, 0.46], [0.536, 0.438], [0.51, 0.43], [0.488, 0.432], [0.464, 0.452], [0.458, 0.478], [0.464, 0.484], [0.486, 0.488], [0.512, 0.484], [0.496, 0.438], [0.474, 0.448], [0.492, 0.488], [0.504, 0.504], [0.518, 0.506], [0.526, 0.486], [0.514, 0.448], [0.5, 0.45], [0.49, 0.474], [0.37, 0.216], [0.342, 0.224], [0.298, 0.258], [0.274, 0.288], [0.258, 0.318], [0.248, 0.344], [0.232, 0.388], [0.22, 0.436], [0.216, 0.474], [0.216, 0.51], [0.226, 0.558], [0.24, 0.586], [0.26, 0.618], [0.28, 0.634], [0.32, 0.662], [0.36, 0.676], [0.392, 0.686], [0.426, 0.696], [0.448, 0.702], [0.488, 0.704], [0.532, 0.708], [0.572, 0.704], [0.598, 0.7], [0.636, 0.688], [0.67, 0.664], [0.68, 0.654], [0.698, 0.624], [0.708, 0.602], [0.728, 0.568], [0.732, 0.542], [0.732, 0.514], [0.734, 0.486], [0.73, 0.454], [0.712, 0.412], [0.694, 0.376], [0.668, 0.336], [0.64, 0.306], [0.612, 0.286], [0.58, 0.266], [0.55, 0.244], [0.524, 0.242], [0.458, 0.218], [0.412, 0.21], [0.49, 0.222]]
salida = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

minimoX = min([i[0] for i in entrada])
maximoX = max([i[0] for i in entrada])
minimoY = min([i[1] for i in entrada])
maximoY = max([i[1] for i in entrada])

def a(X):
        res = -1*((math.fabs(theta[0]) + theta[1]*X**2)/theta[2])
        print(X)
        print(res)
        return res
   
def btnClick(event):
    global entrada, salida, procesado
    #print(entrada)
    #print(salida)
    clasificacion(entrada,salida)
    print(theta)
    procesado = True

    x = np.arange(minimoX,maximoX,0.1)
    #y = [X * (theta[1]/theta[2])*-1 for X in x]
    #y = [theta[0] + theta[2] * X for X in x]
    y = [math.sqrt(a(X)) for X in x]
    

    plt.plot(x,y)
    plt.plot([i[1] for i in entrada],[i[2] for i in entrada],'ro')

    #x = [desnorm(i) for i in x]
    #y = [desnorm(i) for i in y]
    #dibujarLineas(canvas, x, y)

    plt.show()

    

b = Button(root, text="Procesar")
b.bind("<Button-1>", btnClick)
b.pack()


root.mainloop()