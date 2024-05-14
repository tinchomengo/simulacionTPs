import random
def simulacion(tupla_probs):
    # Estructura tupla ((probAutos), (probCategoria), (probComisionMediano), (probComisionDeLujo), (probSorteo), (valor_i, valor_j), semanas)
    filas_guardadas = []
    semanas_guardadas = []
    comisiones_promedio_guardadas = []
    
    #Estructura de las filas (hacer todos -1)
    #0 [RndDemanda,Demanda],
    #1 [[RndAuto1,"tipo"],[RndAuto2,"tipo"],[RndAuto3,"tipo"],[RndAuto4,"tipo"]],
    #2 [[ComisionAuto1, cantidadComision1],[ComisionAuto2, cantidadComision2],[ComisionAuto3, cantidadComision3],[ComisionAuto4, cantidadComision4]],
    #3 [RndSorteo,"ResSorteo"],
    #4 ComisionFila,
    #5 ComisionAcumulada,
    #6 ComisionPromedio]

    fila = [[[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0]],[[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0]]]
    fila_usar = 0
    fila_no_usar = 1
    acumulador_vendidos = 0
    ganada = False
    for semana in range(tupla_probs[6]):
        for empleado in range(4):
            #Determinar Demanda
            fila[fila_usar][empleado][0][0] = round(random.uniform(0,0.9999),4)
            fila[fila_usar][empleado][0][1] = funcionBuscar(tupla_probs[0], fila[fila_usar][empleado][0][0])
            acumulador_vendidos += fila[fila_usar][empleado][0][1]
            #Determinar autos y comisiones
            if(fila[fila_usar][empleado][0][1]>0):
                for i in range(fila[fila_usar][empleado][0][1]): #Estoy utilizando la demanda solicitada para recorrer y cambiar el array de autos y comisiones
                    # Determino el tipo de auto
                    fila[fila_usar][empleado][1][i][0] = round(random.uniform(0,0.9999),4)
                    fila[fila_usar][empleado][1][i][1] = funcionBuscar(tupla_probs[1], fila[fila_usar][empleado][1][i][0]) 
                    # Determino la comision segun tipo de auto
                    if(fila[fila_usar][empleado][1][i][1] == "compacto"):
                        fila[fila_usar][empleado][2][i][0] = 0
                        fila[fila_usar][empleado][2][i][1] = 250
                    elif (fila[fila_usar][empleado][1][i][1] == "mediano"):
                        fila[fila_usar][empleado][2][i][0] = round(random.uniform(0,0.9999),4)
                        fila[fila_usar][empleado][2][i][1] = funcionBuscar(tupla_probs[2], fila[fila_usar][empleado][2][i][0])
                    elif (fila[fila_usar][empleado][1][i][1] == "de lujo"):
                        fila[fila_usar][empleado][2][i][0] = round(random.uniform(0,0.9999),4)
                        fila[fila_usar][empleado][2][i][1] = funcionBuscar(tupla_probs[3], fila[fila_usar][empleado][2][i][0])
                        
                    


            # Determinar comision total de la fila
            for i in range(4):
                fila[fila_usar][empleado][4] += fila[fila_usar][empleado][2][i][1]

            # Si es una cuarta semana, se realiza el sorteo      
            if((semana+1)%4 == 0) and ganada == False:
                if(acumulador_vendidos >=4):
                    fila[fila_usar][empleado][3][0] = round(random.uniform(0,0.9999),4)
                    fila[fila_usar][empleado][3][1] = funcionBuscar(tupla_probs[4], fila[fila_usar][empleado][3][0])
                    if(fila[fila_usar][empleado][3][1] == "Gana el sorteo"):
                        ganada = True
                        fila[fila_usar][empleado][4] += 5000
                else:
                    fila[fila_usar][empleado][3][1] = "No aplica"
                acumulador_vendidos = 0

            #Comision Acumulado
            fila[fila_usar][empleado][5] = (fila[fila_no_usar][empleado][5] + fila[fila_usar][empleado][4])

            #Comision Promedio
            #fila[fila_usar][empleado][7] = round(fila[fila_usar][empleado][5]/semana+1,4) |no hay mas 7

        if((tupla_probs[5][1]+tupla_probs[5][0] > semana >= tupla_probs[5][0]) or semana == tupla_probs[6]-1):
            filas_guardadas.append((fila[fila_usar]))
            semanas_guardadas.append(semana+1)
            comisiones_promedio_guardadas.append(calcular_comision_promedio(fila[fila_usar], semana+1))
        fila[fila_no_usar] = reiniciar_fila()

        if(fila_usar == 0):
            fila_usar = 1
            fila_no_usar = 0
        else:
            fila_usar = 0
            fila_no_usar = 1
        ganada = False
    
    return filas_guardadas, semanas_guardadas, comisiones_promedio_guardadas

def funcionBuscar(tupla_determinar, rnd):
    acumulador = 0
    
    for i in range(len(tupla_determinar)):
        valor_comparar = tupla_determinar[i][0]/100
        
        if i == 0:
            if rnd < valor_comparar:
                return tupla_determinar[i][1]
        else:
            if acumulador <= rnd < valor_comparar+acumulador:
                return tupla_determinar[i][1]
        acumulador += valor_comparar

def reiniciar_fila():
    return [[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0],[[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0]]


def calcular_comision_promedio(fila, semana):
    comision_acumulada_todos = 0
    for empleado in range(4):
        comision_acumulada_todos += fila[empleado][5]
    return round(comision_acumulada_todos/semana,4)
    

simulacion((((20, 0), (30, 1), (30, 2), (15, 3), (5, 4)), ((50, 'compacto'), (35, 'mediano'), (15, 'de lujo')), ((40, 400), (60, 500)), ((35, 1000), (40, 1500), (25, 2000)), ((30, 'Gana el sorteo'), (70, 'No gana el sorteo')), (0, 10), 100000))

