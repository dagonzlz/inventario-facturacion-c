CREATE TABLE IF NOT EXISTS productos (
    Producto TEXT,
    Cantidad INTEGER,
    "Código" INTEGER,
    Precio REAL
);
INSERT INTO productos (Producto, Cantidad, "Código", Precio)
SELECT 'Varilla de Plata', 21, 1, 3500.0
WHERE NOT EXISTS (SELECT 1 FROM productos WHERE "Código" = 1);
INSERT INTO productos (Producto, Cantidad, "Código", Precio)
SELECT 'Varilla de Níquel', 14, 2, 7600.0
WHERE NOT EXISTS (SELECT 1 FROM productos WHERE "Código" = 2);
