import random
import copy
def simulacion(tupla_probs):
    # Estructura tupla ((probAutos), (probCategoria), (probComisionMediano), (probComisionDeLujo), (probSorteo), (valor_i, valor_j), semanas)

    filas_guardadas = []
    #Estructura de las filas 
    #0 [[Semana,
    #1 [RndDemanda,Demanda],
    #2 [[RndAuto1,"tipo"],[RndAuto2,"tipo"],[RndAuto3,"tipo"],[RndAuto4,"tipo"]],
    #3 [[ComisionAuto1, cantidadComision1],[ComisionAuto2, cantidadComision2],[ComisionAuto3, cantidadComision3],[ComisionAuto4, cantidadComision4]],
    #4 [RndSorteo,"ResSorteo"],
    #5 ComisionFila,
    #6 ComisionAcumulada,
    #7 ComisionPromedio]

    fila = [[0,[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0,0] , [0,[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0,0]]
    fila_usar = 0
    fila_no_usar = 1
    acumulador_vendidos = 0
    for semana in range(tupla_probs[6]):
        #Cambiar semana
        fila[fila_usar][0] = semana+1
        #Determinar Demanda
        fila[fila_usar][1][0] = round(round(random.random(),4),4)
        fila[fila_usar][1][1] = funcionBuscar(tupla_probs[0], fila[fila_usar][1][0])
        acumulador_vendidos = fila[fila_usar][1][1]
        #Determinar autos y comisiones
        for i in range(fila[fila_usar][1][1]): #Estoy utilizando la demanda solicitada para recorrer y cambiar el array de autos y comisiones
            # Determino el tipo de auto
            fila[fila_usar][2][i][0] = round(random.random(),4)
            fila[fila_usar][2][i][1] = funcionBuscar(tupla_probs[1], fila[fila_usar][2][i][0]) 
            # Determino la comision segun tipo de auto
            if(fila[fila_usar][2][i][1] == "compacto"):
                fila[fila_usar][3][i][0] = 0
                fila[fila_usar][3][i][1] = 250
            elif (fila[fila_usar][2][i][1] == "mediano"):
                fila[fila_usar][3][i][0] = round(random.random(),4)
                fila[fila_usar][3][i][1] = funcionBuscar(tupla_probs[2], fila[fila_usar][3][i][0])
            elif (fila[fila_usar][2][i][1] == "de lujo"):
                fila[fila_usar][3][i][0] = round(random.random(),4)
                fila[fila_usar][3][i][1] = funcionBuscar(tupla_probs[3], fila[fila_usar][3][i][0])
            # Si es una cuarta semana, se realiza el sorteo
            fila[fila_usar][5] += fila[fila_usar][3][i][1]
            if(semana%4 == 0):
                if(acumulador_vendidos >=4):
                    fila[fila_usar][4][0] = round(random.random(),4)
                    fila[fila_usar][4][1] = funcionBuscar(tupla_probs[4], fila[fila_usar][4][0])
                    if(fila[fila_usar][4][1] == "Gana el sorteo"):
                        fila[fila_usar][5] += 5000
                acumulador_vendidos = 0
            #Comision Acumulado
            fila[fila_usar][6] = (fila[fila_no_usar][6] + fila[fila_usar][5])
            #Comision Promedio
            fila[fila_usar][7] = fila[fila_usar][6]/fila[fila_usar][0]

        if((tupla_probs[5][1]+tupla_probs[5][0] > semana >= tupla_probs[5][0]) or semana == tupla_probs[6]-1):
            filas_guardadas.append(copy.copy(fila[fila_usar]))
            print(fila[fila_usar])

        reiniciar_fila(fila[fila_no_usar])

        if(fila_usar == 0):
            fila_usar = 1
            fila_no_usar = 0
        else:
            fila_usar = 0
            fila_no_usar = 1


def funcionBuscar(tupla_determinar, rnd):
    acumulador = 0
    for i in range(len(tupla_determinar)):
        
        if i == 0:
            if rnd < tupla_determinar[i][0]/100:
                return tupla_determinar[i][1]
        else:
            if acumulador <= rnd < tupla_determinar[i][0]/100+acumulador:
                return tupla_determinar[i][1]
        acumulador += tupla_determinar[i][0]/100

def reiniciar_fila(fila):
    fila = [0,[0,0],[[0,""],[0,""],[0,""],[0,""]],[[0,0],[0,0],[0,0],[0,0]],[0,""],0,0,0]