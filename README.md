# TUIA — Procesamiento de Lenguaje Natural

Ejercicios y trabajos practicos de la materia NLP.
Tecnicatura Universitaria en Inteligencia Artificial — UNR.

## Integrantes del grupo

- Franco Renna
- Micaela Gómez
- Irma Carolina Ruiz
- Franco Esparza

## Categoría seleccionada

Ciencia ficción

## Cantidad de libros extraídos

150

## Modelo de datos

Cada fila de `data/libros.csv` representa un libro, con las siguientes columnas:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | string | Identificador de la ficha en Lectulandia (atributo `data-book` del sitio). Si el sitio no lo trae, se genera un `fallback-<n>` propio para no dejar filas sin id. |
| `titulo` | string | Título del libro. |
| `autores` | array (JSON) | Autor o autores del libro, ej. `["Isaac Asimov"]`. Se guarda como string JSON de array (no como texto separado por comas), para poder recorrerlo con `json.loads(fila["autores"])`. |
| `generos` | array (JSON) | Género o géneros que la ficha declara, ej. `["Ciencia ficción", "Novela"]`. Mismo formato que `autores`. |
| `serie` | string | Serie a la que pertenece el libro, si corresponde; cadena vacía si no pertenece a ninguna. |
| `sinopsis` | string | Texto completo de la sinopsis, normalizado (sin saltos de línea ni espacios repetidos). |
| `url_libro` | string | Dirección completa de la ficha del libro en Lectulandia. |
| `categoria_origen` | string | Categoría por la que el libro ingresó al dataset (siempre "Ciencia ficción" en esta entrega). |
| `fecha_extraccion` | string (fecha) | Fecha y hora en que se obtuvo el registro, formato `YYYY-MM-DD HH:MM:SS`. |
| `url_portada` | string | Dirección de la imagen de portada del libro. |

## Instrucciones de instalación

```powershell
python -m venv .venv-NLP
.\.venv-NLP\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Instrucciones para ejecutar el programa

```powershell
python src/scraper.py
```

El script abre un navegador Chromium, recorre las páginas del género configurado, extrae una muestra aleatoria de libros y genera `data/libros.csv` con los datos obtenidos. Por defecto se ejecuta mostrando la ventana del navegador; para correrlo sin mostrarla, cambiar la constante `HEADLESS` a `True` al inicio de `src/scraper.py`.

## Principales dificultades encontradas

- Selectores CSS inconsistentes entre libros (autor, serie e imagen de portada no siempre están presentes), lo que obligó a validar cada campo antes de asignarlo en `Libro`.
- Tiempos de carga variables del sitio: fue necesario agregar esperas explícitas (`wait_for_timeout`) entre navegaciones para evitar extraer páginas incompletas.
- Paginación dinámica: el número de la última página se obtiene de forma dinámica.
- Volcado a CSV: se evaluaron distintas formas de serializar los objetos `Libro` (módulo `csv` estándar vs. `pandas`) para manejar correctamente listas (géneros) y campos opcionales.
- Pérdida de datos ante errores tardíos: en una corrida se extrajeron los 150 libros pero el guardado final falló (carpeta `data/` inexistente), perdiéndose todo el progreso por no haberse guardado nada hasta ese momento. Se resolvió guardando cada registro en el CSV apenas se procesa, en lugar de acumular todo en memoria y escribir una sola vez al final.
- Manejo de errores por ficha: una falla de red o de parseo en un libro puntual no debe interrumpir toda la extracción; cada ficha se procesa dentro de un bloque que registra el error por consola y continúa con la siguiente.
- Tipo de dato de autores/géneros: a pedido de la cátedra, se reemplazó el campo de texto separado por `" | "` por un array en formato JSON (parseable con `json.loads`), y se agregó una columna `id` tomada del identificador propio del sitio (`data-book`).
