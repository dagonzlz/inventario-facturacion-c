"""Prueba de integración con una base temporal; no modifica los datos del usuario."""
import csv
from pathlib import Path
import sqlite3
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    with sqlite3.connect(work / 'Inventario.db') as db:
        db.executescript((ROOT / 'sql/inicializar.sql').read_text(encoding='utf-8'))
    def run(inputs):
        result = subprocess.run([str(ROOT / 'proyecto_pp')], input=inputs, text=True,
                                cwd=work, capture_output=True, timeout=10)
        assert result.returncode == 0, result.stderr
        assert not result.stderr, result.stderr
        return result.stdout
    output = run('1\n5\n')
    assert 'Varilla de Plata' in output
    # Alta y modificación de un producto.
    run('4\na\nProducto Demo\n5\n99\n100\nb\n99\n7\n125\nc\n5\n')
    with sqlite3.connect(work / 'Inventario.db') as db:
        assert db.execute('SELECT Cantidad, Precio FROM productos WHERE "Código"=99').fetchone() == (7, 125.0)
    # Venta, total calculado, descuento de existencias e historial.
    output = run('2\nPEDIDO-DEMO\na\nProducto Demo\n2\nm\nd\n5\n')
    assert 'Total Factura: 250.00' in output
    with sqlite3.connect(work / 'Inventario.db') as db:
        assert db.execute('SELECT Cantidad FROM productos WHERE "Código"=99').fetchone() == (5,)
    with (work / 'historial_facturas.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.reader(stream))
    assert len(rows) == 1 and rows[0][0] == 'PEDIDO-DEMO'
    assert rows[0][2:] == ['Producto Demo', '2', '99', '125.00']
    assert 'Producto Demo' in run('3\nPEDIDO-DEMO\n5\n')
    # Cantidad cero elimina el producto.
    run('4\nb\n99\n0\n-1\nc\n5\n')
    with sqlite3.connect(work / 'Inventario.db') as db:
        assert db.execute('SELECT COUNT(*) FROM productos WHERE "Código"=99').fetchone() == (0,)
print('OK: listado, alta, modificación, pedido, total, stock, historial y eliminación.')
