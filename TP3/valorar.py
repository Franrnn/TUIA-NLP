# -*- coding: utf-8 -*-
"""Paso 3 del TP3: registrar las preferencias del lector.

Muestra los libros del catalogo limpio de a uno y guarda la respuesta.
Se ejecuta desde la raiz del repositorio:

    .\\.venv\\Scripts\\python.exe TP3\\valorar.py

Guarda cada respuesta en el momento, asi que se puede cortar con "q" (o con
Ctrl+C) y retomar mas tarde: al volver a abrirlo sigue donde habia quedado.
"""
import csv
import datetime as dt
import os
import shutil
import sys
import textwrap
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
RUTA_CATALOGO = BASE / "catalogo_limpio.csv"
RUTA_LOG = BASE / "salidas" / "valoraciones_log.csv"

# Lo que pide la consigna: al menos 100 respuestas validas y 20 de cada clase.
VALIDAS_OBJETIVO = 100
POR_CLASE_OBJETIVO = 20

AYUDA = """\
  1       me interesaria leerlo
  0       no me interesaria leerlo
  Enter   no me decido (queda sin valorar)
  s       esto es spam que el Paso 2 no detecto
  q       salir y seguir mas tarde
"""


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def cargar_respondidos():
    """Los slug que ya tienen respuesta, para no volver a preguntarlos."""
    if not RUTA_LOG.exists():
        return set()
    previas = pd.read_csv(RUTA_LOG, keep_default_na=False)
    return set(previas["slug"])


def contar(respuestas):
    unos = sum(1 for r in respuestas if r == "1")
    ceros = sum(1 for r in respuestas if r == "0")
    return unos, ceros


def barra_de_progreso(respuestas):
    unos, ceros = contar(respuestas)
    validas = unos + ceros
    faltan = max(0, VALIDAS_OBJETIVO - validas)
    return (f"valoradas {validas}/{VALIDAS_OBJETIVO}"
            f"   me interesa {unos}/{POR_CLASE_OBJETIVO}"
            f"   no me interesa {ceros}/{POR_CLASE_OBJETIVO}"
            f"   faltan {faltan}"
            f"   (vistos {len(respuestas)})")


def objetivo_cumplido(respuestas):
    unos, ceros = contar(respuestas)
    return (unos + ceros >= VALIDAS_OBJETIVO
            and unos >= POR_CLASE_OBJETIVO
            and ceros >= POR_CLASE_OBJETIVO)


def main():
    if not RUTA_CATALOGO.exists():
        sys.exit(f"No encuentro {RUTA_CATALOGO}. Hay que ejecutar antes el Paso 2 del notebook.")

    libros = pd.read_csv(RUTA_CATALOGO, keep_default_na=False)
    # El mismo orden que usa el notebook. No cambiar la semilla.
    libros = libros.sample(frac=1, random_state=42).reset_index(drop=True)

    respondidos = cargar_respondidos()
    respuestas = []
    if RUTA_LOG.exists():
        respuestas = pd.read_csv(RUTA_LOG, keep_default_na=False)["respuesta"].astype(str).tolist()

    RUTA_LOG.parent.mkdir(exist_ok=True)
    archivo_nuevo = not RUTA_LOG.exists()
    ancho = min(shutil.get_terminal_size((100, 30)).columns - 4, 96)

    with open(RUTA_LOG, "a", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        if archivo_nuevo:
            escritor.writerow(["orden", "slug", "respuesta", "momento"])
            f.flush()

        for orden, libro in libros.iterrows():
            if libro["slug"] in respondidos:
                continue

            limpiar_pantalla()
            print(barra_de_progreso(respuestas))
            if objetivo_cumplido(respuestas):
                print("Ya alcanzaste el objetivo. Podes seguir valorando o salir con 'q'.")
            print("-" * ancho)
            print(textwrap.fill(str(libro["title"]), ancho))
            print("-" * ancho)
            print(textwrap.fill(str(libro["synopsis"]), ancho))
            print("-" * ancho)
            print(AYUDA)

            try:
                respuesta = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nCortado. Lo que respondiste quedo guardado.")
                break

            if respuesta == "q":
                break
            if respuesta not in ("1", "0", "", "s"):
                continue  # tecla que no es ninguna de las opciones: se vuelve a preguntar

            escritor.writerow([orden, libro["slug"], respuesta,
                               dt.datetime.now().isoformat(timespec="seconds")])
            f.flush()  # se escribe en el disco en el momento, no al final
            respondidos.add(libro["slug"])
            respuestas.append(respuesta)

    limpiar_pantalla()
    print(barra_de_progreso(respuestas))
    if objetivo_cumplido(respuestas):
        print("\nObjetivo cumplido. Ahora corre el Paso 3 del notebook para armar preferencias.csv.")
    else:
        unos, ceros = contar(respuestas)
        print(f"\nTodavia falta. Volve a ejecutar este script cuando quieras seguir.")
        if unos < POR_CLASE_OBJETIVO:
            print(f"  faltan {POR_CLASE_OBJETIVO - unos} libros que te interesen")
        if ceros < POR_CLASE_OBJETIVO:
            print(f"  faltan {POR_CLASE_OBJETIVO - ceros} libros que no te interesen")
    print(f"\nRespuestas guardadas en {RUTA_LOG}")


if __name__ == "__main__":
    main()
