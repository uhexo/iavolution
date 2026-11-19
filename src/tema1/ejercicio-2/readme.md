
## Reporte de pedidos (ejercicio 2.1)

La función `reporte_pedido`, definida en [ejercicio-2.py](../ejercicio-2/ejercicio-2.py), genera un reporte a partir de la lista de pedidos de `ejercicio-2/pedidos.json`. Para cada pedido, suma los subtotales de los artículos en `detalle` y calcula el IVA; por defecto, la tasa es del 13%.

El reporte incluye:

* El periodo consultado y una tabla con el identificador, la fecha, el subtotal y el IVA de cada pedido dentro del periodo. Las fechas inicial y final se incluyen.
* Un resumen con la cantidad de pedidos, el total antes de IVA y el total con IVA.

La función también devuelve como número el total de los pedidos con IVA. Al ejecutar el archivo, se genera el reporte para el año 2026.