
def normalizarMatrizPorColumnas(matriz):
    # matriz = lista de listas
    transpuesta = []
    for i in zip(*matriz):
        transpuesta.append(list(i))
    for i in range(len(transpuesta)):
        mayor = max(transpuesta[i])
        menor = min(transpuesta[i])
        for j in range(len(transpuesta[i])):
            transpuesta[i][j] = (transpuesta[i][j] - menor) / (mayor - menor)
    res = []
    for i in zip(*transpuesta):
        res.append(list(i))
    return res

def normalizarLista(lista):
    mayor = max(lista)
    menor = min(lista)
    for i in range(len(lista)):
        lista[i] = (lista[i] - menor) / (mayor - menor)
    return lista