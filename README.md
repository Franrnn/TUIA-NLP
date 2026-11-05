# TUIA — Procesamiento de Lenguaje Natural

Trabajos prácticos de la materia Procesamiento de Lenguaje Natural, Tecnicatura Universitaria en Inteligencia Artificial (UNR).

**Integrantes:** Franco Renna · Micaela Gómez · Irma Carolina Ruiz · Franco Esparza

## Qué hay en este repositorio

| Trabajo | Qué hace | Dónde está |
| --- | --- | --- |
| **TP1** — Extracción de texto | Scraper que recorre la categoría *Ciencia ficción* de Lectulandia y arma un dataset de 150 libros con sus metadatos y su sinopsis. | `src/scraper.py`, `src/Libro.py`, `docs/diseno_extraccion.md`, `data/libros.csv` |
| **TP2** — Embeddings y búsqueda semántica | Sobre las sinopsis del TP1: compara TF-IDF, Word2Vec (propio y pre-entrenado) y SBERT, guarda los vectores en Postgres con `pgvector`, busca por similitud y evalúa los modelos con un conjunto propio de consultas. | `src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb`, `queries.json`, `docs/informe.pdf`, `data/` |
| **TP3** — Recomendador personalizado | Sobre un catálogo ampliado de 8747 libros que la cátedra contaminó a propósito: primero lo audita (limpieza, expresiones regulares, detección de idioma, NER, clasificación de oraciones y similitud) y después aprende las preferencias de un lector para recomendarle libros. | `TP3/` |

## Instalación

Requiere Python 3.12 o 3.13.

```powershell
python -m venv .venv-NLP
.\.venv-NLP\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt` incluye las dependencias de los tres trabajos. Para volver a ejecutar el scraper del TP1 hace falta además el navegador de Playwright:

```powershell
playwright install chromium
```

El TP3 usa un modelo de spaCy en español, que no se instala con `requirements.txt`:

```powershell
python -m spacy download es_core_news_lg
```

## Ejecución

### TP1: scraper

```powershell
python src/scraper.py
```

Abre un navegador Chromium, recorre el listado del género, extrae una muestra aleatoria de 150 libros y genera `data/libros.csv`. Para ejecutarlo sin mostrar la ventana, cambiar la constante `HEADLESS` a `True` al inicio de `src/scraper.py`. Sobrescribe el CSV existente y tarda varios minutos.

### TP2: notebook

**En local (VS Code o Jupyter).** Abrir `src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb`, elegir el kernel `.venv-NLP` y ejecutar todas las celdas en orden. También se puede ejecutar completo desde la terminal:

```powershell
jupyter nbconvert --to notebook --execute --inplace src/TP2_Renna_Gomez_Ruiz_Esparza.ipynb
```

**En Google Colab.**

1. Subir el notebook a Colab (Archivo → Subir notebook).
2. Abrir el panel *Secrets* (ícono de llave en la barra izquierda), crear el secreto `DATABASE_URL` con la cadena de conexión y activar "Acceso desde el notebook".
3. Ejecutar las celdas en orden. La primera instala lo que Colab no trae.
4. Cuando las celdas lo pidan, subir `data/libros.csv` (al principio) y `queries.json` (en la Parte D).

La primera ejecución descarga el modelo `SBW-vectors-300-min5` (1,1 GB, a la carpeta `models/`) y el modelo SBERT (unos 500 MB), y tarda varios minutos. El resultado es el mismo en cada ejecución: se usa una semilla fija.

### TP3: notebook

Abrir `TP3/TP3_Renna_Gomez_Ruiz_Esparza.ipynb`, elegir el kernel `.venv` y ejecutar las celdas en orden. También se puede ejecutar completo desde la terminal:

```powershell
jupyter nbconvert --to notebook --execute --inplace TP3/TP3_Renna_Gomez_Ruiz_Esparza.ipynb
```

Los archivos de entrada ya están en el repositorio: `TP3/catalogo_tp3.jsonl` (el catálogo de la cátedra, 8747 libros) y `TP3/consigna_tp3/tp3/muestra_etiquetada.csv` (500 libros con la etiqueta `contaminado`, que el Paso 2 usa para calibrar y medir los detectores).

La primera ejecución descarga el modelo de oración del TP2 (`distiluse-base-multilingual-cased-v1`, unos 500 MB). El TP3 no usa la base de datos.

**La carpeta `TP3/salidas/`** guarda resultados intermedios para no recalcularlos. Los dos detectores lentos del Paso 2 —el de idioma y el clasificador, que recorren unas 60.000 oraciones— dejan ahí su resultado: la primera ejecución tarda unos 45 minutos y las siguientes, unos pocos. Esos dos archivos están en el repositorio, así que quien clone no tiene que esperar esa primera vez. Si se cambia algo del Paso 1 y la cantidad de libros deja de coincidir, las celdas cortan con un error y hay que borrarlos.

Todas las divisiones usan `random_state=42` y la semilla de `langdetect` queda fija, así que cada ejecución da el mismo resultado.

### TP3: valorar los libros (Paso 3)

El Paso 3 necesita que **una sola persona del grupo** valore los libros a mano. Eso no se hace en el notebook sino con un script aparte, porque lleva alrededor de una hora y conviene poder cortar y retomar:

```powershell
.\.venv\Scripts\python.exe TP3\valorar.py
```

Muestra un libro por pantalla, con su título y su sinopsis, y se responde con una tecla:

| Tecla | Significado |
| --- | --- |
| `1` | me interesaría leerlo |
| `0` | no me interesaría leerlo |
| `Enter` | no me decido; el libro queda sin valorar |
| `s` | es spam que el Paso 2 no detectó |
| `q` | salir y seguir más tarde |

Recorre el catálogo limpio en el mismo orden que el notebook (`sample(frac=1, random_state=42)`) y **guarda cada respuesta en el momento** en `TP3/salidas/valoraciones_log.csv`, así que se puede cortar en cualquier momento y al volver a abrirlo sigue donde había quedado. Arriba muestra cuántas respuestas faltan para llegar a las 100 válidas y a las 20 de cada clase que pide la consigna.

Cuando el objetivo esté cumplido, hay que volver a ejecutar el Paso 3 del notebook: de ahí sale `TP3/preferencias.csv`.

### Conexión a la base de datos (Supabase)

Las partes E y F y la parte avanzada usan una base Postgres en Supabase. La cadena de conexión **no está en el repositorio**: se entrega por separado.

- **En local:** copiar `.env.example` como `.env` en la raíz del repo y pegar ahí la cadena (`DATABASE_URL=...`). El archivo `.env` está en `.gitignore`.
- **En Colab:** cargarla como secreto `DATABASE_URL` (paso 2 de arriba).

Usar la cadena **Session pooler**, que funciona en cualquier red y en Colab. La de conexión directa (`db.<proyecto>.supabase.co`) solo funciona en redes con IPv6.

Sin la cadena, el notebook se ejecuta igual: las celdas que usan la base avisan que se omiten y el resto corre completo. El notebook entregado ya tiene guardadas las salidas de esas celdas.

## Modelo de datos

### `data/libros.csv` (salida del TP1)

Una fila por libro, 150 filas.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | string | Identificador de la ficha en Lectulandia (atributo `data-book` del sitio). Si el sitio no lo trae, se genera un `fallback-<n>`. |
| `titulo` | string | Título del libro. |
| `autores` | array (JSON) | Autor o autores, ej. `["Isaac Asimov"]`. Se guarda como string JSON y se recupera con `json.loads`. |
| `generos` | array (JSON) | Géneros que la ficha declara, ej. `["Ciencia ficción", "Novela"]`. Mismo formato que `autores`. |
| `serie` | string | Serie a la que pertenece el libro; cadena vacía si no pertenece a ninguna. |
| `sinopsis` | string | Texto completo de la sinopsis, sin saltos de línea ni espacios repetidos. |
| `url_libro` | string | Dirección de la ficha del libro en Lectulandia. |
| `categoria_origen` | string | Categoría por la que el libro ingresó al dataset (siempre "Ciencia ficción"). |
| `fecha_extraccion` | string (fecha) | Fecha y hora en que se obtuvo el registro, formato `YYYY-MM-DD HH:MM:SS`. |
| `url_portada` | string | Dirección de la imagen de portada. |

### `data/libros_preprocesados.csv`

Las mismas filas y columnas de `libros.csv`, más dos:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `sinopsis_emb` | string | Versión **cruda**: la sinopsis original, solo con los espacios normalizados. Es la entrada del modelo de oración (SBERT). |
| `sinopsis_limpio` | string | Versión **limpia**: minúsculas, sin puntuación, sin números, sin stopwords (lista de español de NLTK) y sin palabras de una letra. Es la entrada de TF-IDF. |

### `data/libros_vectores.pkl`

DataFrame de pandas (se lee con `pd.read_pickle`) con las columnas anteriores y los vectores de cada libro. En este archivo `autores` y `generos` son listas de Python.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `vec_propio` | array de 100 `float32` | Promedio de los vectores de palabra del Word2Vec entrenado sobre el corpus, con norma 1. |
| `cob_propio` | float (0 a 1) | Fracción de las palabras de la sinopsis (sin stopwords) que tienen vector en ese modelo. |
| `vec_sbw` | array de 300 `float32` | Promedio de los vectores de palabra de `SBW-vectors-300-min5`, con norma 1. |
| `cob_sbw` | float (0 a 1) | Lo mismo que `cob_propio`, con el vocabulario de SBW. |
| `n_tokens_sbert` | entero | Cantidad de tokens de la sinopsis según el tokenizador de SBERT. Si supera 128, el modelo la trunca. |
| `vec_sbert` | array de 512 `float32` | Embedding de la sinopsis cruda con `distiluse-base-multilingual-cased-v1`, con norma 1. |

`data/emb_sbert.npy` es la misma información de `vec_sbert` como matriz de NumPy de 150 × 512, con las filas en el orden de `libros_preprocesados.csv`.

### `data/chunks.pkl` y `data/emb_sbert_chunks.npy`

Parte avanzada del TP2. `chunks.pkl` es un DataFrame con una fila por fragmento de sinopsis (322 en total); `emb_sbert_chunks.npy` es la matriz de 322 × 512 con sus embeddings, en el mismo orden.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `libro_id` | string | `id` del libro al que pertenece el fragmento. |
| `titulo`, `generos` | string, lista | Copiados del libro. |
| `chunk_idx` | entero | Número de fragmento dentro del libro, empezando en 0. |
| `texto` | string | Oraciones consecutivas de la sinopsis que juntas no superan los 128 tokens de SBERT. |
| `n_tokens` | entero | Tokens del fragmento según el tokenizador de SBERT. |
| `vec` | array de 512 `float32` | Embedding del fragmento, con norma 1. |

### `queries.json`

Conjunto de evaluación del TP2: 18 consultas en lenguaje natural y, para cada una, los libros del corpus que se consideran relevantes.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | string | Identificador de la consulta (`q01` a `q18`). |
| `consulta` | string | Texto de la consulta. |
| `criterio` | string | Qué se consideró relevante para esa consulta y qué no. |
| `sin_palabras_en_comun` | booleano | `true` en las consultas diseñadas para no compartir ninguna palabra con sus libros relevantes (`q17` y `q18`). |
| `relevantes` | array de objetos | Libros relevantes, cada uno con `id` (el mismo de `libros.csv`) y `titulo`. |

### Tablas en Supabase (Postgres + `pgvector`)

Una tabla por modelo. `libros_word2vec` y `libros_sbert` tienen las mismas columnas y 150 filas; solo cambia la dimensión del vector.

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `id` | `text` (clave primaria) | Mismo `id` que en `libros.csv`. |
| `titulo` | `text` | Título del libro. |
| `generos` | `text[]` | Géneros del libro, como array para poder filtrar en SQL. |
| `embedding` | `vector(300)` en `libros_word2vec`, `vector(512)` en `libros_sbert` | Promedio de vectores de palabra de SBW y embedding de SBERT, respectivamente. |

`libros_sbert_chunks` guarda un vector por fragmento (322 filas):

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `libro_id`, `chunk_idx` | `text`, `int` (clave primaria compuesta) | Libro y número de fragmento. |
| `titulo`, `generos` | `text`, `text[]` | Copiados del libro. |
| `texto` | `text` | Texto del fragmento. |
| `embedding` | `vector(512)` | Embedding de SBERT del fragmento. |

Las tres tablas tienen un índice HNSW sobre `embedding` con la opclass `vector_cosine_ops`. El notebook las borra y las vuelve a crear en cada ejecución.

### Archivos del TP3

Entradas que entrega la cátedra:

| Archivo | Qué contiene |
| --- | --- |
| `TP3/catalogo_tp3.jsonl` | 8747 libros, uno por línea. Campos: `source_url`, `slug`, `title`, `authors`, `genres`, `seed_genre`, `series`, `series_number`, `cover_url`, `synopsis`, `synopsis_chars`, `scraped_at`. Algunos registros están contaminados y no se indica cuáles. |
| `TP3/consigna_tp3/tp3/muestra_etiquetada.csv` | 500 libros del mismo catálogo con `contaminado` (1 o 0). En los contaminados, `fragmento` trae el texto que se insertó. El 20 % está contaminado, bastante más que el catálogo completo. |

Salidas que genera el notebook:

| Archivo | Qué contiene |
| --- | --- |
| `TP3/salidas/catalogo_paso1.csv` | Los 8592 libros que quedan después del Paso 1, con `slug`, `title`, `authors`, `genres`, `series` y `synopsis`. Se regenera en segundos, así que no se sube al repositorio. |
| `TP3/sospechosos.csv` | Los 380 libros que la auditoría marca, con `slug` y `motivo`. El motivo combina con `+` los detectores que lo marcaron: `regex`, `normalizacion`, `idioma`, `clasificador`, `casi_duplicado`. |
| `TP3/catalogo_limpio.csv` | Los 8212 libros que quedan al sacar los sospechosos. **Es la entrada de los pasos 3 a 8**, y conviene no regenerarlo: el Paso 3 lo mezcla con `random_state=42` y el lector valora los libros en ese orden. |
| `TP3/salidas/deteccion_idioma_catalogo.csv` | Cache del detector de idioma: `slug` y `marcado`. |
| `TP3/salidas/deteccion_clasificador_catalogo.csv` | Cache del clasificador: `slug` y la `probabilidad` más alta entre las oraciones de cada sinopsis. |
| `TP3/salidas/valoraciones_log.csv` | Lo que respondió el lector en `valorar.py`, una fila por libro visto: `orden` (posición en el recorrido), `slug`, `respuesta` (`1`, `0`, vacío o `s`) y `momento`. Se escribe de a una fila, para poder cortar y retomar. |
| `TP3/preferencias.csv` | Un libro por fila con `slug`, `title`, `synopsis` e `interes` (1, 0 o vacío). El Paso 4 le agrega la columna `conjunto`. Las abstenciones se conservan: un libro sin valorar tiene preferencia desconocida, no es un 0. |
| `TP3/grupo11_sospechosos.csv` | Copia de `sospechosos.csv` con el nombre que pide la entrega. |
| `TP3/grupo11_preferencias.csv` | Copia de `preferencias.csv` con la columna `conjunto` (`entrenamiento` o `prueba`; vacía en las abstenciones), con el nombre que pide la entrega. |
| `TP3/salidas/embeddings_candidatos.npy` | Cache del Paso 8: embeddings (8112 × 512) de los libros del catálogo limpio que el lector no valoró. `embeddings_candidatos_slugs.csv` guarda sus `slug` en el mismo orden; si no coinciden con los candidatos, la celda los recalcula (unos 4 minutos). |

Los dos archivos de cache se leen por posición, así que las celdas comprueban que los `slug` coincidan con el catálogo antes de usarlos.
