import numpy as np
import copy
from scipy.stats import norm
import sys
sys.path.append('C:/Users/matpo/Desktop/TP/simulacionTPs/TP2 Simulacion V2/Distribuciones')
from exponencial import unidor_invervalos


def normal(muestra,cantidad_intervalos ,media,desviacion):
    dist_normal = [0]*muestra
    dist_normal = generador_numeros_normales(muestra,media,desviacion )

    max = np.max(dist_normal)
    min = np.min(dist_normal)
    media = np.mean(dist_normal)
    rango = max - min
    ancho_intervalo = round(rango / cantidad_intervalos,4)

    #Formato de la matriz matriz_ji_cuadrado [ [ [LI1,LS1] , [LI2,LS2] ] , [FO1,FO2,FO3] , [FE1,FE2,FE3]  ]
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
    for i in range(len(dist_normal)):
        
        for j in range(len(matriz_ji_cuadrado[0])):
            #Verifico si el dato tomado se encuentra dentro del intervalo analizado
            if matriz_ji_cuadrado[0][j][0] <= dist_normal[i] < matriz_ji_cuadrado[0][j][1]:
                #Si se verifica que se encuentra en el intervalo se suma
                matriz_ji_cuadrado[1][j] += 1
                break
    matriz_ji_cuadrado.append([0 for _ in range(cantidad_intervalos)])
    for i in range(cantidad_intervalos):
        matriz_ji_cuadrado[2][i] = round(((frec_esperada_intervalo(matriz_ji_cuadrado[0][i][1], media,desviacion) - frec_esperada_intervalo(matriz_ji_cuadrado[0][i][0], media,desviacion))*len(dist_normal)),4)
    unidor_invervalos(matriz_ji_cuadrado)
    ji_calc, ji=calcular_ji_cuadrado(matriz_ji_cuadrado)
    tot_fo,tot_fe= sumar_frecuencias(matriz_ji_cuadrado)
    return matriz_ji_cuadrado, dist_normal, ji_calc, ji,tot_fo,tot_fe


def calcular_ji_cuadrado(matriz):
    ji_cuadrado = 0
    ji = []
    for i in range(len(matriz[0])):
        temp = ((matriz[1][i] - matriz[2][i])**2) / matriz[2][i]
        ji_cuadrado += temp
        ji.append(temp)
    return round(ji_cuadrado,4), ji


def generador_numeros_normales(muestra, media, desviacion):
    # Usamos metodo de Box-Muller
    numeros_normales = []
    if (muestra>1000000):
        return -1
    

    for _ in range(muestra // 2):
        # Generar dos números aleatorios uniformemente distribuidos entre 0 y 1
        RND1 = np.random.uniform(0,1)
        RND2 = np.random.uniform(0,1)
        
        # Calcular N1 y N2 usando las fórmulas corregidas
        N1 = round(((np.sqrt((-2) * np.log(RND1)) * np.cos(2 * np.pi * RND2)) * desviacion) + media, 4)
        N2 = round(((np.sqrt((-2) * np.log(RND1)) * np.sin(2 * np.pi * RND2)) * desviacion) + media, 4)
    
        # Agregar N1 y N2 a la lista de números normales generados
        numeros_normales.append(N1)
        numeros_normales.append(N2)
    
    if (muestra % 2) != 0:
        RND1 = np.random.uniform(0,1)
        RND2 = np.random.uniform(0,1)
        N1 = round(((np.sqrt((-2) * np.log(RND1)) * np.cos(2 * np.pi * RND2)) * desviacion) + media, 4)    
        # Agregar N1 y N2 a la lista de números normales generados
        numeros_normales.append(N1)
    return numeros_normales

def frec_esperada_intervalo(limite,media, desviacion):
    return(round(norm.cdf(limite, loc=media, scale=desviacion),4))

def sumar_frecuencias(matriz):
    total_fo = round(sum(matriz[1]),4)
    total_fe = round(sum(matriz[2]),4)
    return total_fo, total_fe



