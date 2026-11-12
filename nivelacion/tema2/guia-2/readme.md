# Estructura de datos

##Archivo

El archivo pedidos.json contiene 210 pedidos


## Información del pedido:
**Pedido**
* **id_pedido:** Identificador correlativo (ej. PED-2026-0001).
* **fecha:** Fechas distribuidas a lo largo del año 2026.
* **cliente:** Formato de un nombre y un apellido (ej. Carlos Morales, Ana Flores, Luis Castillo), distribuidos en un grupo fijo para reflejar clientes recurrentes.
* **pais:** Países de Centroamérica (Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica, Panamá, Belice).
* **estado:** Claves solicitadas:
+ O: Abierto
+ A: Aceptado
+ P: Pagado
+ E: Entregado
+ C: Cancelado
* **total_pedido:** Suma total calculada a partir de los subtotales de cada artículo.

**Detalle de artículos (lista de articulos):**
* **codigo:** Código del producto reutilizable entre pedidos (ej. PROD-001, PROD-002, etc.).
* **descripcion:** Nombre del producto.
* **cantidad:** Unidades solicitadas (de 1 a 8).
* **precio:** Precio unitario estándar.
* **codigo_descuento:** P3 (3%), P5 (5%), P10 (10%), P25 (25%) o null cuando no aplica.
* **subtotal:** Cálculo exacto considerando la cantidad, el precio y el descuento aplicado (cantidad * precio * (1 - descuento)).