import math
import numpy as np
import copy


def exponencial(muestra, cantidad_intervalos, lambda_dato):
    distExponencial = [0]*len(muestra)
    for i in range(len(distExponencial)):
        distExponencial[i] = generador_exponenciales(lambda_dato, muestra[i])
    max = np.max(distExponencial)
    min = np.min(distExponencial)
    rango = max - min
    ancho_intervalo = round(rango / cantidad_intervalos,4)

    #Formato de la matriz matriz_ji_cuadrado [      [ [LI1,LS1]  ,  [LI2,LS2] ]         ,      [FO1,FO2,FO3]       ,       [FE1,FE2,FE3]  ]
    matriz_ji_cuadrado = [[0 for _ in range(cantidad_intervalos)] for _ in range(2)]
    for i in range (cantidad_intervalos):
        matriz_ji_cuadrado[0][i] = [0,0]

    #Coloco el primer limite inferior y superior
    matriz_ji_cuadrado[0][0] = [min, round(min+ancho_intervalo,4)]


    #Defino todos los limites inferiores y superiores restantes
    for i in range(1 ,cantidad_intervalos):
        matriz_ji_cuadrado[0][i][0] = round(matriz_ji_cuadrado[0][i-1][1],4)
        matriz_ji_cuadrado[0][i][1] = round(matriz_ji_cuadrado[0][i][0] + ancho_intervalo,4)
        
    #Coloco el ultimo limite superior para que pueda ser contado correctamente
    matriz_ji_cuadrado[0][-1][1] = max+0.0001


    #Cuento la frecuencia observada
    for i in range(len(distExponencial)):
        
        for j in range(len(matriz_ji_cuadrado[0])):
            #Verifico si el dato tomado se encuentra dentro del intervalo analizado
            if matriz_ji_cuadrado[0][j][0] <= distExponencial[i] < matriz_ji_cuadrado[0][j][1]:
                #Si se verifica que se encuentra en el intervalo se suma
                matriz_ji_cuadrado[1][j] += 1
                break
    #Formato de la matriz matriz_intervalos_frecuencias [      [ [LI1,LS1]  ,  [LI2,LS2] ]         ,      [FO1,FO2,FO3]]
    
    #matriz_intervalos_frecuencias = copy.deepcopy(matriz_ji_cuadrado)

    
    matriz_ji_cuadrado.append([0 for _ in range(cantidad_intervalos)])
    for i in range(cantidad_intervalos):
        matriz_ji_cuadrado[2][i] = round(((frec_esperada_intervalo(matriz_ji_cuadrado[0][i][1], lambda_dato) - frec_esperada_intervalo(matriz_ji_cuadrado[0][i][0], lambda_dato))*len(distExponencial)),4)
    print(matriz_ji_cuadrado)
    unidor_invervalos(matriz_ji_cuadrado)
    ji_cuadrado, ji = calcular_ji_cuadrado(matriz_ji_cuadrado)
    
    return matriz_ji_cuadrado, distExponencial, ji_cuadrado, ji


def calcular_ji_cuadrado(matriz):
    ji_cuadrado = 0
    ji = []
    for i in range(len(matriz[0])):
        temp = ((matriz[1][i] - matriz[2][i])**2) / matriz[2][i]
        ji_cuadrado += temp
        ji.append(temp)
    return round(ji_cuadrado,4), ji

def generador_exponenciales(lambda_dato, rnd):
    return round((-1 / lambda_dato) * (math.log(1 - rnd)),4)

def frec_esperada_intervalo(x, lambda_dato):
    return (1 - math.exp(-lambda_dato * x))

def eliminar_intervalos(matriz, posicion):
    matriz[0].pop(posicion)
    matriz[1].pop(posicion)
    matriz[2].pop(posicion)
    
def unidor_invervalos(matriz):
    sumar_frec_obs = 0
    sumar_frec_esp = 0
    i = 0
    j = i+1
    sigue_buscando_intervalo1 = True
    sigue_buscando_intervalo2 = True

    #Recorro el array con un while para evitar problemas de indexacion y poder manejar mas a gusto el indice
    while sigue_buscando_intervalo1:
        
        #Solo muevo el i cuando ya se juntaron valores o se saltearon valores
        if (matriz[2][i]) < 5:
            #Si si, entonces empiezo a buscar el intervalo con el que se combinara
            sigue_buscando_intervalo2 = True
            while sigue_buscando_intervalo2:
                if j == len(matriz[2]) and sumar_frec_esp+matriz[2][i] < 5:
                    matriz[0][i-1][1] = matriz[0][i][1]
                    sumar_frec_obs += matriz[1][i]
                    sumar_frec_esp += matriz[2][i]
                    matriz[1][i-1] += sumar_frec_obs
                    matriz[2][i-1] += sumar_frec_esp
                    eliminar_intervalos(matriz, i)
                    sigue_buscando_intervalo2 = False
                    sigue_buscando_intervalo1 = False
                    continue

                if j == len(matriz[2]) and sumar_frec_esp+matriz[2][i] >= 5:
                    matriz[1][i] += sumar_frec_obs
                    matriz[2][i] += sumar_frec_esp
                    eliminar_intervalos(matriz, i)
                    sigue_buscando_intervalo2 = False
                    sigue_buscando_intervalo1 = False
                    continue

                #Si el valor actual mas el siguiente es mayor o igual a 5, significa que debere asignar el limite inferior al intervalo actual (el limite superior estara dado por el intervalo i actual)
                if (sumar_frec_esp+matriz[2][i]) >= 5:
                    matriz[0][i][1] = matriz[0][j][1]
                    matriz[1][i] += sumar_frec_obs
                    matriz[2][i] += sumar_frec_esp
                    sigue_buscando_intervalo2 = False
                    
                    sumar_frec_obs = 0
                    sumar_frec_esp = 0

                    sumar_frec_obs = matriz[1][j]
                    sumar_frec_esp = matriz[2][j]

                    eliminar_intervalos(matriz, j)
                    continue

                sumar_frec_obs += matriz[1][j]
                sumar_frec_esp += matriz[2][j]
                matriz[0][j-1][1] = matriz[0][j][1]
                eliminar_intervalos(matriz, j)
        if i+1 == len(matriz[2]):
            sigue_buscando_intervalo1 = False
            continue
        else:
            i += 1
            j = i+1