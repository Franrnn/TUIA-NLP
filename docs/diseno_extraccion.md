# Diseño de la extracción
 
**Unidad 1 — Extracción y procesamiento de texto**
Procesamiento del Lenguaje Natural — Tecnicatura Universitaria en Inteligencia Artificial, UNR
 
---
 
## 1. Categoría seleccionada
 
- **Nombre de la categoría:** Ciencia ficción
- **URL de la categoría:** `https://ww3.lectulandia.co/genero/ciencia-ficcion/`
- **Cantidad de libros que se propone extraer:** 150
### Criterio utilizado para seleccionar las páginas
 
Se recorre de forma secuencial la totalidad del listado de la categoría (182 páginas, con 24 fichas por página salvo la última, que contiene 15) para construir la lista completa de URLs. Ese conjunto, de aproximadamente 4.359 libros, constituye el universo de muestreo dentro de la misma ejecución del programa; las URLs repetidas se descartan (conservando el primer orden de aparición) antes de muestrear.
 
Sobre ese universo se extrae una muestra aleatoria simple de 150 fichas, utilizando una semilla fija que permite reproducir exactamente la misma selección en corridas sucesivas.
 
En este sentido, se descarta la alternativa de limitarse a las primeras páginas porque el orden del listado no responde a ningún criterio explícito y no se puede garantizar que los primeros resultados sean representativos del conjunto del género. El recorrido exhaustivo previo al sorteo asegura que todos los libros tengan la misma probabilidad de integrar la muestra.
 
La cantidad total del universo se confirma con el conteo efectivo de URLs únicas obtenidas al finalizar el recorrido. Las diferencias respecto de esta estimación se documentan como incidencias de la extracción.
 
---
 
## 2. Datos que se extraerán
 
| Campo | Descripción |
| --- | --- |
| `id` | Identificador del libro (ver convenciones) |
| `titulo` | Título del libro |
| `autores` | Autor o autores |
| `generos` | Género o géneros |
| `serie` | Serie a la que pertenece, si corresponde |
| `sinopsis` | Texto completo de la sinopsis |
| `url_libro` | Dirección de la ficha |
| `categoria_origen` | Categoría seleccionada por el grupo |
| `fecha_extraccion` | Fecha en que se obtuvo el registro |
| `url_portada` | Dirección de la imagen de portada (campo opcional) |
 
**Convenciones adoptadas**
 
- `id` es el identificador propio que Lectulandia le asigna a la ficha (atributo `data-book`, el mismo que aparece en el listado como `id="post-<id>"`). Si alguna ficha no lo trajera, se genera un identificador propio (`fallback-<n>`) para no dejar filas sin `id`.
- `autores` y `generos` pueden contener varios valores. Se almacenan como un **array en formato JSON** dentro de la celda (ej. `["Autor A", "Autor B"]`), de modo que cualquier lector del CSV pueda recorrerlos con `json.loads(...)` en vez de tener que parsear un separador de texto. Es el equivalente, dentro de una celda de CSV, a un campo `jsonb`/array nativo en una base de datos.
- `generos` registra todos los géneros que la ficha declara para el libro. `categoria_origen` deja constancia de la categoría por la cual el libro ingresó al dataset. Ambos campos pueden coincidir parcialmente, pero no son equivalentes.
- Los campos ausentes se representan de manera uniforme como cadena vacía en todos los registros (los arrays vacíos se guardan como `[]`).
---
 
## 3. Localización de los datos
 
| Dato | Tipo de página | Etiqueta HTML | Selector propuesto |
| --- | --- | --- | --- |
| `id` | Ficha individual | Atributo `data-book` en los botones de acciones ("Lo quiero leer", etc.) | `[data-book]` |
| Título | Ficha individual | `<h1>` dentro de `<div id="title">` | `#title h1` |
| Autores | Ficha individual | `<a class="dinSource">` dentro de `<div id="autor">` | `#autor a.dinSource` |
| Géneros | Ficha individual | `<a class="dinSource">` dentro de `<div id="genero">` | `#genero a.dinSource` |
| Serie | Ficha individual | `<a class="dinSource">` dentro de `<div id="serie">` | `#serie a.dinSource` |
| Sinopsis | Ficha individual | Contenido variable dentro de `<div id="sinopsis">` (ver observación) | `#sinopsis` |
| Portada | Ficha individual | `<img>` dentro de `<div id="cover">` | `#cover img` |
| `url_libro` | — | — | Sin selector: es la URL obtenida en la fase de recolección del listado y utilizada para acceder a la ficha |
| `categoria_origen` | — | — | Sin selector: valor constante definido en el script |
| `fecha_extraccion` | — | — | Sin selector: la genera el programa al guardar cada registro |
 
Los selectores fueron obtenidos inspeccionando el HTML del sitio con las herramientas de desarrollo del navegador, y re-verificados contra el HTML real del sitio antes de cerrar la implementación.
 
### Observaciones sobre la estructura del HTML
 
**Ámbito de búsqueda.** La ficha individual incluye, antes del contenido del libro, un listado de otros títulos recomendados con su propio encabezado, autor y fragmento de sinopsis. Todos los selectores se aplican dentro del contenedor `div#book`, que delimita el bloque de la ficha y excluye ese listado. De no acotarse el ámbito, la extracción devolvería los datos del primer libro recomendado en lugar de los del libro visitado, sin generar ningún error visible.
 
**Etiquetas de campo.** Los bloques `#autor`, `#serie` y `#genero` comparten la misma estructura: un `<span class="tagTitle">` con la etiqueta literal del campo ("Autor:", "Libro N de:", "Generos:") seguido de uno o más `<a class="dinSource">` con el contenido. Los selectores apuntan directamente a los enlaces, de modo que no es necesario depurar el prefijo del texto extraído.
 
**Cardinalidad.** `#autor` y `#genero` devuelven habitualmente más de un elemento y deben recorrerse en su totalidad. `#serie` devuelve un único elemento o ninguno, según el libro pertenezca o no a una serie.

**Identificador de la ficha.** El atributo `data-book` aparece repetido varias veces dentro de `#book` (en los botones "Lo quiero leer", "Lo estoy leyendo", etc.), siempre con el mismo valor numérico para una misma ficha, y coincide con el `id="post-<id>"` que esa misma ficha tiene cuando aparece listada en el catálogo. Se toma el primer elemento que lo declara.
 
**Tratamiento de la sinopsis.** El sitio no envuelve la sinopsis de forma consistente: según el libro, el contenido de `#sinopsis` aparece dentro de un `<span>`, dentro de un `<p class="description">`, o como texto suelto directamente dentro del `<div>`, sin ninguna etiqueta envolvente. Por eso la extracción toma el texto completo del contenedor `#sinopsis` en lugar de apuntar a una etiqueta hija específica. Ese texto tampoco es plano: incluye etiquetas de énfasis intercaladas (títulos de obras, expresiones destacadas) y separadores `<br>` entre párrafos. La extracción debe recuperar el texto de todos los nodos descendientes; tomar únicamente los nodos de texto directos produciría un resultado incompleto que omite los fragmentos en cursiva. Los saltos de párrafo se convierten en espacio y las secuencias de espacios en blanco se colapsan, de modo que la sinopsis se almacena como un único párrafo de texto plano. No se normalizan comillas, guiones ni otros signos tipográficos: el texto se conserva tal como fue publicado.
 
---
 
## 4. Estrategia de extracción
 
### Fase 1
 
1. Abrir la página de la categoría con Playwright. El navegador se abre visible por defecto; una constante (`HEADLESS`) permite ejecutarlo sin mostrar la ventana.
2. Obtener del paginador el número total de páginas del listado.
3. Recorrer secuencialmente la totalidad de las páginas, obteniendo el HTML de cada una mediante Playwright e incorporando una pausa entre visitas.
4. Analizar cada HTML con BeautifulSoup y extraer las URL de las fichas de los libros.
5. Consolidar las URL descartando repetidos (se conserva el primer orden de aparición), dentro de la misma ejecución del programa.
### Fase 2
 
6. Extraer sobre esa lista una muestra aleatoria simple de 150 fichas, utilizando una semilla fija.
### Fase 3
 
7. Visitar con Playwright cada URL de la muestra, con una pausa entre visitas.
8. Analizar el HTML de cada ficha con BeautifulSoup, acotando la búsqueda al contenedor `#book`, y extraer título, autores, géneros, serie, sinopsis y portada según los selectores indicados en el punto 3.
9. Completar los campos generados por el programa: `url_libro`, `categoria_origen` y `fecha_extraccion`.
10. Normalizar el contenido según las convenciones establecidas en el punto 2.
11. Volcar cada registro al CSV apenas se procesa, de modo que una interrupción o un error posterior no implique perder lo ya extraído. Los errores en una ficha (de red, de parseo, etc.) se registran por consola y la ejecución continúa con la siguiente URL de la muestra.
### Fase 4
 
12. Verificar la ausencia de registros duplicados por `url_libro`.
13. Aplicar los controles mínimos: presencia de título, validez de las URL, cobertura de sinopsis, limpieza de espacios y saltos, consistencia en la representación de los campos ausentes y cantidad final dentro del rango establecido. El propio script imprime estos controles al finalizar la extracción.
14. El archivo `data/libros.csv` queda generado con pandas, en codificación UTF-8, desde el inicio de la ejecución (encabezado) y con cada fila agregada de forma incremental durante la Fase 3.

 
---
 
## 5. Restricciones
 
Conforme a lo establecido en la consigna, la extracción se limita a los metadatos y las sinopsis de acceso público. No se descargan libros, archivos EPUB, PDF ni ningún otro contenido. Se incorpora una pausa entre las páginas visitadas para no generar una carga excesiva sobre el sitio.