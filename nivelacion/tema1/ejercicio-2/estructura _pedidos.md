# Estructura de datos

##Archivo
El archivo pedidos.json contiene 210 pedidos

## Información del pedido:
**Pedido** 
Campos para los pedidos:

* **id:** str Identificador correlativo (ej. PED-2026-0001). Este obligatorio 
* **fecha:** datetime Fechas distribuidas a lo largo del año 2026. formato YYYY-MM-DD HH24:mm:SS
* **empresa:** str nombres aleatorios de empresa ficticias, se deben repetir. Los nombres no exceden 60 caracteres. 
* **pais:** str Países de Centroamérica (Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica, Panamá, Belice).
* **estado:** str Claves solicitadas:
+ A: Aperturado
+ S: Solicitado
+ P: Pagado
+ E: Entregado
+ C: Cancelado
+ **Nota:** str Es un campo opcional, donde se puede agregar un comentario al pedido.w
* **detalle:** list Lista de artículos solitados en el pedido. En promedio cada pèdido son 4 articulos.
  
**detalle**
Composicion del detalle   (restriccion y descripcion del mensaje)
* **codigo:** str Código del producto reutilizable entre pedidos (ej. PROD-001, PROD-002, etc.).
* **descripcion:** str Nombre del producto. 60 caracteres
* **cantidad:** int Unidades solicitadas (de 1 a 8). Entero
* **precio:** decimal(8,2) Precio unitario estándar. Flotante varian de 1.00 a 35.00 
* **codigo_descuento:** str P3 (3%), P5 (5%), P10 (10%), P25, P15 (15%), P25 (25%) o null cuando no aplica.
* **subtotal:** Decimal(8,2) Cálculo exacto considerando la cantidad, el precio y el descuento aplicado (cantidad * precio * (1 - descuento)).


**Retricciones. Reglas de los integridad**
* **PED-Q1:** Datos requeridos : id, fecha, emoresa, estado, pais, detalles, codigo, descripcion, cantidad, precio, subtotal.
* **PED-Q2:** El detalle debe tener un registro
* **PED-Q3:** Datos requeridos: id, fecha, emoresa, estado, pais, detalle
* **PED-Q4:** Conversion invalida.
* **ENC-Q1:** el id debe cumplir con la mascara PED\-\d{3}-\d{4}
* **ENC-Q2:** los digitos del 5 al 9 del ID, debe conincidir con el año del pedido.
* **ENC-Q3:** El estado tiene un dato invalido. Solo puede ser  [ASPEC]
* **DET-01:** la cantidad debe ser mayor de cero.
* **DET-02:** la descripcion debe tener al menos 5 caracters   
* **DET-03:** el precio debe usar . como divición entre entero y decimal Y debe ser mayor de dero 
* **DET-04:** Los valores validos para el codigo_descuento son P03, P05, P10, P15, P35
* **DET-05:** El calculo del subtotal no correspondo.


**Autocorrecciones**
Las autocorrecion del la data se aplica antes de la validacion de las restriciones.
* Los campos empresa, pais y descripción debe Capitsalizarse y eliminar cualquier espacio en blanco antes y después
* Id,estado,producto,codigo_descuento deben estar en mayuscula
* Valor de precio y subtotal deben ser redondeados a dos deciales. 


## Información del pedido invalñidos:
**Pedido** 
Campos para los pedidos:

* **pedido_pos:** int, posicion en el lista de pedidos. 
* **id:** str identificaor del pedido si tiene.
* **resticion:** str  El codigo de la restriccion 
* **mensaje:** str mensaje de la restricion incumplida   
* **data** dict registro del pedido original 

