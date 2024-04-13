import random
import tkinter as tk
from tkinter import ttk
import numpy as np


def generar_tabla(tabla):
    tabla.heading("#0", text="Indice")
    tabla.heading("#1", text="Numero")

    tabla.column("#0", width=100, anchor="center")
    tabla.column("#1", width=100, anchor="center")


def mostrar_tabla_uniforme():
    numeros = generar_numeros_aleatorios(txt_muestra_uniforme)
    actualiza_tabla(tabla_uniforme, numeros)


def mostra_tabla_normal():
    numeros_1 = generar_numeros_aleatorios(txt_muestra_normal)
    numeros_2 = generar_numeros_aleatorios(txt_muestra_normal)
    actualiza_tabla(tabla_normal_1, numeros_1)
    actualiza_tabla(tabla_normal_2, numeros_2)

def mostrar_tabla_exponencial():
    numeros = generar_numeros_aleatorios(txt_muestra_exponencial)
    actualiza_tabla(tabla_exponencial,numeros)

def generar_numeros_aleatorios(txt):
    numeros = []
    if validar_muestra(txt.get()):
        tamano = int(txt.get())
        numeros = np.random.uniform(0, 1, tamano).round(4)
    return numeros


def actualiza_tabla(tabla, numeros):
    tabla.delete(*tabla.get_children())

    data_to_insert = [(idx + 1, num) for idx, num in enumerate(numeros)]

    for data in data_to_insert:
        tabla.insert("","end",values=data)


def validar_muestra(numero):
    try:
        num = int(numero)
        if 1 <= num <= 1000000:
            return True
        else:
            return False
    except ValueError:
        return False


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

root = tk.Tk()

root.title("Trabajo practico N°2")
root.geometry("800x500")

frame_botones = tk.Frame(root)
frame_botones.pack(padx=20, pady=20)

frame_principal = tk.Frame(root)
frame_principal.pack(padx=20, pady=20)

#UNIFORME
btn_uniforme = tk.Button(frame_botones, text="Uniforme", command=mostrar_uniforme, cursor="hand2")
btn_uniforme.grid(row=0, column=2, padx=5, pady=5)

frame_uniforme = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_uniforme, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=1, padx=5, pady=5)

txt_muestra_uniforme = tk.Entry(frame_uniforme)
txt_muestra_uniforme.grid(row=0, column=2, padx=5, pady=5)

lbl_a = tk.Label(frame_uniforme, text="A:")
lbl_a.grid(row=1, column=0, padx=5, pady=5)

txt_a = tk.Entry(frame_uniforme)
txt_a.grid(row=1, column=1, padx=5, pady=5)

lbl_b = tk.Label(frame_uniforme, text="B:")
lbl_b.grid(row=1, column=2, padx=5, pady=5)

txt_b = tk.Entry(frame_uniforme)
txt_b.grid(row=1, column=3, padx=5, pady=5)

btn_generar_uniforme = tk.Button(frame_uniforme, text="Generar", command=mostrar_tabla_uniforme, cursor="hand2")
btn_generar_uniforme.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

tabla_uniforme = ttk.Treeview(frame_uniforme, columns=("Indice", "Numero"), show="headings")
tabla_uniforme.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

scrollbar_uniforme = ttk.Scrollbar(frame_uniforme, orient="vertical", command=tabla_uniforme.yview)
scrollbar_uniforme.grid(row=3, column=4, sticky="ns")
tabla_uniforme.configure(yscrollcommand=scrollbar_uniforme.set)

generar_tabla(tabla_uniforme)

#NORMAL
btn_normal = tk.Button(frame_botones, text="Normal", command=mostrar_normal, cursor="hand2")
btn_normal.grid(row=0, column=0, padx=5, pady=5)

frame_normal = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_normal, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=1, padx=5, pady=5)

txt_muestra_normal = tk.Entry(frame_normal)
txt_muestra_normal.grid(row=0, column=2, padx=5, pady=5)

lbl_media = tk.Label(frame_normal, text="Media:")
lbl_media.grid(row=1, column=0, padx=5, pady=5)

txt_media = tk.Entry(frame_normal)
txt_media.grid(row=1, column=1, padx=5, pady=5)

lbl_desviacion = tk.Label(frame_normal, text="Desviacion:")
lbl_desviacion.grid(row=1, column=2, padx=5, pady=5)

txt_desviacion = tk.Entry(frame_normal)
txt_desviacion.grid(row=1, column=3, padx=5, pady=5)

btn_generar_normal = tk.Button(frame_normal, text="Generar", command=mostra_tabla_normal, cursor="hand2")
btn_generar_normal.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

scrollbar_normal = ttk.Scrollbar(frame_normal, orient="vertical")

tabla_normal_1 = ttk.Treeview(frame_normal, columns=("Indice", "Numero"), show="headings",yscrollcommand=scrollbar_normal.set)
tabla_normal_1.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

generar_tabla(tabla_normal_1)

tabla_normal_2 = ttk.Treeview(frame_normal, columns=("Indice", "Numero"), show="headings",yscrollcommand=scrollbar_normal.set)
tabla_normal_2.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

scrollbar_normal.config(command=lambda *args: (tabla_normal_1.yview(*args), tabla_normal_2.yview(*args)))

scrollbar_normal.grid(row=3, column=4, sticky="ns")

generar_tabla(tabla_normal_2)

#EXPONENCIAL
btn_exponencial = tk.Button(frame_botones, text="Exponencial",command=mostrar_exponencial,cursor="hand2")
btn_exponencial.grid(row=0, column=1, padx=5, pady=5)

frame_exponencial = tk.Frame(frame_principal)

lbl_muestra = tk.Label(frame_exponencial, text="Tamaño muestra:")
lbl_muestra.grid(row=0, column=0, padx=5, pady=5)

txt_muestra_exponencial = tk.Entry(frame_exponencial)
txt_muestra_exponencial.grid(row=0, column=1, padx=5, pady=5)

lbl_lambda = tk.Label(frame_exponencial, text="Lambda:")
lbl_lambda.grid(row=1, column=0, padx=5, pady=5)

txt_lambda = tk.Entry(frame_exponencial)
txt_lambda.grid(row=1, column=1, padx=5, pady=5)

btn_generar_exponencial = tk.Button(frame_exponencial, text="Generar", command=mostrar_tabla_exponencial, cursor="hand2")
btn_generar_exponencial.grid(row=2, column=1, columnspa=2, padx=5, pady=5)

tabla_exponencial = ttk.Treeview(frame_exponencial, columns=("Indice", "Numero"), show="headings")
tabla_exponencial.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

scrollbar_exponencial = ttk.Scrollbar(frame_exponencial, orient="vertical", command=tabla_exponencial.yview)
scrollbar_exponencial.grid(row=3, column=4, sticky="ns")
tabla_exponencial.configure(yscrollcommand=scrollbar_exponencial.set)

generar_tabla(tabla_exponencial)

root.mainloop()
