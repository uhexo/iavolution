# Estructura de datos

##Archivo
El archivo pedidos.json contiene 210 pedidos

## Información del pedido:
**Pedido** 
Campos para los pedidos:

* **id:** Identificador correlativo (ej. PED-2026-0001).
* **fecha:** Fechas distribuidas a lo largo del año 2026. formato YYYY-MM-DD HH24:mm:SS
* **empresa:** nombres aleatorios de empresa ficticias, se deben repetir. Los nombres no exceden 60 caracteres. 
* **pais:** Países de Centroamérica (Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica, Panamá, Belice).
* **estado:** Claves solicitadas:
+ A: Aperturado
+ S: Solicitado
+ P: Pagado
+ E: Entregado
+ C: Cancelado
* **detalle:** Lista de artículos solitados en el pedido. En promedio cada pèdido son 4 articulos.
  
**detalle**
campos que componen cada detalle  
* **codigo:** Código del producto reutilizable entre pedidos (ej. PROD-001, PROD-002, etc.).
* **descripcion:** Nombre del producto. 60 caracteres
* **cantidad:** Unidades solicitadas (de 1 a 8). Entero
* **precio:** Precio unitario estándar. Flotante varian de 1.00 a 35.00 
* **codigo_descuento:** P3 (3%), P5 (5%), P10 (10%), P25 (25%) o null cuando no aplica.
* **subtotal:** Cálculo exacto considerando la cantidad, el precio y el descuento aplicado (cantidad * precio * (1 - descuento)).
  