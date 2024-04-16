import random

def generar_numeros_aleatorios_uniformes(a, b, tamaño_muestra):
    return round(a + (b - a) * random.uniform(0,1),4)

def calcular_intervalos(datos, num_intervalos):
    min_valor = min(datos)
    max_valor = max(datos)    
    intervalo_ancho = (max_valor - min_valor) / num_intervalos
    intervalos = [round(min_valor + i * intervalo_ancho,4) for i in range(num_intervalos)]
    intervalos.append(round((max_valor),4))
    return intervalos

def calcular_frecuencias(datos, intervalos):
    frecuencias = [0] * (len(intervalos) - 1)  # Se usa (len(intervalos) - 1) para excluir el intervalo adicional
    
    for dato in datos:
        for i in range(len(intervalos) - 1):  # Se itera hasta el penúltimo intervalo
            if intervalos[i] <= dato < intervalos[i + 1]:
                frecuencias[i] += 1
                break
    frecuencias[-1]+=1
    return frecuencias

def ji_cuadrado_observado(frecuencias_obs, frecuencias_esp):
    return round(sum((frec_obs - frec_esp)**2 / frec_esp for frec_obs, frec_esp in zip(frecuencias_obs, frecuencias_esp)),4)

def generar_frecuencias_esperadas(tamaño_muestra, num_intervalos):
    frecuencia_esperada = round(len(tamaño_muestra) / num_intervalos, 4)
    frecuencias_esperadas = [frecuencia_esperada] * num_intervalos
    
    # Iteracion
    i = 0
    while i < len(frecuencias_esperadas) - 1:
        # Si la frecuencia esperada actual es menor a 5 y hay un elemento siguiente
        if frecuencias_esperadas[i] < 5 and i + 1 < len(frecuencias_esperadas):
            # Sumamos la frecuencia esperada del siguiente elemento
            frecuencias_esperadas[i] += frecuencias_esperadas[i + 1]
            # Eliminamos el siguiente elemento
            frecuencias_esperadas.pop(i + 1)
        else:
            i += 1
    
    # Verificar si el último elemento es menor a 5 y sumarlo al elemento anterior si es necesario
    if frecuencias_esperadas[-1] < 5 and len(frecuencias_esperadas) > 1:
        frecuencias_esperadas[-2] += frecuencias_esperadas[-1]
        del frecuencias_esperadas[-1]
    
    return len(frecuencias_esperadas), frecuencias_esperadas

def calcular_frecuencia_observada(datos, intervalos):
    frecuencias_obs = [0] * (len(intervalos) - 1)
    
    for dato in datos:
        for i, (limite_inferior, limite_superior) in enumerate(intervalos):
            if (limite_inferior <= dato) and (dato < limite_superior):
                frecuencias_obs[i] += 1
                break

    return frecuencias_obs



def uniforme(tamaño_muestra,intervalos,a,b):
    distribucion_uniforme = [0]*len(tamaño_muestra)
    for i in range(len(distribucion_uniforme)):
        distribucion_uniforme[i] = generar_numeros_aleatorios_uniformes(a,b,tamaño_muestra[i])
    # Generar números aleatorios uniformes
    #Verificar Frecuencias esperadas < 5 y generar nuevos intervalos
    num_intervalos, frecuencias_esperadas = generar_frecuencias_esperadas(tamaño_muestra, intervalos)
    
    # Calcular intervalos y frecuencias
    intervalos_calculados = calcular_intervalos(distribucion_uniforme, num_intervalos)
    frecuencias_observadas = calcular_frecuencias(distribucion_uniforme, intervalos_calculados)
    

    # Calcular chi-cuadrado
    ji_cuadrado = ji_cuadrado_observado(frecuencias_observadas, frecuencias_esperadas)


    intervalos_uniforme = [
        [[intervalos_calculados[i], intervalos_calculados[i + 1]] for i in range(len(intervalos_calculados) - 1)],
        frecuencias_observadas,
        frecuencias_esperadas
    ]

    return intervalos_uniforme,distribucion_uniforme,ji_cuadrado



