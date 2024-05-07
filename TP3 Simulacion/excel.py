import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def mostrar_excel(datos):
    def flatten(lst):
        flattened_list = []
        for item in lst:
            if isinstance(item, list):
                flattened_list.extend(flatten(item))
            elif item == "":
                flattened_list.append("0")
            else:
                flattened_list.append(str(item))
        return flattened_list

    datos_unificados = [flatten(sublista) for sublista in datos]

    datos_en_lista = datos_unificados

    columnas = [
        "Semana",
        "RndDemanda",
        "Demanda",
        "RndAuto1", 
        "TipoAuto1",
        "RndAuto2", 
        "TipoAuto2",
        "RndAuto3", 
        "TipoAuto3",
        "RndAuto4", 
        "TipoAuto4",
        "ComisionAuto1", 
        "CantidadComision1",
        "ComisionAuto2", 
        "CantidadComision2",
        "ComisionAuto3",
        "CantidadComision3",
        "ComisionAuto4", 
        "CantidadComision4",
        "RndSorteo", 
        "ResSorteo",
        "ComisionFila",
        "ComisionAcumulada",
        "ComisionPromedio"
    ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = "Datos"

    # Definir los colores para cada grupo de columnas
    colores = {
        '1': 'FFFF99',  # Amarillo
        '2': '99CCFF',  # Azul
        '3': 'FF9999',  # Rojo claro
        '4': 'D3D3D3'   # Gris
    }

    columnas_a_colorear = {}

    for col, encabezado in enumerate(columnas, start=1):
        hoja.cell(row=1, column=col, value=encabezado)
        # Obtener el número de la columna
        num = encabezado[-1] if encabezado[-1].isdigit() else None
        if num and num in colores:
            fill = PatternFill(start_color=colores[num], end_color=colores[num], fill_type="solid")
            hoja.cell(row=1, column=col).fill = fill

            # Agregar la columna actual al diccionario de columnas a colorear
            if num not in columnas_a_colorear:
                columnas_a_colorear[num] = []
            columnas_a_colorear[num].append(col)

    # Colorear todas las celdas de las columnas que deben colorearse juntas
    for num, columnas in columnas_a_colorear.items():
        fill = PatternFill(start_color=colores[num], end_color=colores[num], fill_type="solid")
        for col in columnas:
            for fila in range(2, hoja.max_row + 1):
                hoja.cell(row=fila, column=col).fill = fill

    for fila_data in datos_en_lista:
        hoja.append(fila_data)

    # Guardar el archivo Excel
    nombre_archivo = "datos.xlsx"
    wb.save(nombre_archivo)

    # Abrir el archivo Excel
    os.system("start EXCEL.EXE {}".format(nombre_archivo))