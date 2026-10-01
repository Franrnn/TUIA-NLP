# TUIA — Procesamiento de Lenguaje Natural

Ejercicios y trabajos practicos de la materia NLP.
Tecnicatura Universitaria en Inteligencia Artificial — UNR.

## Integrantes del grupo

- Franco Renna
- Micaela 
- Carolina 
- Franco Esparza

## Categoría seleccionada

Ciencia ficción

## Cantidad de libros extraídos

150

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

El script abre un navegador Chromium (no headless), recorre las páginas del género configurado, extrae una muestra aleatoria de libros y genera `libros.csv` con los datos obtenidos.

## Principales dificultades encontradas

- Selectores CSS inconsistentes entre libros (autor, serie e imagen de portada no siempre están presentes), lo que obligó a validar cada campo antes de asignarlo en `Libro`.
- Tiempos de carga variables del sitio: fue necesario agregar esperas explícitas (`wait_for_timeout`) entre navegaciones para evitar extraer páginas incompletas.
- Paginación dinámica: el número de la última página se obtiene de forma dinámica.
- Volcado a CSV: se evaluaron distintas formas de serializar los objetos `Libro` (módulo `csv` estándar vs. `pandas`) para manejar correctamente listas (géneros) y campos opcionales.
