from ntpath import join
import tkinter as tk
from tkinter import ttk
import numpy as np
import sys
sys.path.append('/Users/tinchomengo/Desktop/UTN/SIM/simulacionTPs/TP2 Simulacion V2')
from Distribuciones.exponencial import exponencial
from Distribuciones.uniforme import uniforme
from Distribuciones.normal import normal
from Graficos.uniforme import histograma_uniforme
from Graficos.normal import histograma_normal
from Graficos.exponencial import histograma_exponencial

def generar_tabla(tabla):
    tabla.heading("Indice", text="Indice")
    tabla.heading("Numero", text="Numero")

    tabla.column("Indice", width=60, anchor="center")
    tabla.column("Numero", width=150, anchor="center")

def generar_tabla_ji_cuadrado(tabla):
    tabla.heading("#1", text="Intervalo")
    tabla.heading("#2", text="Frecuencia Observada")
    tabla.heading("#3", text="Frecuencia Esperada")
    tabla.heading("#4", text="Ji Cuadrado")


    tabla.column("#1", width=60, anchor="center")  # Ajustamos el ancho de la columna para que quepa el texto "Intervalo"
    tabla.column("#2", width=130, anchor="center")  # Ancho igual para las otras dos columnas
    tabla.column("#3", width=130, anchor="center")
    tabla.column("#4", width=130, anchor="center")


# Mostrar tablas (y generar numeros RND, exceptg para normal, ya que se hace en normal.py)
def mostrar_tabla_uniforme(cant_intervalo, a, b):
    numeros = generar_numeros_aleatorios(txt_muestra_uniforme) # Normal se genera en normal.py
    distribucionJiCuad,num,ji_calc, ji,fo,fe = uniforme(numeros, int(cant_intervalo), int(a), int(b)) 

    valor_fo =  tk.StringVar()
    valor_fe =  tk.StringVar()
    valor_ji = tk.StringVar()
    valor_ji.set(str(ji_calc))  
    valor_fo.set(str(fo))  
    valor_fe.set(str(fe))  

    lbl_Ji_cuadrado = tk.Label(frame_uniforme, text="Ji Cuadrado: "+ valor_ji.get())
    lbl_fo = tk.Label(frame_uniforme, text="Frecuencia Obs: "+ valor_fo.get())
    lbl_fe = tk.Label(frame_uniforme, text="Frecuencia Esp: "+ valor_fe.get())

    lbl_Ji_cuadrado.grid(row=5, column=3, pady=5, padx=(1, 5))  # Columna 0
    lbl_fo.grid(row=5, column=1, pady=5, padx=(5, 5))          # Columna 1
    lbl_fe.grid(row=5, column=2, pady=5, padx=(5, 5))           # Columna 2


    actualiza_tabla(tabla_uniforme, num)
    actualizar_tabla_ji_cuadrado(tabla_ji_cuadrado_uniforme, distribucionJiCuad,ji)
    btn_generar_uniforme = tk.Button(frame_uniforme, text="Generar Grafico", 
                                    command=lambda: histograma_uniforme(
                                        num,
                                        distribucionJiCuad,
                                        int(cant_intervalo)
                                    ),
                                    cursor="hand2")
    btn_generar_uniforme.grid(row=2, column=1, columnspa=4, padx=5, pady=5)

def mostra_tabla_normal(muestra,cant_intervalo,media,desviacion):
    distribucion,num,ji_calc, ji,fo,fe = normal(int(muestra),int(cant_intervalo), float(media), float(desviacion))


    valor_fo =  tk.StringVar()
    valor_fe =  tk.StringVar()
    valor_ji = tk.StringVar()
    valor_ji.set(str(ji_calc))  
    valor_fo.set(str(fo))  
    valor_fe.set(str(fe))  

    lbl_Ji_cuadrado = tk.Label(frame_normal, text="Ji Cuadrado: "+ valor_ji.get())
    lbl_fo = tk.Label(frame_normal, text="Frecuencia Obs: "+ valor_fo.get())
    lbl_fe = tk.Label(frame_normal, text="Frecuencia Esp: "+ valor_fe.get())

    lbl_Ji_cuadrado.grid(row=5, column=3, pady=5, padx=(1, 5))  # Columna 0
    lbl_fo.grid(row=5, column=1, pady=5, padx=(5, 5))          # Columna 1
    lbl_fe.grid(row=5, column=2, pady=5, padx=(5, 5))           # Columna 2


    actualiza_tabla(tabla_normal_1, num)

    actualizar_tabla_ji_cuadrado(tabla_ji_cuadrado_normal,distribucion,ji)

    btn_generar_normal = tk.Button(frame_normal, text="Generar Grafico", 
                                    command=lambda: histograma_normal(
                                        num,
                                        distribucion,
                                        int(cant_intervalo)
                                    ),
                                    cursor="hand2")
    btn_generar_normal.grid(row=2, column=1, columnspa=4, padx=5, pady=5)

def mostrar_tabla_exponencial(cant_intervalo, lambda_valor):
    numeros = generar_numeros_aleatorios(txt_muestra_exponencial) # Normal se genera en normal.py
    distr, num, ji_calc, ji,fo,fe = exponencial(numeros, int(cant_intervalo), float(lambda_valor))

    valor_fo =  tk.StringVar()
    valor_fe =  tk.StringVar()
    valor_ji = tk.StringVar()
    valor_ji.set(str(ji_calc))  
    valor_fo.set(str(fo))  
    valor_fe.set(str(fe))  

    lbl_Ji_cuadrado = tk.Label(frame_exponencial, text="Ji Cuadrado: "+ valor_ji.get())
    lbl_fo = tk.Label(frame_exponencial, text="Frecuencia Obs: "+ valor_fo.get())
    lbl_fe = tk.Label(frame_exponencial, text="Frecuencia Esp: "+ valor_fe.get())

    lbl_Ji_cuadrado.grid(row=5, column=3, pady=5, padx=(1, 5))  # Columna 0
    lbl_fo.grid(row=5, column=1, pady=5, padx=(5, 5))          # Columna 1
    lbl_fe.grid(row=5, column=2, pady=5, padx=(5, 5))           # Columna 2


    actualiza_tabla(tabla_exponencial, num)
    actualizar_tabla_ji_cuadrado(tabla_ji_cuadrado, distr,ji)
    btn_generar_exponencial = tk.Button(frame_exponencial, text="Generar Grafico", 
                                    command=lambda: histograma_exponencial(
                                        num,
                                        distr,
                                        int(cmb_intervalo_exponencial.get())
                                    ),
                                    cursor="hand2")
    btn_generar_exponencial.grid(row=2, column=1, columnspa=4, padx=5, pady=5)

# Actualiza los datos de la interfaz de la tabla de Ji Cuadrado (para las 3 distribuciones)
def actualizar_tabla_ji_cuadrado(tabla, datos, ji_array):
    # Borra todos los elementos actuales de la tabla
    tabla.delete(*tabla.get_children())

    # Asegúrate de que las listas tengan la misma longitud
    if len(datos[0]) != len(datos[1]) or len(datos[1]) != len(datos[2]):
        raise ValueError("Las listas de datos deben tener la misma longitud")

    # Inserta los nuevos datos en la tabla
    for i in range(len(datos[0])):
        intervalo = datos[0][i]
        fo = datos[1][i]
        fe = datos[2][i]
        ji = ji_array[i]
        tabla.insert("", "end", values=(intervalo, fo, fe, ji))


def generar_numeros_aleatorios(txt):
    numeros = []
    if validar_muestra(txt.get()):
        tamano = int(txt.get())
        numeros = np.random.uniform(0, 1, tamano)    
        return numeros


def actualiza_tabla(tabla, numeros):
    tabla.delete(*tabla.get_children())

    data_to_insert = [(idx + 1, num) for idx, num in enumerate(numeros)]

    for data in data_to_insert:
        tabla.insert("", "end", values=data)

# Valida que muestra esté entre (1;1000000)
def validar_muestra(numero):
    try:
        num = int(numero)
        if 1 <= num <= 1000000:
            return True
        else:
            return False
    except ValueError:
        return False

# De acá para abajo es todo para generación de interfaz
def mostrar_uniforme():
    frame_uniforme.grid(row=1, column=0, padx=20, pady=20)
    frame_normal.grid_forget()
    frame_exponencial.grid_forget()
    btn_uniforme.config(relief=tk.SUNKEN)
    btn_normal.config(relief=tk.RAISED)
    btn_exponencial.config(relief=tk.RAISED)


def mostrar_normal():
    frame_normal.grid(row=1, column=0, padx=20, pady=20)
    frame_uniforme.grid_forget()
    frame_exponencial.grid_forget()
    btn_normal.config(relief=tk.SUNKEN)
    btn_uniforme.config(relief=tk.RAISED)
    btn_exponencial.config(relief=tk.RAISED)


def mostrar_exponencial():
    frame_exponencial.grid(row=1, column=0, padx=20, pady=20)
    frame_uniforme.grid_forget()
    frame_normal.grid_forget()
    btn_exponencial.config(relief=tk.SUNKEN)
    btn_uniforme.config(relief=tk.RAISED)
    btn_normal.config(relief=tk.RAISED)


opciones_frecuencia = ["10", "15", "20", "25"]
root = tk.Tk()

root.title("Trabajo practico N°2")
root.geometry("800x500")

frame_botones = tk.Frame(root)
frame_botones.pack(padx=20, pady=20)

frame_principal = tk.Frame(root)
frame_principal.pack(padx=20, pady=20)

#-------------------- UNIFORME --------------------
btn_uniforme = tk.Button(frame_botones, text="Uniforme", command=mostrar_uniforme, cursor="hand2")
btn_uniforme.grid(row=0, column=2, padx=5, pady=5)

frame_uniforme = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_uniforme, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=0, padx=5, pady=5)

txt_muestra_uniforme = tk.Entry(frame_uniforme,)
txt_muestra_uniforme.grid(row=0, column=1, padx=5, pady=5)

lbl_intervalo = tk.Label(frame_uniforme, text="Intervalos:")
lbl_intervalo.grid(row=0, column=2, padx=5, pady=5)

cmb_intervalo_uniforme = ttk.Combobox(frame_uniforme, values=opciones_frecuencia, state="readonly")
cmb_intervalo_uniforme.grid(row=0, column=3, padx=5, pady=5)

lbl_a = tk.Label(frame_uniforme, text="A:")
lbl_a.grid(row=1, column=0, padx=5, pady=5)

txt_a = tk.Entry(frame_uniforme)
txt_a.grid(row=1, column=1, padx=5, pady=5)

lbl_b = tk.Label(frame_uniforme, text="B:")
lbl_b.grid(row=1, column=2, padx=5, pady=5)

txt_b = tk.Entry(frame_uniforme)
txt_b.grid(row=1, column=3, padx=5, pady=5)

btn_generar_uniforme = tk.Button(frame_uniforme, text="Generar", 
                                 command=lambda: mostrar_tabla_uniforme(
                                     cmb_intervalo_uniforme.get(),
                                     txt_a.get(),
                                     txt_b.get(),
                                 ),
                                 cursor="hand2")
btn_generar_uniforme.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

tabla_uniforme = ttk.Treeview(frame_uniforme, columns=("Indice", "Numero"), show="headings")
tabla_uniforme.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

scrollbar_uniforme = ttk.Scrollbar(frame_uniforme, orient="vertical", command=tabla_uniforme.yview)
scrollbar_uniforme.grid(row=3, column=4, sticky="ns")
tabla_uniforme.configure(yscrollcommand=scrollbar_uniforme.set)

generar_tabla(tabla_uniforme)

tabla_ji_cuadrado_uniforme = ttk.Treeview(frame_uniforme, columns=("Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "Ji Cuadrado"), show="headings")

tabla_ji_cuadrado_uniforme.grid(row=3, column=2, columnspan=2, padx=1, pady=5)  # Second table

scrollbar_ji_cuadrado = ttk.Scrollbar(frame_uniforme, orient="vertical", command=tabla_ji_cuadrado_uniforme.yview)
scrollbar_ji_cuadrado.grid(row=3, column=6, sticky="ns")  # Second table scrollbar
tabla_ji_cuadrado_uniforme.configure(yscrollcommand=scrollbar_ji_cuadrado.set)
generar_tabla_ji_cuadrado(tabla_ji_cuadrado_uniforme)

#-------------------- NORMAL --------------------
btn_normal = tk.Button(frame_botones, text="Normal", command=mostrar_normal, cursor="hand2")
btn_normal.grid(row=0, column=0, padx=5, pady=5)

frame_normal = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_normal, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=0, padx=5, pady=5)

txt_muestra_normal = tk.Entry(frame_normal)
txt_muestra_normal.grid(row=0, column=1, padx=5, pady=5)

lbl_intervalo = tk.Label(frame_normal, text="Intervalo:")
lbl_intervalo.grid(row=0, column=2, padx=5, pady=5)

cmb_intervalo_normal = ttk.Combobox(frame_normal, values=opciones_frecuencia, state="readonly")
cmb_intervalo_normal.grid(row=0, column=3, padx=5, pady=5)

lbl_media = tk.Label(frame_normal, text="Media:")
lbl_media.grid(row=1, column=0, padx=5, pady=5)

txt_media = tk.Entry(frame_normal)
txt_media.grid(row=1, column=1, padx=5, pady=5)

lbl_desviacion = tk.Label(frame_normal, text="Desviacion:")
lbl_desviacion.grid(row=1, column=2, padx=5, pady=5)

txt_desviacion = tk.Entry(frame_normal)
txt_desviacion.grid(row=1, column=3, padx=5, pady=5)

btn_generar_normal =tk.Button(frame_normal, text="Generar", 
                                    command=lambda: mostra_tabla_normal(
                                        txt_muestra_normal.get(),
                                        cmb_intervalo_normal.get(),
                                        txt_media.get(),
                                        txt_desviacion.get()
                                    ),
                                    cursor="hand2")
btn_generar_normal.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

scrollbar_normal = ttk.Scrollbar(frame_normal, orient="vertical")

tabla_normal_1 = ttk.Treeview(frame_normal, columns=("Indice", "Numero"), show="headings",
                              yscrollcommand=scrollbar_normal.set)
tabla_normal_1.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

generar_tabla(tabla_normal_1)

tabla_normal_2 = ttk.Treeview(frame_normal, columns=("Indice", "Numero"), show="headings",
                              yscrollcommand=scrollbar_normal.set)
tabla_normal_2.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

scrollbar_normal.config(command=lambda *args: (tabla_normal_1.yview(*args), tabla_normal_2.yview(*args)))

scrollbar_normal.grid(row=3, column=4, sticky="ns")

generar_tabla(tabla_normal_2)

tabla_ji_cuadrado_normal = ttk.Treeview(frame_normal, columns=("Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "Ji Cuadrado"), show="headings")

tabla_ji_cuadrado_normal.grid(row=3, column=2, columnspan=2, padx=1, pady=5)  # Second table

scrollbar_ji_normal = ttk.Scrollbar(frame_normal, orient="vertical", command=tabla_ji_cuadrado_normal.yview)
scrollbar_ji_cuadrado.grid(row=3, column=6, sticky="ns")  # Second table scrollbar
tabla_ji_cuadrado_normal.configure(yscrollcommand=scrollbar_ji_cuadrado.set)
generar_tabla_ji_cuadrado(tabla_ji_cuadrado_normal)


#-------------------- EXPONENCIAL --------------------
btn_exponencial = tk.Button(frame_botones, text="Exponencial", command=mostrar_exponencial, cursor="hand2")
btn_exponencial.grid(row=0, column=1, padx=5, pady=5)

frame_exponencial = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_exponencial, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=0, padx=5, pady=5)

txt_muestra_exponencial = tk.Entry(frame_exponencial)
txt_muestra_exponencial.grid(row=0, column=1, padx=5, pady=5)

lbl_intervalo = tk.Label(frame_exponencial, text="Intervalo:")
lbl_intervalo.grid(row=0, column=2, padx=5, pady=5)

cmb_intervalo_exponencial = ttk.Combobox(frame_exponencial, values=opciones_frecuencia, state="readonly")
cmb_intervalo_exponencial.grid(row=0, column=3, padx=5, pady=5)

lbl_lambda = tk.Label(frame_exponencial, text="Lambda:")
lbl_lambda.grid(row=1, column=1, padx=5, pady=5)

txt_lambda = tk.Entry(frame_exponencial)
txt_lambda.grid(row=1, column=2, padx=5, pady=5)

btn_generar_exponencial = tk.Button(frame_exponencial, text="Generar", 
                                    command=lambda: mostrar_tabla_exponencial(
                                        cmb_intervalo_exponencial.get(),
                                        txt_lambda.get()
                                    ),
                                    cursor="hand2")
btn_generar_exponencial.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

tabla_exponencial = ttk.Treeview(frame_exponencial, columns=("Indice", "Numero"), show="headings")
tabla_exponencial.grid(row=3, column=0, columnspan=2, padx=5, pady=5)  # First table

scrollbar_exponencial = ttk.Scrollbar(frame_exponencial, orient="vertical", command=tabla_exponencial.yview)
scrollbar_exponencial.grid(row=3, column=4, sticky="ns")  # First table scrollbar
tabla_exponencial.configure(yscrollcommand=scrollbar_exponencial.set)

generar_tabla(tabla_exponencial)

tabla_ji_cuadrado = ttk.Treeview(frame_exponencial, columns=("Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "Ji Cuadrado"), show="headings")

tabla_ji_cuadrado.grid(row=3, column=2, columnspan=2, padx=1, pady=5)  # Second table

scrollbar_ji_cuadrado = ttk.Scrollbar(frame_exponencial, orient="vertical", command=tabla_ji_cuadrado.yview)
scrollbar_ji_cuadrado.grid(row=3, column=6, sticky="ns")  # Second table scrollbar
tabla_ji_cuadrado.configure(yscrollcommand=scrollbar_ji_cuadrado.set)

generar_tabla_ji_cuadrado(tabla_ji_cuadrado)

root.mainloop()
