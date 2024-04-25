import numpy as np
import copy
from scipy.stats import norm
import sys
sys.path.append('/Users/tinchomengo/Desktop/UTN/SIM/simulacionTPs/TP2 Simulacion V2/Distribuciones')
from exponencial import unidor_invervalos


def uniforme(muestra,intervalos,a,b):
    distribucion_uniforme = [0]*len(muestra)
    for i in range(len(distribucion_uniforme)):
        distribucion_uniforme[i] = generar_numeros_aleatorios_uniformes(a,b,muestra[i])

    max = np.max(distribucion_uniforme)
    min = np.min(distribucion_uniforme)
    rango = max - min
    ancho_intervalo = round(rango / intervalos,4)

    #Formato de la matriz matriz_ji_cuadrado [ [ [LI1,LS1] , [LI2,LS2] ] , [FO1,FO2,FO3] , [FE1,FE2,FE3]  ]
    matriz_ji_cuadrado = [[0 for _ in range(intervalos)] for _ in range(2)]
    for i in range (intervalos):
        matriz_ji_cuadrado[0][i] = [0,0]

    #Coloco el primer limite inferior y superior
    matriz_ji_cuadrado[0][0] = [min, round(min+ancho_intervalo,4)]


    #Defino todos los limites inferiores y superiores restantes
    for i in range(1 ,intervalos):
        matriz_ji_cuadrado[0][i][0] = round(matriz_ji_cuadrado[0][i-1][1],4)
        matriz_ji_cuadrado[0][i][1] = round(matriz_ji_cuadrado[0][i][0] + ancho_intervalo,4)
        
    #Coloco el ultimo limite superior para que pueda ser contado correctamente
    matriz_ji_cuadrado[0][-1][1] = max+0.0001

    #Cuento la frecuencia observada
    for i in range(len(distribucion_uniforme)):
        
        for j in range(len(matriz_ji_cuadrado[0])):
            #Verifico si el dato tomado se encuentra dentro del intervalo analizado
            if matriz_ji_cuadrado[0][j][0] <= distribucion_uniforme[i] < matriz_ji_cuadrado[0][j][1]:
                #Si se verifica que se encuentra en el intervalo se suma
                matriz_ji_cuadrado[1][j] += 1
                break
    matriz_ji_cuadrado.append([0 for _ in range(intervalos)])
    frec_esperada_intervalo(len(muestra), intervalos, matriz_ji_cuadrado)
    matriz_intervalos_frecuencias = copy.deepcopy(matriz_ji_cuadrado)

    unidor_invervalos(matriz_ji_cuadrado)
    ji_calc, ji=calcular_ji_cuadrado(matriz_ji_cuadrado)
    tot_fo,tot_fe= sumar_frecuencias(matriz_ji_cuadrado)
    return matriz_ji_cuadrado, matriz_intervalos_frecuencias, distribucion_uniforme, ji_calc, ji,tot_fo,tot_fe


def calcular_ji_cuadrado(matriz):
    ji_cuadrado = 0
    ji = []
    for i in range(len(matriz[0])):
        temp = ((matriz[1][i] - matriz[2][i])**2) / matriz[2][i]
        ji_cuadrado += temp
        ji.append(temp)
    return round(ji_cuadrado,4), ji

def frec_esperada_intervalo(tamaño_muestra, num_intervalos, matriz):
    frecuencia_esperada = round(tamaño_muestra / num_intervalos, 4)
    for i in range(len(matriz[2])):
        matriz[2][i] = frecuencia_esperada

def sumar_frecuencias(matriz):
    total_fo = round(sum(matriz[1]),4)
    total_fe = round(sum(matriz[2]),4)
    return total_fo, total_fe

def generar_numeros_aleatorios_uniformes(a, b, random):
    return round(a + (b - a) * random,4)