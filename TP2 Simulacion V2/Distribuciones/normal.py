import numpy as np
import copy
from scipy.stats import norm


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
    #Formato de la matriz matriz_intervalos_frecuencias [      [ [LI1,LS1]  ,  [LI2,LS2] ]         ,      [FO1,FO2,FO3]]
    
    #matriz_intervalos_frecuencias = copy.deepcopy(matriz_ji_cuadrado)
    
    matriz_ji_cuadrado.append([0 for _ in range(cantidad_intervalos)])
    for i in range(cantidad_intervalos):
        matriz_ji_cuadrado[2][i] = round(((frec_esperada_intervalo(matriz_ji_cuadrado[0][i][1], media,desviacion) - frec_esperada_intervalo(matriz_ji_cuadrado[0][i][0], media,desviacion))*len(dist_normal)),4)
    unidor_invervalos(matriz_ji_cuadrado)

    contador = 0
    for i in range(len(matriz_ji_cuadrado[2])):
        contador += matriz_ji_cuadrado[2][i]


    ji_calc, ji=calcular_ji_cuadrado(matriz_ji_cuadrado)
    return matriz_ji_cuadrado, dist_normal, ji_calc, ji


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
        #print("Numeros normales ->", numeros_normales)
    
    if (muestra % 2) != 0:
        RND1 = np.random.uniform(0,1)
        RND2 = np.random.uniform(0,1)
        N1 = round(((np.sqrt((-2) * np.log(RND1)) * np.cos(2 * np.pi * RND2)) * desviacion) + media, 4)    
        # Agregar N1 y N2 a la lista de números normales generados
        numeros_normales.append(N1)
    return numeros_normales

def frec_esperada_intervalo(limite,media, desviacion):
    return(round(norm.cdf(limite, loc=media, scale=desviacion),4))
def unidor_invervalos(matriz):
    # Iterar sobre los intervalos
    i = 0
    while i < len(matriz[0]) - 1:
        # Verificar si la frecuencia esperada actual es menor a 5
        if matriz[2][i] < 5:
            # Inicializar la suma de frecuencias esperadas y el índice para el próximo intervalo
            suma_frecuencias = matriz[2][i]
            suma_frecuencias_observadas = matriz[1][i]
            j = i + 1
            # Iterar sobre los intervalos restantes
            while j < len(matriz[0]):
                # Sumar la frecuencia esperada y la observada del próximo intervalo
                suma_frecuencias += matriz[2][j]
                suma_frecuencias_observadas += matriz[1][j]
                # Verificar si la suma alcanza o supera 5
                if suma_frecuencias >= 5:
                    # Actualizar los datos del primer intervalo
                    matriz[0][i][1] = matriz[0][j][1]
                    matriz[1][i] = suma_frecuencias_observadas  # Actualizar frecuencia observada
                    matriz[2][i] = suma_frecuencias  # Actualizar frecuencia esperada
                    # Eliminar los intervalos agrupados
                    del matriz[0][i + 1:j + 1]
                    del matriz[1][i + 1:j + 1]
                    del matriz[2][i + 1:j + 1]
                    # Reiniciar el índice para la siguiente iteración
                    i = 0
                    break
                j += 1
            # Si no se encontró un intervalo adicional para agrupar, salir del bucle
            else:
                break
        else:
            i += 1

    # Verificar si el último intervalo tiene frecuencia esperada menor a 5
    if matriz[2][-1] < 5:
        # Agrupar con el intervalo anterior hasta que la frecuencia esperada sea igual o mayor a 5
        i = len(matriz[0]) - 2
        while i >= 0:
            if matriz[2][i] >= 5:
                break
            else:
                matriz[0][i][1] = matriz[0][i + 1][1]  # Fusionar intervalos
                matriz[1][i] += matriz[1][i + 1]  # Actualizar frecuencia observada
                matriz[2][i] += matriz[2][i + 1]  # Actualizar frecuencia esperada
                # Eliminar el último intervalo
                del matriz[0][-1]
                del matriz[1][-1]
                del matriz[2][-1]
            i -= 1

    # Si el último intervalo sigue siendo menor a 5, agruparlo con el penúltimo
    if matriz[2][-1] < 5 and len(matriz[0]) > 1:
        matriz[0][-2][1] = matriz[0][-1][1]  # Fusionar intervalos
        matriz[1][-2] += matriz[1][-1]  # Actualizar frecuencia observada
        matriz[2][-2] += matriz[2][-1]  # Actualizar frecuencia esperada
        # Eliminar el último intervalo
        del matriz[0][-1]
        del matriz[1][-1]
        del matriz[2][-1]

    return matriz




