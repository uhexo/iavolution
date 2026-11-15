                                                                                                                #!/usr/bin/env python3

import json
import sys 
from calendar import monthrange
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP


VERSION = "1.0"

__EJERCICIO_2__ = False
if __EJERCICIO_2__ :
    exit 
else:
    __EJERCICIO_2__ = True


def ingrensar_periodo(inicio: date = date.min, final:date = date.max) -> tuple[date , date]:
    """
    Solicita el ingreso del periodo para los reportes
    * inicio: date. Fecha de inicio del periodo. 
        Por omisión, el valor pasado como argumento, el primer dia del mes actual o usar * desde el principio
    * final: date. Fecha final del periodo. 
        Por omisión el ultimo día del mes actual o usar * para hasta el final.
    El formato para las fechas es dd/mm/yyyy en caso desde una fecha sea un límite representar con * 
    
    Restriciones:
    * La fecha final puede ser mayor o igual a la menor

    Al haber un ingreso invalido repite la solicitud de ambos valores.
    """
    hoy = date.today()
    inicio_predeterminado = (
        date(hoy.year, hoy.month, 1) if inicio == date.min else inicio
    )
    final_predeterminado = (
        date(hoy.year, hoy.month, monthrange(hoy.year, hoy.month)[1])
        if final == date.max
        else final
    )

    while True:
        inicio_ingresado = input(
            f"Fecha de inicio [dd/mm/aaaa, *] "
            f"(Enter: {inicio_predeterminado.strftime('%d/%m/%Y')}): "
        ).strip()
        final_ingresado = input(
            f"Fecha final [dd/mm/aaaa, *] "
            f"(Enter: {final_predeterminado.strftime('%d/%m/%Y')}): "
        ).strip()

        try:
            ini = (
                inicio_predeterminado
                if not inicio_ingresado
                else date.min
                if inicio_ingresado == "*"
                else datetime.strptime(inicio_ingresado, "%d/%m/%Y").date()
            )
            fin = (
                final_predeterminado
                if not final_ingresado
                else date.max
                if final_ingresado == "*"
                else datetime.strptime(final_ingresado, "%d/%m/%Y").date()
            )
        except ValueError:
            print("Fecha inválida. Use dd/mm/aaaa o *; vuelva a ingresar ambas fechas.")
            continue

        if ini > fin:
            print("El inicio no puede ser posterior al final; vuelva a ingresar ambas fechas.")
            continue

        return ini, fin

def linea(simbolo: str = "-", tamaño: int = 72):
    """
    Inmprime un linea ASCII
    * simbolo: Str  Caracter que se repita como parte de la linea
    * tamaño: int Tamaño en caracteres de la linea 
    """
    print( simbolo * tamaño )


def encabezasdo_reporte(titulo: str, fecha_inicio: date, fecha_fin: date, columnas: str):
    """
    Imprime el encabezado del reporte con el título, periodo y nombres de columnas.
    """
    print(titulo)
    print(f"Periodo desde {fecha_inicio.isoformat()} hasta {fecha_fin.isoformat()}")
    linea()
    print(columnas)
    linea()



def reporte_pedidos_solicitados_por_pais(pedidos: dict, fecha_inicio: date, fecha_fin: date):
    """
    Imprime el reporte de pedidos solicitados por país, ordenados de mayor a menor.
    """

    pedidos_paises = {}
    for pedido_actual in pedidos["pedidos"]:
        if pedido_actual["estado"] == "A" and fecha_inicio <= datetime.fromisoformat(pedido_actual["fecha"]).date() <= fecha_fin:
            pais = pedido_actual["pais"]
            if pais not in pedidos_paises:
                pedidos_paises[pais]= {"cantidad": 1}
            else:
                pedidos_paises[pais]["cantidad"]  += 1

    columnas=f"{'País':<30} {'Cantidad':>14}"
    encabezasdo_reporte("Reporte de pedidos solicitados por país", fecha_inicio, fecha_fin, columnas)

    total = 0
    for pais, cantidad in sorted(pedidos_paises.items(), key=lambda x: x[1]["cantidad"], reverse=True):
        print(f"{pais:<30} {cantidad['cantidad']:>14}")        
        total += cantidad['cantidad']

    linea()
    print(f"Total: {total:>14}")
    linea()
    

def reporte_pedido(pedidos: dict, inicia: date = date.min, finaliza: date = date.max, iva=0.13):
    """
    Imprime el reporte de pedidos del periodo indicado y devuelve el total con IVA.
    """

    tasa_iva = Decimal(str(iva))
    pedidos_periodo = []

    for pedido_actual in pedidos["pedidos"]:
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

def reportar_invalidos(invalidos: dict) -> None :
    """
    Escribe los pedididos invalidos 
    """

    salida = Path(sys.prefix).parent.resolve() / "salida"
    file_path = salida / "invalidos.json"

    salida.mkdir(exist_ok=True)   

    try:
        with open( file_path, "w", encoding="utf-8") as file:
            json.dump(invalidos, file, indent=2)
        print(f"Archivo {file_path} fue creadi.")


    except Exception as e:
        print(f"Error inesperado al escribir el archivo de invalidos: {e}")      
        print(f"Archivo {file_path} no fue escrito.")
        quit(-1)  # Salir del programa si no se pudieron cargar los pedidos
    
       

    


def normalizar(data: dict) -> dict:
    """
    Normaliza los datos de los pedidos:
    
    El proceso de normalizacion consiste en autocorregir los datos, 
    llevarlos a su tipo de dato esperado y 
    eliminar los pedidos que no cumplan con las restricciones

    * Recibe:
    data dict pedidos recuperados.

    * Retorna: dict con los datos validos y normalizados.
    * Si existe datos invalidos son escrito en invalidos y llama la rutina reportar_invalidos. 

    De acuerdo a lo especificado en estrudtura_pedidos.md

    * aplicar las autocorreciones descripta en el documento estructura_pedidos-.
    * revisa el cunplimiento de las restriciones

    Los pedidos correctos son agreagos a la dict pedidos_normalizados

    El ciclo solo aborta hasta que se revisen todos los pedidos en data.

    La data solo tiene str. Asi que convertir a sus tipos de datos
    """

    pedidos_normalizados = {} 
    invalidos = {} 

    # <Implementar aqui>
    
    
    return pedidos_normalizados


def leer_pedidos(file_path: str) -> dict:
    """
    Lee ycarga los pedidos desde un archivo JSON.

    Args:
        relative_file_path (str): Ruta relativa al archivo JSON.

    Returns:
        list: Lista de pedidos cargados desde el archivo.
    """
   
   
    try:
        pedidos = {}    
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


def recuperar_pedidos(ubicacion_json: str) -> dict:
    """
    """

    file_path = Path(__file__).parent.resolve() / ubicacion_json
    data = leer_pedidos(file_path)
    #pedidos = normalizar(data)
    reportar_invalidos(data)

