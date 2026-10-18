# Inventario y facturación en C

Sistema de consola para practicar la gestión de inventario de un pequeño negocio. Permite consultar productos, agregar o modificar existencias, preparar pedidos y calcular el total de una factura. Los productos se guardan en SQLite y el historial de pedidos se registra en CSV.

## Funcionalidades

- Consultar productos con cantidad disponible, código y precio.
- Agregar productos al inventario y modificar sus cantidades o precios.
- Eliminar un producto estableciendo su cantidad en cero.
- Preparar un carrito y editar las cantidades antes de finalizar el pedido.
- Calcular subtotales y total de la factura en la terminal.
- Descontar existencias al finalizar el pedido.
- Consultar el historial por identificador del pedido.

**Esta versión no genera archivos PDF.** La descripción inicial del proyecto mencionaba esa función, pero el código recibido imprime la factura en consola y guarda sus líneas en `historial_facturas.csv`.

## Requisitos

La guía de instalación está orientada a Ubuntu/Debian o Ubuntu dentro de WSL en Windows. Se necesita GCC, las cabeceras de desarrollo de SQLite y Make. Python 3 solo se requiere para ejecutar las pruebas.

```bash
sudo apt update
sudo apt install build-essential sqlite3 libsqlite3-dev python3
```

Comprobar las herramientas:

```bash
gcc --version
sqlite3 --version
```

## Descarga, compilación y ejecución

```bash
git clone https://github.com/dagonzlz/inventario-facturacion-c.git
cd inventario-facturacion-c
make
./proyecto_pp
```

También se puede descargar el ZIP desde **Code → Download ZIP**, extraerlo y abrir una terminal en la carpeta extraída.

Sin Make, el comando equivalente es:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic proyecto_pp.c -o proyecto_pp -lsqlite3
./proyecto_pp
```

Ejecutar siempre desde la carpeta del proyecto: el programa busca `Inventario.db` y el historial en el directorio actual.

## Datos de ejemplo incluidos

`Inventario.db` viene inicializada con los mismos dos productos de `Inventario.csv`:

| Producto | Cantidad | Código | Precio |
|---|---:|---:|---:|
| Varilla de Plata | 21 | 1 | 3500.00 |
| Varilla de Níquel | 14 | 2 | 7600.00 |

Se puede iniciar el programa directamente después de compilarlo. El historial se crea automáticamente al finalizar el primer pedido; no es necesario descargarlo ni crearlo a mano.

Si la base de datos no existe, crearla con:

```bash
make init
```

O bien:

```bash
sqlite3 Inventario.db < sql/inicializar.sql
```

El script SQL crea la tabla e incorpora los productos de ejemplo cuando sus códigos no existen. No restaura las cantidades de los productos existentes.

## Ejemplo de uso

1. Seleccionar **1** para consultar los productos.
2. Seleccionar **2** e indicar un identificador de prueba, por ejemplo `PEDIDO-DEMO`.
3. Elegir **a**, escribir exactamente `Varilla de Plata` e indicar una cantidad de `2`.
4. Elegir **m** para volver al menú del pedido y **d** para finalizarlo.
5. La factura debe mostrar un total de `7000.00`; las existencias bajan de 21 a 19 si se utiliza la base inicial.
6. Seleccionar **3** e introducir `PEDIDO-DEMO` para consultar el historial.
7. Seleccionar **5** para salir.

En **4 → b**, ingresar el código del producto para modificarlo: `-1` conserva el valor actual y cantidad `0` elimina el producto.

## SQLite y CSV

SQLite es el almacenamiento activo del inventario. El programa **no sincroniza automáticamente** `Inventario.csv` al modificar productos. El CSV incluido es una referencia de los datos iniciales.

El CSV de productos utiliza **comas**, no punto y coma, y no tiene encabezado. Su orden es `Producto,Cantidad,Código,Precio`. Si se quiere importarlo manualmente, usar una base vacía con la tabla creada y, dentro de SQLite:

```text
.mode csv
.separator ","
.import Inventario.csv productos
```

No importar sobre la base de ejemplo sin revisar su contenido: se duplicarían los registros.

El historial utiliza las columnas `identificador,fecha,producto,cantidad,codigo,precio_unitario`, también sin encabezado.

## Estructura

```text
inventario-facturacion-c/
├── proyecto_pp.c
├── Inventario.db
├── Inventario.csv
├── Makefile
├── sql/inicializar.sql
├── tests/smoke_test.py
├── .github/workflows/build.yml
└── README.md
```

`proyecto_pp` es el ejecutable generado al compilar. `historial_facturas.csv` se genera durante el uso. Ambos se excluyen del control de versiones; el ZIP original no se publica como paquete porque contiene un historial antiguo y archivos duplicados.

## Validación

```bash
make test
```

La prueba usa una base temporal y verifica listado, alta y modificación de productos, cálculo de un pedido, descuento de existencias, historial y eliminación. No modifica la base del usuario. GitHub Actions ejecuta la compilación y esa prueba en Ubuntu.

## Alcance de esta versión

Se conserva el código académico recibido. Es un prototipo para demostración: no implementa impuestos, facturación electrónica, PDF, usuarios ni permisos. La validación de entradas y de existencias al editar o repetir artículos en el carrito es limitada. Algunos nombres con apóstrofes o comas pueden producir consultas o CSV incorrectos. Utilizar entradas breves y datos de prueba; se requiere revisar esos puntos antes de usarlo como sistema de un negocio real.

## Origen y autoría

Proyecto académico colaborativo del grupo 5, compartido por una de sus participantes para publicarlo en esta cuenta. Código original de referencia: [alesr21/Proyecto_grupo5](https://github.com/alesr21/Proyecto_grupo5). La documentación anterior mencionaba la rama `proyecto_grupo05`; esta publicación utiliza el código contenido en el ZIP `Proyecto_grupo5-main.zip` proporcionado por la participante.

Esta copia conserva el código fuente y agrega documentación de instalación, datos de ejemplo consistentes, un Makefile y validación automatizada. No atribuye el trabajo grupal a una sola persona ni agrega una licencia que los autores no hayan elegido.
