#!/usr/bin/env python3

import pathlib


def leer_json(file_path):
    """
    Lee un archivo JSON y devuelve su contenido como un diccionario.
    
    :param file_path: Ruta del archivo JSON a leer.
    :return: Diccionario con el contenido del archivo JSON.
    """
    import json
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def listar_pedidos(data, pais=None):
    """
    Lista los pedidos contenidos en el diccionario filtrados por país. Si se omite el país, se listan todos los pedidos.
    La lista de pedidos se muestra ordenado por pais, fecha y id_pedido.
    
    :param data: Diccionario con los datos de los pedidos.
    :param pais: País por el que se filtran los pedidos.
    """
    print("Listado de Pedidos:")

    pedidos = data.get('pedidos', [])
    if pais is not None:
        pedidos = [pedido for pedido in pedidos if pedido.get('pais') == pais]
    pedidos = sorted(
        pedidos,
        key=lambda pedido: (pedido['pais'], pedido['fecha'], pedido['id_pedido'])
    )

    for pedido in pedidos:
        print(f"Pais: {pedido['pais']}, Pedido ID: {pedido['id_pedido']}, Cliente: {pedido['cliente']}, Fecha: {pedido['fecha']}, Estado: {pedido['estado']}")

    print("\nTotal de pedidos:", len(pedidos), "\n")


def main():
    # Ruta del archivo JSON
    file_path = pathlib.Path(__file__).parent.resolve() / 'pedidos.json'

    data = leer_json(file_path)

    # Listar los pedidos filtrados por país
    listar_pedidos(data, pais='Belice')  # Puedes cambiar el país según sea necesario
    
    # Listar los pedidos
    listar_pedidos(data )  # Puedes cambiar el país según sea necesario


if __name__ == "__main__":
    main()
    