CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic
LDLIBS = -lsqlite3

.PHONY: all run init test clean
all: proyecto_pp

proyecto_pp: proyecto_pp.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

run: proyecto_pp
	./proyecto_pp

init:
	sqlite3 Inventario.db < sql/inicializar.sql

test: proyecto_pp
	python3 tests/smoke_test.py

clean:
	rm -f proyecto_pp
