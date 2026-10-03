# TUIA — Procesamiento de Lenguaje Natural

Ejercicios y trabajos practicos de la materia NLP.
Tecnicatura Universitaria en Inteligencia Artificial — UNR.

## Integrantes del grupo

- Franco Renna
- Micaela Gómez
- Irma Carolina Ruiz
- Franco Esparza

## Qué hay en este repositorio

| Trabajo | Qué hace | Dónde está |
| --- | --- | --- |
| **TP1** — Extracción y procesamiento de texto | Scraper que recorre la categoría *Ciencia ficción* de Lectulandia y arma un dataset de 150 libros con su sinopsis. | `src/scraper.py`, `src/Libro.py`, `docs/diseno_extraccion.md`, `data/libros.csv` |
| **TP2** — Representación vectorial de texto | Sobre las sinopsis del TP1: embeddings de palabra (Word2Vec propio y pre-entrenado), embeddings de oración (SBERT), persistencia en Postgres con `pgvector` y búsqueda semántica evaluada contra TF-IDF. | `src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb`, `data/`, `models/` (no se sube) |

## Instalación (común a los dos trabajos)

Requiere Python 3.12 o 3.13.

```powershell
python -m venv .venv-NLP
.\.venv-NLP\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt` incluye las dependencias de los dos trabajos.

---

# TP1 — Extracción de datos

### Categoría seleccionada

Ciencia ficción

### Cantidad de libros extraídos

150

### Modelo de datos

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

### Instrucciones de instalación

Además de la instalación común (ver arriba), el scraper necesita el navegador de Playwright:

```powershell
playwright install chromium
```

### Instrucciones para ejecutar el programa

```powershell
python src/scraper.py
```

El script abre un navegador Chromium, recorre las páginas del género configurado, extrae una muestra aleatoria de libros y genera `data/libros.csv` con los datos obtenidos. Por defecto se ejecuta mostrando la ventana del navegador; para correrlo sin mostrarla, cambiar la constante `HEADLESS` a `True` al inicio de `src/scraper.py`.

### Principales dificultades encontradas

- Selectores CSS inconsistentes entre libros (autor, serie e imagen de portada no siempre están presentes), lo que obligó a validar cada campo antes de asignarlo en `Libro`.
- Tiempos de carga variables del sitio: fue necesario agregar esperas explícitas (`wait_for_timeout`) entre navegaciones para evitar extraer páginas incompletas.
- Paginación dinámica: el número de la última página se obtiene de forma dinámica.
- Volcado a CSV: se evaluaron distintas formas de serializar los objetos `Libro` (módulo `csv` estándar vs. `pandas`) para manejar correctamente listas (géneros) y campos opcionales.
- Pérdida de datos ante errores tardíos: en una corrida se extrajeron los 150 libros pero el guardado final falló (carpeta `data/` inexistente), perdiéndose todo el progreso por no haberse guardado nada hasta ese momento. Se resolvió guardando cada registro en el CSV apenas se procesa, en lugar de acumular todo en memoria y escribir una sola vez al final.
- Manejo de errores por ficha: una falla de red o de parseo en un libro puntual no debe interrumpir toda la extracción; cada ficha se procesa dentro de un bloque que registra el error por consola y continúa con la siguiente.
- Tipo de dato de autores/géneros: a pedido de la cátedra, se reemplazó el campo de texto separado por `" | "` por un array en formato JSON (parseable con `json.loads`), y se agregó una columna `id` tomada del identificador propio del sitio (`data-book`).

---

# TP2 — Embeddings y búsqueda semántica

Notebook: `src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb`. Parte de `data/libros.csv` (salida del TP1) y sigue las partes del enunciado:

| Parte | Qué hace | Estado |
| --- | --- | --- |
| Primer análisis del corpus | Géneros, estabilidad de TF-IDF según el tamaño del corpus, vocabulario promocional, idioma | Hecho |
| A. Preparar el corpus | Dos versiones de cada sinopsis: cruda (para SBERT) y limpia (para TF-IDF) | Hecho |
| B. Word2Vec propio vs pre-entrenado | Entrena Word2Vec sobre el corpus, lo compara con `SBW-vectors-300-min5` y arma un vector por documento promediando palabras | Hecho |
| C. Modelo de oración | Embeddings con `distiluse-base-multilingual-cased-v1` y conteo de sinopsis truncadas | Hecho |
| D. Comparación y visualización | Rankings lado a lado, distribución de similitudes entre pares, proyección 2D (PCA) por género | Hecho |
| E. Persistencia | Tablas en Supabase con `pgvector`, carga de los vectores e índice HNSW | Hecho |
| F. Búsqueda semántica | `buscar(consulta, k)` resuelta en SQL con filtro por género, y demostración del problema de recall con filtro | Hecho |
| Evaluación | `queries.json`, precision@k contra TF-IDF y contra el azar | `queries.json` armado, en revisión (ver `docs/revision_queries.md`); falta precision@k |

## Instrucciones para ejecutar el notebook

**En local (VS Code o Jupyter).** Abrir el notebook, elegir el kernel `.venv-NLP` y ejecutar todas las celdas en orden. También se puede ejecutar completo desde la terminal:

```powershell
jupyter nbconvert --to notebook --execute --inplace src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb
```

**En Google Colab.**

1. Subir el notebook a Colab (Archivo → Subir notebook).
2. Abrir el panel *Secrets* (ícono de llave en la barra izquierda), crear el secreto `DATABASE_URL` con la cadena **Session pooler** de Supabase y activar "Acceso desde el notebook". Ver la sección de conexión más abajo.
3. Ejecutar las celdas en orden. La primera instala lo que Colab no trae (`gensim`, `psycopg2-binary`, `python-dotenv`).
4. Cuando las celdas lo pidan, subir `data/libros.csv` (al principio) y `queries.json` (en la Parte D). El repositorio es privado, no se pueden descargar por URL.

En Colab los archivos se pierden al cerrar la sesión: el modelo SBW se vuelve a descargar cada vez (unos minutos) y los archivos que genera el notebook quedan en `/content/data`.

Qué pasa la primera vez que se ejecuta:

- Se descarga el modelo `SBW-vectors-300-min5.bin.gz` (1,1 GB) desde el sitio del SBWCE (`cs.famaf.unc.edu.ar/~ccardellino/SBWCE/`) a `models/`, y se guarda una copia en el formato de gensim (1,2 GB más) para que las siguientes cargas tarden segundos. La carpeta `models/` está en `.gitignore`.
- Se descarga el modelo SBERT (unos 500 MB) a la caché de Hugging Face.

El resultado es el mismo en cada ejecución: los muestreos y el entrenamiento de Word2Vec usan una semilla fija (`SEMILLA = 42`) y un solo hilo.

## Conexión a Supabase (Parte E)

La cadena de conexión **nunca** se escribe en el notebook. Se lee de afuera:

- **En local:** copiar `.env.example` como `.env` en la raíz del repo y completar la contraseña. El archivo `.env` está en `.gitignore`.
- **En Colab:** panel *Secrets* (ícono de llave) → crear el secreto `DATABASE_URL` y habilitar el acceso para el notebook.

La cadena se copia del panel de Supabase, botón **Connect**. Hay dos:

| Cadena | Host | Dónde funciona |
| --- | --- | --- |
| **Session pooler** (recomendada) | `aws-0-<región>.pooler.supabase.com` | En cualquier red y en Colab. |
| Direct connection | `db.<proyecto>.supabase.co` | Solo en redes con IPv6. No funciona en Colab. |

Si la conexión falla con un error de nombre de host, es que se está usando la conexión directa en una red sin IPv6: cambiar a la cadena del pooler.

Sin credencial, el notebook se ejecuta igual: las celdas que usan la base avisan que se omiten.

Los proyectos gratuitos de Supabase **se pausan a los 7 días sin actividad**. Si la conexión falla, entrar al panel y reactivar el proyecto (tarda cerca de medio minuto).

## Modelo de datos

### `data/libros_preprocesados.csv`

Las mismas 150 filas y columnas de `data/libros.csv` (ver el modelo de datos del TP1), más dos columnas:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `sinopsis_emb` | string | Versión **cruda**: la sinopsis original, solo con los espacios normalizados. Es la entrada del modelo de oración (SBERT). |
| `sinopsis_limpio` | string | Versión **limpia**: minúsculas, sin puntuación, sin números, sin stopwords (lista de español de NLTK) y sin palabras de una letra, con los tokens separados por un espacio. Es la entrada de TF-IDF. |

`autores` y `generos` siguen guardados como array JSON, igual que en `libros.csv`.

### `data/libros_vectores.pkl`

DataFrame de pandas (se lee con `pd.read_pickle`) con las columnas anteriores y los vectores de cada libro. En este archivo `autores` y `generos` son listas de Python.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `vec_propio` | array de 100 `float32` | Promedio de los vectores de palabra del Word2Vec entrenado sobre el corpus, con norma 1. |
| `cob_propio` | float (0 a 1) | Cobertura: fracción de las palabras de la sinopsis (sin stopwords) que tienen vector en ese modelo. |
| `vec_sbw` | array de 300 `float32` | Promedio de los vectores de palabra de `SBW-vectors-300-min5`, con norma 1. |
| `cob_sbw` | float (0 a 1) | Cobertura con el vocabulario de SBW. |
| `n_tokens_sbert` | entero | Cantidad de tokens de la sinopsis según el tokenizador de SBERT. Si supera 128, el modelo la trunca. |
| `vec_sbert` | array de 512 `float32` | Embedding de la sinopsis cruda con `distiluse-base-multilingual-cased-v1`, con norma 1. |

Un vector vale `None` si no se pudo calcular (ninguna palabra con vector, norma cero o valores no finitos). En el corpus actual no hay ninguno.

### `data/emb_sbert.npy`

Matriz de NumPy de 150 × 512 (`float32`) con los embeddings de SBERT. La fila *i* corresponde a la fila *i* de `libros_preprocesados.csv`.

### `queries.json`

Conjunto de evaluación propio: 18 consultas en lenguaje natural y, para cada una, los libros del corpus que se consideran relevantes. Se armó leyendo las 150 sinopsis, **antes** de ejecutar ningún buscador, para que los resultados de los modelos no influyeran en qué se marca como relevante.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | string | Identificador de la consulta (`q01` a `q18`). |
| `consulta` | string | Texto de la consulta, como la escribiría un usuario. |
| `criterio` | string | Qué se consideró relevante para esa consulta y qué no. |
| `sin_palabras_en_comun` | booleano | `true` en las consultas diseñadas para no compartir ninguna palabra con los libros relevantes (después de la limpieza de TF-IDF). Son `q17` y `q18`. |
| `relevantes` | array de objetos | Libros relevantes, cada uno con `id` (el mismo de `libros.csv`) y `titulo`. |

`docs/revision_queries.md` muestra cada consulta con sus libros relevantes y el comienzo de sus sinopsis, y explica cómo revisar el conjunto antes de la evaluación.

### Tablas en Supabase (Postgres + `pgvector`)

Una tabla por modelo, porque la dimensión del vector es parte del tipo de la columna y los espacios de dos modelos no son comparables entre sí. Las dos tablas tienen las mismas columnas (todas `NOT NULL`) y 150 filas; solo cambia la dimensión de `embedding`.

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `id` | `text` (clave primaria) | Mismo `id` que en `libros.csv`. |
| `titulo` | `text` | Título del libro. |
| `generos` | `text[]` | Géneros del libro, como array para poder filtrar en SQL (`'Terror' = ANY(generos)`). |
| `embedding` | `vector(300)` en `libros_word2vec`, `vector(512)` en `libros_sbert` | Promedio de vectores de palabra de SBW (`vec_sbw`) y embedding de SBERT (`vec_sbert`), respectivamente. |

Cada tabla tiene un índice HNSW sobre `embedding` con la opclass `vector_cosine_ops`, que corresponde al operador de distancia de coseno (`<=>`) que usa la búsqueda: `libros_word2vec_embedding_hnsw` y `libros_sbert_embedding_hnsw`.

El notebook borra y vuelve a crear las tablas en cada ejecución, y antes de insertar descarta los vectores nulos, no finitos o de norma cero.

## Principales dificultades encontradas

- **Conexión a Supabase solo por IPv6**: la cadena de conexión directa no resolvía en una red sin IPv6. Se documentó el uso del *Session pooler*, que es además el único que funciona en Colab.
- **Corpus chico para entrenar embeddings**: 150 sinopsis suman unas 19.000 palabras y dos tercios del vocabulario aparece una sola vez. El Word2Vec propio solo cubre la mitad de las palabras de contenido de cada sinopsis.
- **Truncado silencioso en SBERT**: el modelo acepta 128 tokens y tres de cada cuatro sinopsis los superan. El modelo no avisa; hubo que contarlo con su tokenizador.
- **Preprocesamiento distinto por modelo**: la limpieza que sirve para TF-IDF perjudica a SBERT, y Word2Vec necesita una tercera tokenización que conserva las stopwords.
- **Credenciales**: una primera versión del notebook tenía la cadena de conexión escrita en una celda. Se pasó a leerla de un archivo `.env` que no se sube al repositorio.
- **Reproducibilidad entre máquinas**: rutas relativas a `src/`, modelos descargados a mano y dependencias sin declarar hacían que el notebook solo corriera en una computadora. Se resolvió detectando la raíz del proyecto, descargando SBW desde el notebook y completando `requirements.txt`.
