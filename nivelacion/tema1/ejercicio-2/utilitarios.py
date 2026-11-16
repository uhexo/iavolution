                                                                                                                #!/usr/bin/env python3

import json
import hashlib
import re
import sys 
import os 
import subprocess
from copy import deepcopy
from calendar import monthrange
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


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

def serializar_valor(valor: object) -> str:
    if isinstance(valor, (date, datetime)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return format(valor, "f")
    raise TypeError(f"Tipo no serializable para el checksum: {type(valor).__name__}")

def reportar(data: any, filename: str) -> None :
    """
    Escribe en la salida
    """

    salida = Path(sys.prefix).parent.resolve() / "salida"
    file_path = salida / filename 

    salida.mkdir(exist_ok=True)   

    try:
        with open( file_path, "w", encoding="utf-8") as file:
            if type(data) == "dict":
                json.dump(data, file, indent=2, ensure_ascii=False)
            elif type(data) == "str":
                file.write(data)
            else:
                raise "Tipo de dato no experado" 
    
        print(f"Archivo {file_path} fue creado.")

    except Exception as e:
        print(f"Error inesperado al escribir el archivo de invalidos: {e}")      
        print(f"Archivo {file_path} no fue escrito.")
        quit(-1)  # Salir del programa si no se pudieron cargar los pedidos
    



def reportar_invalidos(invalidos: dict) -> None :
    """
    Escribe los pedididos invalidos 
    """

    salida = Path(sys.prefix).parent.resolve() / "salida"
    file_path = salida / "invalidos.json"

    salida.mkdir(exist_ok=True)   

    try:
        with open( file_path, "w", encoding="utf-8") as file:
            json.dump(invalidos, file, indent=2, ensure_ascii=False)
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

    if not isinstance(data, dict) or not isinstance(data.get("pedidos"), list):
        raise ValueError("Se esperaba un diccionario con una lista 'pedidos'.")

    pedidos_normalizados = {"pedidos": []}
    invalidos = {"pedidos_invalidos": []}
    campos_pedido = ("id", "fecha", "empresa", "estado", "pais", "detalle")
    campos_detalle = ("codigo", "descripcion", "cantidad", "precio", "subtotal")
    descuentos_validos = {"P03", "P05", "P10", "P15", "P25", "P35"}
    patron_id = re.compile(r"PED-(\d{4})-\d{4}")
    centavo = Decimal("0.01")

    for pedido_pos, pedido_original in enumerate(data["pedidos"], start=1):
        errores_antes = len(invalidos["pedidos_invalidos"])
        pedido = deepcopy(pedido_original)
        pedido_id = pedido.get("id") if isinstance(pedido, dict) else None
        if isinstance(pedido_id, str):
            pedido_id = pedido_id.strip().upper()

        def registrar_error(restriccion: str, mensaje: str) -> None:
            invalidos["pedidos_invalidos"].append(
                {
                    "pedido_pos": pedido_pos,
                    "id": pedido_id,
                    "restriccion": restriccion,
                    "mensaje": mensaje,
                    "data": deepcopy(pedido_original),
                }
            )

        if not isinstance(pedido, dict):
            registrar_error("PED-Q3", "El pedido debe ser un objeto.")
            continue

        campos_faltantes = [
            campo
            for campo in campos_pedido
            if campo not in pedido
            or pedido[campo] is None
            or (isinstance(pedido[campo], str) and not pedido[campo].strip())
        ]
        if campos_faltantes:
            registrar_error(
                "PED-Q3",
                f"Faltan datos requeridos del pedido: {', '.join(campos_faltantes)}.",
            )

        for campo in ("id", "estado"):
            valor = pedido.get(campo)
            if isinstance(valor, str):
                pedido[campo] = valor.strip().upper()
            elif valor is not None:
                registrar_error("PED-Q4", f"El campo '{campo}' debe ser texto.")

        for campo in ("empresa", "pais"):
            valor = pedido.get(campo)
            if isinstance(valor, str):
                pedido[campo] = valor.strip().title()
            elif valor is not None:
                registrar_error("PED-Q4", f"El campo '{campo}' debe ser texto.")

        fecha_pedido = None
        valor_fecha = pedido.get("fecha")
        if isinstance(valor_fecha, datetime):
            fecha_pedido = valor_fecha
        elif isinstance(valor_fecha, str):
            try:
                fecha_pedido = datetime.strptime(
                    valor_fecha.strip(), "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                registrar_error("PED-Q4", "El campo 'fecha' no tiene un formato válido.")
        elif valor_fecha is not None:
            registrar_error("PED-Q4", "El campo 'fecha' debe ser una fecha válida.")
        if fecha_pedido is not None:
            pedido["fecha"] = fecha_pedido

        coincidencia_id = (
            patron_id.fullmatch(pedido["id"])
            if isinstance(pedido.get("id"), str)
            else None
        )
        if pedido.get("id") and coincidencia_id is None:
            registrar_error("ENC-Q1", "El id debe cumplir el formato PED-AAAA-NNNN.")
        elif coincidencia_id and fecha_pedido is not None:
            if int(coincidencia_id.group(1)) != fecha_pedido.year:
                registrar_error("ENC-Q2", "El año del id no coincide con la fecha del pedido.")

        estado = pedido.get("estado")
        if isinstance(estado, str) and estado not in {"A", "S", "P", "E", "C"}:
            registrar_error("ENC-Q3", "El estado solo puede ser A, S, P, E o C.")

        detalle = pedido.get("detalle")
        if isinstance(detalle, list):
            if not detalle:
                registrar_error("PED-Q2", "El pedido debe contener al menos un detalle.")
            detalles_normalizados = []
            for detalle_pos, item_original in enumerate(detalle, start=1):
                if not isinstance(item_original, dict):
                    registrar_error(
                        "PED-Q1", f"El detalle {detalle_pos} debe ser un objeto."
                    )
                    continue

                item = deepcopy(item_original)
                campos_detalle_faltantes = [
                    campo
                    for campo in campos_detalle
                    if campo not in item
                    or item[campo] is None
                    or (isinstance(item[campo], str) and not item[campo].strip())
                ]
                for campo in campos_detalle_faltantes:
                    registrar_error(
                        "PED-Q1",
                        f"Falta el campo requerido '{campo}' en el detalle {detalle_pos}.",
                    )

                codigo = item.get("codigo")
                if isinstance(codigo, str):
                    item["codigo"] = codigo.strip().upper()
                elif codigo is not None:
                    registrar_error(
                        "PED-Q4", f"El código del detalle {detalle_pos} debe ser texto."
                    )

                descripcion = item.get("descripcion")
                if isinstance(descripcion, str):
                    item["descripcion"] = descripcion.strip().title()
                    if len(item["descripcion"]) < 5:
                        registrar_error(
                            "DET-02",
                            f"La descripción del detalle {detalle_pos} debe tener al menos 5 caracteres.",
                        )
                elif descripcion is not None:
                    registrar_error(
                        "PED-Q4",
                        f"La descripción del detalle {detalle_pos} debe ser texto.",
                    )

                cantidad = None
                valor_cantidad = item.get("cantidad")
                if valor_cantidad is not None:
                    try:
                        cantidad_decimal = Decimal(str(valor_cantidad))
                        if (
                            isinstance(valor_cantidad, bool)
                            or not cantidad_decimal.is_finite()
                            or cantidad_decimal != cantidad_decimal.to_integral_value()
                        ):
                            raise InvalidOperation
                        cantidad = int(cantidad_decimal)
                        item["cantidad"] = cantidad
                    except (InvalidOperation, ValueError, TypeError, OverflowError):
                        registrar_error(
                            "PED-Q4",
                            f"La cantidad del detalle {detalle_pos} no es un entero válido.",
                        )
                if cantidad is not None and cantidad <= 0:
                    registrar_error(
                        "DET-01",
                        f"La cantidad del detalle {detalle_pos} debe ser mayor que cero.",
                    )

                montos = {}
                for campo in ("precio", "subtotal"):
                    valor = item.get(campo)
                    if valor is None:
                        continue
                    try:
                        monto = Decimal(str(valor))
                        if isinstance(valor, bool) or not monto.is_finite():
                            raise InvalidOperation
                        monto = monto.quantize(centavo, rounding=ROUND_HALF_UP)
                        item[campo] = monto
                        montos[campo] = monto
                    except (InvalidOperation, ValueError, TypeError):
                        registrar_error(
                            "PED-Q4",
                            f"El campo '{campo}' del detalle {detalle_pos} no es un decimal válido.",
                        )

                precio = montos.get("precio")
                if precio is not None and precio <= 0:
                    registrar_error(
                        "DET-03",
                        f"El precio del detalle {detalle_pos} debe ser mayor que cero.",
                    )

                descuento = item.get("codigo_descuento")
                if descuento is None:
                    item["codigo_descuento"] = None
                    descuento = None
                elif isinstance(descuento, str):
                    descuento = descuento.strip().upper()
                    descuento = {"P3": "P03", "P5": "P05"}.get(descuento, descuento)
                    item["codigo_descuento"] = descuento
                    if descuento not in descuentos_validos:
                        registrar_error(
                            "DET-04",
                            f"El descuento del detalle {detalle_pos} no es válido.",
                        )
                else:
                    registrar_error(
                        "DET-04",
                        f"El descuento del detalle {detalle_pos} debe ser un código válido o null.",
                    )
                    descuento = None

                if (
                    cantidad is not None
                    and cantidad > 0
                    and precio is not None
                    and precio > 0
                    and "subtotal" in montos
                    and descuento in descuentos_validos | {None}
                ):
                    porcentaje = (
                        Decimal(descuento[1:]) / Decimal("100")
                        if descuento is not None
                        else Decimal("0")
                    )
                    subtotal_esperado = (
                        cantidad * precio * (Decimal("1") - porcentaje)
                    ).quantize(centavo, rounding=ROUND_HALF_UP)
                    if montos["subtotal"] != subtotal_esperado:
                        registrar_error(
                            "DET-05",
                            f"El subtotal del detalle {detalle_pos} no coincide con su cantidad, precio y descuento.",
                        )

                detalles_normalizados.append(item)

            pedido["detalle"] = detalles_normalizados
        elif detalle is not None:
            registrar_error("PED-Q4", "El campo 'detalle' debe ser una lista.")

        if len(invalidos["pedidos_invalidos"]) == errores_antes:
            pedidos_normalizados["pedidos"].append(pedido)

    if invalidos["pedidos_invalidos"]:
        reportar_invalidos(invalidos)

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


def recuperar_pedidos(ubicacion_json: str = "pedidos.json") -> dict:
    """
    recupera la data. 

    Recibe
    * ubicacion_json: str La ubicacion del archivo con respecto a data. Por omision es pedidos.json

    Retorna:
    * dict: Pedidos normalizados con los totales recibidos/válidos y el MD5 de la lista.
    
    Excepicion:
    * Termina el programa al haber un problema de lectura del archivop
    * Las incosistencias son almacenadas en la salida
    
    """
    
    data_dir = Path(sys.prefix).parent.resolve() / "data"
    file_path = data_dir / ubicacion_json
    data = leer_pedidos(file_path)
    pedidos = normalizar(data)

 

    contenido = json.dumps(
        pedidos["pedidos"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=serializar_valor,
    ).encode("utf-8")

    pedidos["recibidos"] = len(data["pedidos"])
    pedidos["validos"] = len(pedidos["pedidos"])
    pedidos["check"] = hashlib.md5(contenido, usedforsecurity=False).hexdigest()

    return pedidos 



def verify_bash_shell() -> None:
    """
        Valida que este script de python solo puede ser ejecutado bash shell.¡
    """
    try:
        ppid = os.getppid()
        # Query the parent process command name (works on macOS and Linux)
        result = subprocess.run(
            ["ps", "-p", str(ppid), "-o", "comm="],
            capture_output=True,
            text=True,
            check=True,
        )
        parent_comm = os.path.basename(result.stdout.strip())
        # Remove leading '-' in case it is a login shell (e.g., '-bash')
        if parent_comm.lstrip("-") != "bash":
            print(
                f"Error: This script must be run directly from bash "
                f"(detected parent process: '{parent_comm}').",
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as exc:
        print(f"Error verifying parent shell: {exc}", file=sys.stderr)
        sys.exit(1)


def clear_screen() -> None:
    """Clears the terminal screen using the standard POSIX clear command."""
    os.system("clear")