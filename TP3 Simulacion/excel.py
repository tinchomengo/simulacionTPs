from openpyxl import Workbook

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

    for col, encabezado in enumerate(columnas, start=1):
        hoja.cell(row=1, column=col, value=encabezado)

    for fila_data in datos_en_lista:
        hoja.append(fila_data)

    wb.save("datos.xlsx")