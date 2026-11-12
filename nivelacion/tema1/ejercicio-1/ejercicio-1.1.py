#!/usr/bin/env python3    

# Crea un programa que guarde en tres variables el nombre de un producto, 
# su precio por unidad y la cantidad que compras, y muestre una frase con tu compra. 
# Después, muestra el total a pagar calculándolo, sin escribir el resultado a mano.

# Elaborado por: Francisco HUezo.

def genera_ticket(producto, precio, cantidad):
    """ 
    Función que genera un ticket de compra para un producto dado.
    Args:
        producto (str): Nombre del producto.
        precio (float): Precio por unidad del producto.
        cantidad (int): Cantidad de unidades compradas.
    """

    # 1. Calcular el total a pagar   
    total_a_pagar = precio_unitario * cantidad

    # 2. Se presenta la salida
    print(f"Has comprado {cantidad} unidades de {nombre_producto} a {precio_unitario:.2f} cada una.")
    print(f"Total a pagar: {total_a_pagar:.2f}")



# Ejecucion principal del programa

# Permite solo ejecuciones directas.
if __name__ == "__main__":
    
    nombre_producto = "Manzana"
    precio_unitario = 0.75  # Precio en tu moneda local
    cantidad = 6
    
    genera_ticket(nombre_producto, precio_unitario, cantidad)


