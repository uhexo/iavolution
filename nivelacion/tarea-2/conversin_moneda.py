#!/usr/bin/env python3
"""
Script para convertir Euros a Dólares utilizando la clase Decimal.
"""

## Tema 1. Tarea 2.
# #Conversor de moneda
#
# Pide al usuario un importe en dólares y conviértelo a euros con una tasa de 0,92. 
# Muestra el resultado con dos decimales.
#
# Test de prueba 
# 
# Importe en dólares: 150 
# 150.00 USD equivalen a 138.00 EUR
# 
# Pista: input() siempre devuelve texto. Para hacer cuentas tienes que convertirlo con  float()
#
# Elaborado por: Francisco HUezo.

import locale
from babel.numbers import parse_decimal
from decimal import Decimal, InvalidOperation

TASA_CAMBIO = Decimal('0.92')

def convertir_dolars_euros(monto_en_dolars: Decimal) -> Decimal:
    """Convierte un monto en dolars a euros según la tasa de cambio."""
    return monto_en_dolars * TASA_CAMBIO

def main() -> None:
    print("=== Conversor de Dólares a Euros ===")
    print("Ingrese 'q' para salir.")

    monto_recomendado = locale.format_string('%.2f', 150, grouping=True)
    
    while True:
        entrada = input(f"Ingrese el monto en dolares [{monto_recomendado}]: ").strip()
        
        # Opción para salir
        if entrada.lower() == 'q':
            print("Saliendo del programa. ¡Hasta luego!")
            break
            
        # Valor por defecto si el usuario presiona Enter sin escribir nada
        if not entrada:
            entrada = monto_recomendado

        try:
            # Convertir a Decimal
            elementos_validos = [item for item in locale.getlocale() if item is not None]
            current = "_".join(elementos_validos)
            monto = parse_decimal(entrada,current)
        

            # Validar que tenga como máximo 2 decimales
            # El exponente en Decimal nos indica los decimales (ej. -2 significa centésimas)
            if monto.as_tuple().exponent < -2:
                print("❌ Error: El valor debe tener un máximo de 2 decimales. Intente nuevamente.\n")
                continue
                
            if monto < 0:
                print("❌ Error: El monto no puede ser negativo. Intente nuevamente.\n")
                continue
                
            # Realizar conversión
            resultado = convertir_dolars_euros(monto)
            
            # Mostrar resultado formateado a 2 decimales
            monto = locale.format_string('%.2f', monto, grouping=True)
            resultado = locale.format_string('%.2f', resultado, grouping=True)
            
            print(f"✅ {monto} USD equivalen a {resultado} EUR\n")
            
        except Exception:
            print("❌ Error: Formato numérico inválido. Ingrese un número válido o 'q' para salir.\n")

if __name__ == "__main__":
#    locale.setlocale(locale.LC_ALL, 'es_SV.UTF-8')
#   locale.setlocale(locale.LC_ALL, 'es_SV.UTF-8')
    locale.setlocale(locale.LC_ALL, '')
    main()
    