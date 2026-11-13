#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

def encabezasdo_reporte(titulo: str, fecha_inicio: date, fecha_fin: date, columnas: str):
    """
    Imprime el encabezado del reporte con el título, periodo y nombres de columnas.
    """
    print(titulo)
    print(f"Periodo desde {fecha_inicio.isoformat()} hasta {fecha_fin.isoformat()}")
    print("-" * 72)
    print(columnas)
    print("-" * 72)




def reporte_pedidos_solicitados_por_pais(pedidos: list, fecha_inicio: date, fecha_fin: date):
    """
    Imprime el reporte de pedidos solicitados por país, ordenados de mayor a menor.
    """

    pedidos_paises = {}
    for pedido_actual in pedidos:
        if pedido_actual["estado"] != "solicitado":
            pais = pedido_actual["pais"]
            if pais not in pedidos_paises:
                pedidos_paises[pais] = 1
            else:
                pedidos_paises[pais] += 1

    
    
    columnas=f"{'País':<30} {'total':>14}"
    encabezasdo_reporte("Reporte de pedidos solicitados por país", fecha_inicio, fecha_fin, columnas)

    for pais, totals in paises.items():
        print(f"{pais:<30} {totals['total_subtotal']:>14.2f} {totals['total_iva']:>14.2f}")
        total_subtotal += totals["total_subtotal"]
        total_iva += totals["total_iva"]

    total_con_iva = total_subtotal + total_iva
    print("-" * 72)
    print(f"{'Total':<30} {total_subtotal:>14.2f} {total_iva:>14.2f}")
    print(f"{'Total con IVA':<30} {total_con_iva:>14.2f}")
    print("-" * 72)
    print()  # Línea en blanco al final del reporte
    return float(total_con_iva)


def reporte_pedido(pedido: list, inicia: date = date.min, finaliza: date = date.max, iva=0.13):
    """
    Imprime el reporte de pedidos del periodo indicado y devuelve el total con IVA.
    """

    tasa_iva = Decimal(str(iva))
    pedidos_periodo = []

    for pedido_actual in pedido:
        fecha_pedido = datetime.fromisoformat(pedido_actual["fecha"]).date()
        if inicia <= fecha_pedido <= finaliza    :
            subtotal = sum(
                (Decimal(str(item["subtotal"])) for item in pedido_actual["detalle"]),
                Decimal("0.00"),
            )
            iva_pedido = (subtotal * tasa_iva).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            pedidos_periodo.append((pedido_actual, fecha_pedido, subtotal, iva_pedido))


    columnas=f"{'ID':<18} {'Fecha':<10} {'Subtotal':>14} {'IVA':>14}"
    encabezasdo_reporte("Reporte de pedidos del periodo", inicia, finaliza, columnas)

    total_pedidos = Decimal("0.00")
    total_iva = Decimal("0.00")
    pedidos_periodo.sort(key=lambda pedido_actual: pedido_actual[1])
    for pedido_actual, fecha_pedido, subtotal, iva_pedido in pedidos_periodo:
        print(
            f"{pedido_actual['id']:<18} {fecha_pedido} "
            f"{subtotal:>14.2f} {iva_pedido:>14.2f}"
        )
        total_pedidos += subtotal
        total_iva += iva_pedido

    total_con_iva = total_pedidos + total_iva
    print("-" * 72)
    print(f"Total de pedidos: {len(pedidos_periodo)}")
    print(f"Total de los pedidos: {total_pedidos:.2f}")
    print(f"Total de los pedidos con IVA: {total_con_iva:.2f}")
    print("-" * 72)
    print()  # Línea en blanco al final del reporte
    return float(total_con_iva)


def leer_pedidos(relative_file_path: str) -> dict:
    """
    Lee ycarga los pedidos desde un archivo JSON.

    Args:
        relative_file_path (str): Ruta relativa al archivo JSON.

    Returns:
        list: Lista de pedidos cargados desde el archivo.
    """
   
    file_path = Path(__file__).parent.resolve() / relative_file_path
    try:
        pedidos = []    
        with open(file_path, "r", encoding="utf-8") as file:
            pedidos = json.load(file)
    except FileNotFoundError:
        print(f"El archivo no fue encontrado.")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo, no es un JSON válido.")   
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")      
    finally:
        if not pedidos:
            print(f"Archivo {file_path} invalido.")
            quit(-1)  # Salir del programa si no se pudieron cargar los pedidos
    return pedidos       



def main():
    pedidos = leer_pedidos("pedidos.json")
    reporte_pedido(pedidos["pedidos"], date(2026, 1, 1), date(2026, 1, 31))
   #reporte_pedido(pedidos["pedidos"])


if __name__ == "__main__":
    main()