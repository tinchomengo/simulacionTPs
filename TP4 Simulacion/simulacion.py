import random
import math
import copy
    # 0  - tiempoSimulacion
    # 1  - nroIteraciones
    # 2  - horaGuardado
    # 3  - llegada
    # 4  - prob Tipo
    # 5  - prob unaHoras
    # 6 - tiempo Cobro

class Auto:
    def __init__(self, id, tipo, hora_llegada,fin_estacionamiento, fin_cobro):
        self.id = id
        self.tipo = tipo
        self.estado = "Estacionado"
        self.hora_llegada = hora_llegada
        self.hora_fin_estacionamiento = fin_estacionamiento
        self.hora_fin_cobro = fin_cobro

    def __repr__(self):
        return f"Auto(id={self.id}, tipo={self.tipo}, estado={self.estado}, hora_llegada={self.hora_llegada}, fin_estacionamiento={self.hora_fin_estacionamiento}, fin_cobro={self.hora_fin_cobro})"

def simulacion(datos):
    bandera_primero=True
    id_primero=0
    lista_coches=[]
    iteraciones_guardadas = []
    coches = []
    id_colas = []
    coche_id = 0
    prox_llegada_almacenada = None
    usar_prox_llegada_almacenada = False
    contador_guardados = 0
    finalizar_simulacion = False
    primera_iteracion = True
    coches_guardados=[]

    #Estructura de las filas
    #0 ["Evento"]
    #1 [Reloj (Minutos)]
    #2 [[RndEstadia,Estadia],[RndProxLlegada,ProxLlegada],[FinCobro]],
    #3 [RndAuto1,"tipo"],
    #4 [EstadoPlaya, CapacidadPlaya,PorcentajeUtilizacion],
    #5 [EstadoZonaCobro,ColaCobro],
    #6 [CobroTotal,CobroAcumulado]

    fila = [["Inicio"], 0, [[0, 0], [0, 0], 0], [0, ""], ["Libre", 8, 0], ["Libre", 0], [0, 0]]
    while finalizar_simulacion == False:
        fila_nueva = copy.deepcopy(fila)
        
        if primera_iteracion == True:
            primera_iteracion = False
            rnd_llegada = round(random.uniform(0, 0.9999), 4)
            prox_llegada = distribExp(datos[3], rnd_llegada)
            fila_nueva[2][1][0] = rnd_llegada
            fila_nueva[2][1][1] = prox_llegada
        else:
            fila_nueva = buscarProxHoraYEvento(fila_nueva, fila_anterior, coches, usar_prox_llegada_almacenada, prox_llegada_almacenada)

            if fila_nueva[0][0] == "Llegada":
                
                fila_nueva[0][0] = "Llegada A"+str(coche_id)
                rnd_llegada = round(random.uniform(0, 0.9999), 4)
                fila_nueva[2][1][0] = rnd_llegada
                fila_nueva[2][1][1] = distribExp(datos[3], rnd_llegada)
                prox_llegada_almacenada = fila_nueva[2][1][1] + fila_nueva[1]
                usar_prox_llegada_almacenada = False
                if fila_anterior[4][1]>0:

                    fila_nueva[2][0][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[2][0][1] = funcionBuscar(datos[5], fila_nueva[2][0][0])

                    fila_nueva[2][2] = round(fila_nueva[1] + fila_nueva[2][0][1],4)
                    fila_nueva[3][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[3][1] = funcionBuscar(datos[4], fila_nueva[3][0])
                    fila_nueva[4][1] -= 1
                    fila_nueva[4][0] = "Ocupado"
            
                    coche = Auto(coche_id, fila_nueva[3][1], fila_nueva[1], fila_nueva[2][2],None)
                    
                    coches.append(coche)
                coche_id += 1
            elif fila_nueva[0][0] == "Fin Estacionamiento":
                #Libero un lugar en la playa de estacionamiento
                fila_nueva[4][1] += 1
                
                #Busco el id del auto y calculo su fin de cobro si la zona de cobro esta libre
                id = buscarAuto(coches, fila_nueva[1])
                fila_nueva[0][0] = "Fin Estacionamiento A" + str(id)
                if fila_nueva[5][0] == "Libre":
                    coches[id].hora_fin_cobro=round(fila_nueva[1]+float(datos[6]),4)
                    coches[id].estado = "Cobrando"
                    fila_nueva[5][0] = "Ocupado"
                #Si no, lo agrego a la cola
                else:

                    coches[id].estado = "En cola"
                    fila_nueva[5][1]+=1
                    id_colas.append(id)

                
                usar_prox_llegada_almacenada = True
            
            elif fila_nueva[0][0] == "Fin Cobro":
                id = buscarAutoCobro(coches, fila_nueva[1])
                fila_nueva[0][0] = "Fin Cobro A" + str(id)

                #Calculo el cobro del auto dependiendo del tipo
                if coches[id].tipo == "Grandes":
                    fila_nueva[6][0] = round(float(500) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                elif coches[id].tipo == "Utilarios":
                    fila_nueva[6][0] = round(float(1000) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                else:
                    fila_nueva[6][0] = round(float(300) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                if id_primero ==id and bandera_primero==False:
                    coches[id].estado = "Destruidoo"
                else:    
                    coches[id].estado = "Destruido"

                if fila_nueva[5][1] > 0:
                    prox_id = id_colas.pop(0)
                    coches[prox_id].hora_fin_cobro = round(fila_nueva[1] + float(datos[6]), 4)
                    coches[prox_id].estado = "Cobrando"
                    fila_nueva[5][1] -= 1
                    fila_nueva[5][0] = "Ocupado"
                
                else:
                    fila_nueva[5][0]="Libre"

                usar_prox_llegada_almacenada = True

            fila_nueva[4][2] =( 1 - (fila_nueva[4][1] / 8))*100
            if fila_nueva[4][1] == 8:
                    fila_nueva[4][0] = "Libre"
        if fila_nueva[1] > datos[0]:
            iteraciones_guardadas.append(fila_anterior)
            contador_guardados +=1

            break
        else:
           if fila_nueva[1] >= datos[2] and contador_guardados < datos[1]:
            iteraciones_guardadas.append(fila_nueva)
            coches_guardados = [] 
            bandera_coche = False 
    
            for coche in coches:
                if coche.estado == "Destruidoo":
                    coches_guardados.append([0,0,0,0,0])
                    bandera_coche= True

                elif coche.estado != "Destruido":
                    if bandera_primero:
                        id_primero=coche.id
                        print(coche.id)
                        bandera_primero=False
                    coches_guardados.append([coche.id, coche.tipo, coche.estado, coche.hora_llegada, coche.hora_fin_estacionamiento])
                    bandera_coche = True

                

                elif bandera_coche:
                    coches_guardados.append([0,0,0,0,0])
                


            lista_coches.append(coches_guardados)
            contador_guardados+=1

        fila_anterior = copy.deepcopy(fila_nueva)
    return iteraciones_guardadas,contador_guardados, lista_coches

def funcionBuscar(tupla_determinar, rnd):
    acumulador = 0
    for i in range(len(tupla_determinar)):
        valor_comparar = tupla_determinar[i][0] / 100
        if i == 0:
            if rnd < valor_comparar:
                return tupla_determinar[i][1]
        else:
            if acumulador <= rnd < valor_comparar + acumulador:
                return tupla_determinar[i][1]
        acumulador += valor_comparar


def distribExp(tupla_llegada, rnd):
    proxllegada = -tupla_llegada * math.log(1 - rnd)
    return round(proxllegada, 4)

def buscarProxHoraYEvento(fila, filaAnterior, coches, bandera, hora_almacenada):
    #Primera Iteracion
    if filaAnterior[0][0] == "Inicio":
        fila[1] = filaAnterior[2][1][1] + filaAnterior[1]
        fila[0][0] = "Llegada"
        fila[4][1] = filaAnterior[4][1]
    else:
        
        reloj_actual = filaAnterior[1]
        min_fin_hora_estacionamiento = float('inf')
        min_fin_hora_cobro = float('inf')

        if  bandera:
            min_hora_llegada = hora_almacenada

        else:
            min_hora_llegada = filaAnterior[2][1][1] + filaAnterior[1]

        for coche in coches:
            if coche.hora_fin_estacionamiento > reloj_actual:
                min_fin_hora_estacionamiento = min(min_fin_hora_estacionamiento, coche.hora_fin_estacionamiento)

        for coche in coches:
            if coche.hora_fin_cobro is not None and coche.hora_fin_cobro > reloj_actual:
                min_fin_hora_cobro = min(min_fin_hora_cobro, coche.hora_fin_cobro)


 
        
        if min_hora_llegada < min_fin_hora_estacionamiento and min_hora_llegada < min_fin_hora_cobro:
                fila[1] = min_hora_llegada
                fila[0][0] = "Llegada"
                fila[4][0] =filaAnterior[4][0]
                fila[4][1] = filaAnterior[4][1]
                fila[6][1] = filaAnterior[6][0] + filaAnterior[6][1]
                fila[5][1] = filaAnterior[5][1]
                fila[5][0] = filaAnterior[5][0]
        elif min_fin_hora_estacionamiento < min_hora_llegada and min_fin_hora_estacionamiento < min_fin_hora_cobro:
                fila[1] = min_fin_hora_estacionamiento
                fila[0][0] = "Fin Estacionamiento"
                fila[4][0] =filaAnterior[4][0]
                fila[4][1] = filaAnterior[4][1]
                fila[6][1] = filaAnterior[6][0] + filaAnterior[6][1]
                fila[5][1] = filaAnterior[5][1]
                fila[5][0] = filaAnterior[5][0]
        else:
                fila[1] = min_fin_hora_cobro
                fila[0][0] = "Fin Cobro"
                fila[4][0] =filaAnterior[4][0]
                fila[4][1] = filaAnterior[4][1]
                fila[6][1] = filaAnterior[6][0] + filaAnterior[6][1]
                fila[5][1] = filaAnterior[5][1]
                fila[5][0] = filaAnterior[5][0]


    return fila

def buscarAuto(coches, finEstacionamiento):
    for i, coche in enumerate(coches):
        if coche.hora_fin_estacionamiento == finEstacionamiento:
            return i

def buscarAutoCobro(coches, finCobro):
    for i, coche in enumerate(coches):
        if coche.hora_fin_cobro== finCobro:
            return i
        

def filtrarAutos(coches,hora,filas):

    fila=filas[-2]
    
    lista=[]
    for coche in coches:
        if coche.estado != "Destruido"and coche.hora_llegada<=fila[1] :
            lista.append([coche.hora_llegada,coche.tipo,coche.estado])
    return lista
