# Diseño de la extracción
 
**Unidad 1 — Extracción y procesamiento de texto**
Procesamiento del Lenguaje Natural — Tecnicatura Universitaria en Inteligencia Artificial, UNR
 
---
 
## 1. Categoría seleccionada
 
- **Nombre de la categoría:** Ciencia ficción
- **URL de la categoría:** `https://ww3.lectulandia.co/genero/ciencia-ficcion/`
- **Cantidad de libros que se propone extraer:** 150
### Criterio utilizado para seleccionar las páginas
 
Se recorre de forma secuencial la totalidad del listado de la categoría (182 páginas, con 24 fichas por página salvo la última, que contiene 15) para construir la lista completa de URLs. Ese conjunto, de aproximadamente 4.359 libros, constituye el universo de muestreo y se guarda en un archivo intermedio junto con la fecha de recolección.
 
Sobre ese universo se extrae una muestra aleatoria simple de 150 fichas, utilizando una semilla fija que permite reproducir exactamente la misma selección. La lista de URLs se conserva por separado para que el sorteo pueda repetirse sobre el mismo universo aunque el sitio agregue nuevos títulos.
 
En este sentido, se descarta la alternativa de limitarse a las primeras páginas porque el orden del listado no responde a ningún criterio explícito y no se puede garantizar que los primeros resultados sean representativos del conjunto del género. El recorrido exhaustivo previo al sorteo asegura que todos los libros tengan la misma probabilidad de integrar la muestra.
 
La cantidad total del universo se confirma con el conteo efectivo de URLs únicas obtenidas al finalizar el recorrido. Las diferencias respecto de esta estimación se documentan como incidencias de la extracción.
 
---
 
## 2. Datos que se extraerán
 
| Campo | Descripción |
| --- | --- |
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
 
- `autores` y `generos` pueden contener varios valores. Se almacenan en un único campo de texto, unidos por el separador ` | ` (barra vertical con espacios), elegido para no entrar en conflicto con el delimitador del CSV.
- `generos` registra todos los géneros que la ficha declara para el libro. `categoria_origen` deja constancia de la categoría por la cual el libro ingresó al dataset. Ambos campos pueden coincidir parcialmente, pero no son equivalentes.
- Los campos ausentes se representan de manera uniforme como cadena vacía en todos los registros.
---
 
## 3. Localización de los datos
 
| Dato | Tipo de página | Etiqueta HTML | Selector propuesto |
| --- | --- | --- | --- |
| Título | Ficha individual | `<h1>` dentro de `<div id="title">` | `#title h1` |
| Autores | Ficha individual | `<a class="dinSource">` dentro de `<div id="autor">` | `#autor a.dinSource` |
| Géneros | Ficha individual | `<a class="dinSource">` dentro de `<div id="genero">` | `#genero a.dinSource` |
| Serie | Ficha individual | `<a class="dinSource">` dentro de `<div id="serie">` | `#serie a.dinSource` |
| Sinopsis | Ficha individual | `<span>` dentro de `<div id="sinopsis">` | `#sinopsis span` |
| Portada | Ficha individual | `<img>` dentro de `<div id="cover">` | `#cover img` |
| `url_libro` | — | — | Sin selector: es la URL obtenida en la fase de recolección del listado y utilizada para acceder a la ficha |
| `categoria_origen` | — | — | Sin selector: valor constante definido en el script |
| `fecha_extraccion` | — | — | Sin selector: la genera el programa al guardar cada registro |
 
Los selectores fueron obtenidos inspeccionando el HTML del sitio con las herramientas de desarrollo del navegador.
 
### Observaciones sobre la estructura del HTML
 
**Ámbito de búsqueda.** La ficha individual incluye, antes del contenido del libro, un listado de otros títulos recomendados con su propio encabezado, autor y fragmento de sinopsis. Todos los selectores se aplican dentro del contenedor `div#book`, que delimita el bloque de la ficha y excluye ese listado. De no acotarse el ámbito, la extracción devolvería los datos del primer libro recomendado en lugar de los del libro visitado, sin generar ningún error visible.
 
**Etiquetas de campo.** Los bloques `#autor`, `#serie` y `#genero` comparten la misma estructura: un `<span class="tagTitle">` con la etiqueta literal del campo ("Autor:", "Libro N de:", "Generos:") seguido de uno o más `<a class="dinSource">` con el contenido. Los selectores apuntan directamente a los enlaces, de modo que no es necesario depurar el prefijo del texto extraído.
 
**Cardinalidad.** `#autor` y `#genero` devuelven habitualmente más de un elemento y deben recorrerse en su totalidad. `#serie` devuelve un único elemento o ninguno, según el libro pertenezca o no a una serie.
 
**Tratamiento de la sinopsis.** El contenido de `#sinopsis span` no es texto plano: incluye etiquetas de énfasis intercaladas (títulos de obras, expresiones destacadas) y separadores `<br>` entre párrafos. La extracción debe recuperar el texto de todos los nodos descendientes; tomar únicamente los nodos de texto directos produciría un resultado incompleto que omite los fragmentos en cursiva. Los saltos de párrafo se convierten en espacio y las secuencias de espacios en blanco se colapsan, de modo que la sinopsis se almacena como un único párrafo de texto plano. No se normalizan comillas, guiones ni otros signos tipográficos: el texto se conserva tal como fue publicado.
 
---
 
## 4. Estrategia de extracción
 
### Fase 1
 
1. Abrir la página de la categoría con Playwright, en modo sin ventana.
2. Obtener del paginador el número total de páginas del listado.
3. Recorrer secuencialmente la totalidad de las páginas, obteniendo el HTML de cada una mediante Playwright e incorporando una pausa entre visitas.
4. Analizar cada HTML con BeautifulSoup y extraer las URL de las fichas de los libros.
5. Consolidar las URL en un conjunto sin repetidos y guardarlo en un archivo intermedio, junto con la fecha de recolección y el total obtenido.
### Fase 2
 
6. Cargar la lista de URLs desde el archivo intermedio y extraer una muestra aleatoria simple de 150 fichas, utilizando una semilla fija.
### Fase 3
 
7. Visitar con Playwright cada URL de la muestra, con una pausa entre visitas.
8. Analizar el HTML de cada ficha con BeautifulSoup y extraer título, autores, géneros, serie, sinopsis y portada, según los selectores indicados en el punto 3.
9. Completar los campos generados por el programa: `url_libro`, `categoria_origen` y `fecha_extraccion`.
10. Normalizar el contenido según las convenciones establecidas en el punto 2.
11. Volcar los registros de forma incremental, de modo que una interrupción no implique perder lo ya extraído. Los errores en una ficha se registran y la ejecución continúa con la siguiente.
### Fase 4
 
12. Verificar la ausencia de registros duplicados por `url_libro`.
13. Aplicar los controles mínimos: presencia de título, validez de las URL, cobertura de sinopsis, limpieza de espacios y saltos, consistencia en la representación de los campos ausentes y cantidad final dentro del rango establecido.
14. Generar el archivo `data/libros.csv` con pandas, en codificación UTF-8.

 
---
 
## 5. Restricciones
 
Conforme a lo establecido en la consigna, la extracción se limita a los metadatos y las sinopsis de acceso público. No se descargan libros, archivos EPUB, PDF ni ningún otro contenido. Se incorpora una pausa entre las páginas visitadas para no generar una carga excesiva sobre el sitio.