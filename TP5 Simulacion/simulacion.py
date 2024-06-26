import random
import math
import copy
    # 0  - tiempoSimulacion
    # 1  - nroIteraciones
    # 2  - horaGuardado
    # 3  - llegada
    # 4  - prob Tipo
    # 5  - prob unaHoras
    # 6 - unif A
    # 7 - unif B
    # 8 - rkZ
    # 9 - rkW
    # 10 - rk h

class Auto:
    def __init__(self, id, tipo, hora_llegada,fin_estacionamiento,hora_cobro, hora_fin_cobro):
        self.id = id
        self.tipo = tipo
        self.estado = "Estacionado"
        self.hora_llegada = hora_llegada
        self.hora_fin_estacionamiento = fin_estacionamiento
        self.tiempo_cobro= hora_cobro
        self.hora_fin_cobro = hora_fin_cobro

    def __repr__(self):
        return f"Auto(id={self.id}, tipo={self.tipo}, estado={self.estado}, hora_llegada={self.hora_llegada}, fin_estacionamiento={self.hora_fin_estacionamiento},hora_cobro={self.tiempo_cobro}, fin_cobro={self.hora_fin_cobro})"

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
    listaid=[]

    #Estructura de las filas
    #0 ["Evento"]
    #1 [Reloj (Minutos)]
    #2 [[RndEstadia,Estadia, FinEstacionamiento],[RndProxLlegada,ProxLlegada],[rndC,ValorC, TiempoCobro]],
    #3 [RndAuto1,"tipo"],
    #4 [EstadoPlaya, CapacidadPlaya,PorcentajeUtilizacion],
    #5 [EstadoZonaCobro,ColaCobro],
    #6 [CobroTotal,CobroAcumulado]

    fila = [["Inicio"], 0, [[0, 0,0], [0, 0],[0,0,0]], [0, ""], ["Libre", 10, 0], ["Libre", 0], [0, 0]]
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
                fila_nueva[2][1][1] = round(distribExp(datos[3], rnd_llegada) + fila_nueva[1],4)
                prox_llegada_almacenada = fila_nueva[2][1][1]
                usar_prox_llegada_almacenada = False
                if fila_anterior[4][1]>0:

                    fila_nueva[2][0][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[2][0][1] = funcionBuscar(datos[5], fila_nueva[2][0][0])

                    fila_nueva[2][0][2] = round(fila_nueva[1] + fila_nueva[2][0][1],4)
                   
                    fila_nueva[3][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[3][1] = funcionBuscar(datos[4], fila_nueva[3][0])
                    fila_nueva[4][1] -= 1
            
                    coche = Auto(coche_id, fila_nueva[3][1], fila_nueva[1], fila_nueva[2][0][2],None,None)

                    coches.append(coche)
                if fila_nueva[4][1]>0:
                    fila_nueva[4][0]="Libre"
                else:
                    fila_nueva[4][0] ="Ocupado"
                coche_id +=1
            
            elif fila_nueva[0][0] == "Fin Estacionamiento":
                #Libero un lugar en la playa de estacionamiento
                fila_nueva[4][1] += 1
                if fila_nueva[4][1]>0:
                    fila_nueva[4][0]="Libre"
                else:
                    fila_nueva[4][0] ="Ocupado"
                
                #Busco el id del auto y calculo su fin de cobro si la zona de cobro esta libre
                id,i = buscarAuto(coches, fila_nueva[1])
                fila_nueva[0][0] = "Fin Estacionamiento A" + str(i)
                if fila_nueva[5][0] == "Libre":
                    fila_nueva[2][2][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[2][2][1] =round(distribUnif(datos[6],datos[7],fila_nueva[2][2][0]),4)
                                                    #C                 , Z      , W       , h
                    fila_nueva[2][2][2] = round(calcularRk(fila_nueva[2][2][1],datos[8],datos[9],datos[10]),4)
                    coches[id].tiempo_cobro= fila_nueva[2][2][2]
                    coches[id].hora_fin_cobro=round((fila_nueva[1]+coches[id].tiempo_cobro),4)
                    coches[id].estado = "Cobrando"
                    fila_nueva[5][0] = "Ocupado"
                #Si no, lo agrego a la cola
                else:

                    coches[id].estado = "En cola"
                    fila_nueva[5][1]+=1
                    id_colas.append(id)

                
                usar_prox_llegada_almacenada = True
            
            elif fila_nueva[0][0] == "Fin Cobro":
                id,i = buscarAutoCobro(coches, fila_nueva[1])
                fila_nueva[0][0] = "Fin Cobro A" + str(i)

                #Calculo el cobro del auto dependiendo del tipo
                if coches[id].tipo == "Grandes":
                    fila_nueva[6][0] = round(float(500) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                elif coches[id].tipo == "Utilarios":
                    fila_nueva[6][0] = round(float(1000) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                else:
                    fila_nueva[6][0] = round(float(300) * ((coches[id].hora_fin_estacionamiento - coches[id].hora_llegada ) / 60),4)
                if id_primero ==coches[id].id and bandera_primero==False:
                    coches[id].estado = "Destruido"
                else:    
                    coches[id].estado = "Destruido"

                if fila_nueva[5][1] > 0:
                    prox_id = id_colas.pop(0)
                    fila_nueva[2][2][0] = round(random.uniform(0, 0.9999), 4)
                    fila_nueva[2][2][1] =round(distribUnif(datos[6],datos[7],fila_nueva[2][2][0]),4)
                                                    #C                 , Z      , W       , h
                    fila_nueva[2][2][2] = round(calcularRk(fila_nueva[2][2][1],datos[8],datos[9],datos[10]),4)
                    coches[prox_id].tiempo_cobro= fila_nueva[2][2][2]
                    coches[prox_id].hora_fin_cobro = round(fila_nueva[1]+coches[prox_id].tiempo_cobro, 4)
                    coches[prox_id].estado = "Cobrando"
                    fila_nueva[5][1] -= 1
                    fila_nueva[5][0] = "Ocupado"
                
                else:
                    fila_nueva[5][0]="Libre"

                usar_prox_llegada_almacenada = True

            fila_nueva[4][2] =( 1 - (fila_nueva[4][1] / 10))*100
            if fila_nueva[4][1] > 0:
                    fila_nueva[4][0] = "Libre"
        if fila_nueva[1] > datos[0]:
            if contador_guardados < datos[1]:
                break
            else:

                iteraciones_guardadas.append(fila_anterior)
                contador_guardados +=1

            break
        else:
           if fila_nueva[1] >= datos[2] and contador_guardados < datos[1]:
            iteraciones_guardadas.append(fila_nueva)
            coches_guardados = [] 
            bandera_coche = False 
    
            for coche in coches:
                if coche.estado == "Destruido" and coche.id==id_primero and not bandera_primero:
                    
                    coches_guardados.append([0,0,0,0,0,0])
                    bandera_coche= True
                    

                elif coche.estado != "Destruido":
                    if bandera_primero:
                        id_primero=coche.id
                        bandera_primero=False
                    coches_guardados.append([coche.id, coche.tipo, coche.estado, coche.hora_llegada, coche.hora_fin_estacionamiento,coche.tiempo_cobro])
                    bandera_coche = True
                    listaid.append(coche.id)

                else:
                    if bandera_coche:
                        if coche.id  not in listaid:
                            pass
                        else:
                            coches_guardados.append([0,0,0,0,0,0])                


            lista_coches.append(coches_guardados)
            contador_guardados+=1

        fila_anterior = copy.deepcopy(fila_nueva)
    rkExcel=[]
    rkExcel=calcularRkMax(datos[7],datos[8],datos[9],datos[10])
    return iteraciones_guardadas,contador_guardados, lista_coches,rkExcel

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
        fila[1] = filaAnterior[2][1][1] 
        fila[0][0] = "Llegada"
        fila[4][1] = filaAnterior[4][1]
    else:
        
        reloj_actual = filaAnterior[1]
        min_fin_hora_estacionamiento = float('inf')
        min_fin_hora_cobro = float('inf')

        if  bandera:
            min_hora_llegada = hora_almacenada

        else:
            min_hora_llegada = filaAnterior[2][1][1] 

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
            return i,coche.id

def buscarAutoCobro(coches, finCobro):
    for i, coche in enumerate(coches):
        if coche.hora_fin_cobro== finCobro:
            return i,coche.id
        
def distribUnif(a,b,rnd):
    return a+rnd*(b-a)

def calcularRk(valorC,z,w,h):
    rk_guardado=[]
    primVez=True
    tant=0
    cant=0
    #0 - t
    #1 - C
    #2 - k1
    #3 - C + k1/2
    #4 - k2
    #5 - 3 + K2/2
    #6 - k3
    #7 - 5 + k3
    #8 - k4
    #9 - Ci+1
    iRK= [0,1,0,0,0,0,0,0,0,0]

    while iRK[9]<valorC:
        if primVez:
            iRK[2]=h*((z)*math.log(iRK[1]+w))
            iRK[3]=iRK[1]+(iRK[2]/2)
            iRK[4]= h*((z)*math.log(iRK[3]+w))
            iRK[5]= iRK[3]+(iRK[4]/2)
            iRK[6]= h*((z)*math.log(iRK[5]+w))
            iRK[7]=iRK[3]+(iRK[6])
            iRK[8]=h*((z)*math.log(iRK[7]+w))
            iRK[9]=iRK[1]+ 1/6*(iRK[2]+2*iRK[4]+2*iRK[6]+iRK[8])
            rk_guardado.append(iRK)
            primVez=False
            tant=iRK[0]
            cant=iRK[9]
        else:
            iRK[0]=tant+h
            iRK[1]=cant
            iRK[2]=h*((z)*math.log(iRK[1]+w))
            iRK[3]=iRK[1]+(iRK[2]/2)
            iRK[4]= h*((z)*math.log(iRK[3]+w))
            iRK[5]= iRK[3]+(iRK[4]/2)
            iRK[6]= h*((z)*math.log(iRK[5]+w))
            iRK[7]=iRK[3]+(iRK[6])
            iRK[8]=h*((z)*math.log(iRK[7]+w))
            iRK[9]=iRK[1]+ 1/6*(iRK[2]+2*iRK[4]+2*iRK[6]+iRK[8])
            rk_guardado.append(iRK)
            tant=iRK[0]
            cant=iRK[9]
    return (iRK[0]+h)    
    


def calcularRkMax(b,z,w,h):
    rk_guardado=[]
    primVez=True
    tant=0
    cant=0
    #0 - t
    #1 - C
    #2 - k1
    #3 - C + k1/2
    #4 - k2
    #5 - 3 + K2/2
    #6 - k3
    #7 - 5 + k3
    #8 - k4
    #9 - Ci+1
    iRK= [0,1,0,0,0,0,0,0,0,0]
    while iRK[9]<b:
        if primVez:
            iRK[2]=h*((z)*math.log(iRK[1]+w))
            iRK[3]=iRK[1]+(iRK[2]/2)
            iRK[4]= h*((z)*math.log(iRK[3]+w))
            iRK[5]= iRK[3]+(iRK[4]/2)
            iRK[6]= h*((z)*math.log(iRK[5]+w))
            iRK[7]=iRK[3]+(iRK[6])
            iRK[8]=h*((z)*math.log(iRK[7]+w))
            iRK[9]=iRK[1]+ 1/6*(iRK[2]+2*iRK[4]+2*iRK[6]+iRK[8])
            rk_guardado.append(iRK[:])
            primVez=False
            tant=iRK[0]
            cant=iRK[9]
        else:
            iRK[0]=tant+h
            iRK[1]=cant
            iRK[2]=h*((z)*math.log(iRK[1]+w))
            iRK[3]=iRK[1]+(iRK[2]/2)
            iRK[4]= h*((z)*math.log(iRK[3]+w))
            iRK[5]= iRK[3]+(iRK[4]/2)
            iRK[6]= h*((z)*math.log(iRK[5]+w))
            iRK[7]=iRK[3]+(iRK[6])
            iRK[8]=h*((z)*math.log(iRK[7]+w))
            iRK[9]=iRK[1]+ 1/6*(iRK[2]+2*iRK[4]+2*iRK[6]+iRK[8])
            rk_guardado.append(iRK[:])
            tant=iRK[0]
            cant=iRK[9]
    return (rk_guardado)    
    


