import json
import random
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright

from Libro import Libro

urlBase = "https://ww3.lectulandia.co"
urlGenero = "/genero/ciencia-ficcion"
categoriaSeleccionada = "Ciencia ficción"
archivo_csv = "./data/libros.csv"
HEADLESS = False  # Cambiar a True para correr sin mostrar la ventana del navegador.
listaLibrosProcesados = []

campos = [
    "id",
    "titulo",
    "autores",
    "generos",
    "serie",
    "sinopsis",
    "url_libro",
    "categoria_origen",
    "fecha_extraccion",
    "url_portada",
]


def limpiarTexto(texto: str) -> str:
    """Colapsa espacios en blanco y saltos de línea, y recorta los extremos."""
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def libroAFila(libro: Libro) -> dict:
    return {
        "id": libro.getId(),
        "titulo": libro.getTitulo(),
        # Se guardan como string JSON de array (no como texto separado por " | ")
        # para que autores/generos sean un tipo array recorrible desde cualquier
        # lector del CSV, ej. json.loads(fila["autores"]).
        "autores": json.dumps(libro.getAutores(), ensure_ascii=False),
        "generos": json.dumps(libro.getGeneros(), ensure_ascii=False),
        "serie": libro.getSerie(),
        "sinopsis": libro.getSinopsis(),
        "url_libro": libro.getUrl(),
        "categoria_origen": libro.getCategoria(),
        "fecha_extraccion": libro.getFechaExtraccion(),
        "url_portada": libro.getUrlPortada(),
    }


def validarDataset(archivo: str) -> None:
    """Controles mínimos antes de dar por cerrada la extracción."""
    df = pd.read_csv(archivo, dtype=str, keep_default_na=False)
    total = len(df)
    duplicados = int(df["url_libro"].duplicated().sum())
    idsDuplicados = int(df["id"].duplicated().sum())
    sinId = int((df["id"].str.strip() == "").sum())
    sinTitulo = int((df["titulo"].str.strip() == "").sum())
    urlsInvalidas = int((~df["url_libro"].str.startswith("http")).sum())
    conSinopsis = int((df["sinopsis"].str.strip() != "").sum())
    porcentajeSinopsis = (conSinopsis / total * 100) if total else 0

    print("\n--- Controles mínimos ---")
    print(f"Registros totales: {total}")
    print(f"Duplicados por url_libro: {duplicados}")
    print(f"Duplicados por id: {idsDuplicados}")
    print(f"Registros sin id: {sinId}")
    print(f"Registros sin título: {sinTitulo}")
    print(f"URLs inválidas: {urlsInvalidas}")
    print(f"Registros con sinopsis: {conSinopsis} ({porcentajeSinopsis:.1f}%)")

    if not (100 <= total <= 200):
        print(f"AVISO: la cantidad de libros ({total}) está fuera del rango 100-200 pedido en la consigna.")
    if duplicados or idsDuplicados or sinId or sinTitulo or urlsInvalidas:
        print("AVISO: revisar los registros señalados arriba antes de entregar.")


def ObtenerUrlsLibros(page: Page) -> list[str]:
    listaUrlsLibros = []
    nroUltimaPagina = int(page.locator("div.page-nav").locator("a").all()[2].text_content())
    for i in range(nroUltimaPagina):
        listaArticulosLibros  = page.locator("div.books-grid").locator("article").all()
        for articuloLibro in listaArticulosLibros:
            url = articuloLibro.locator("a").first.get_attribute("href")
            listaUrlsLibros.append(url)
        page.goto(f"{urlBase}{urlGenero}/page/{i+1}")
        page.wait_for_timeout(5000)

    # Se descarta cualquier URL repetida, conservando el primer orden de aparición.
    return list(dict.fromkeys(listaUrlsLibros))

if __name__ == "__main__":
    Path(archivo_csv).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=campos).to_csv(archivo_csv, index=False, encoding="utf-8-sig")

    with sync_playwright() as p:
        cantidadLibrosScraper = 150
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(f"{urlBase}{urlGenero}")
        listaUrlsLibros = ObtenerUrlsLibros(page)
        rng = random.Random(42)
        contadorIdFallback = 0

        while (len(listaUrlsLibros) > 0) and (len(listaLibrosProcesados) < cantidadLibrosScraper):
            indice = rng.randrange(len(listaUrlsLibros))
            urlLibroParaScrapear = listaUrlsLibros.pop(indice)
            urlCompletaDelLibro = f"{urlBase}{urlLibroParaScrapear}"

            try:
                page.goto(urlCompletaDelLibro, wait_until="domcontentloaded")

                htmlLibroParaScraper = BeautifulSoup(page.content(), "html.parser")
                # Se acota la búsqueda a la ficha del libro visitado: sin este contenedor,
                # los selectores podrían devolver datos de otro libro listado en la página.
                contenedorLibro = htmlLibroParaScraper.select_one("#book") or htmlLibroParaScraper
                libro = Libro()

                # El sitio identifica cada ficha con un id propio en el atributo
                # data-book (visible en los botones de acciones). Si alguna vez
                # no estuviera presente, se usa un contador propio como respaldo.
                idElemento = contenedorLibro.select_one("[data-book]")
                if idElemento and idElemento.has_attr("data-book"):
                    libro.setId(idElemento["data-book"])
                else:
                    contadorIdFallback += 1
                    libro.setId(f"fallback-{contadorIdFallback}")

                titulo = contenedorLibro.select_one("#title h1")

                if not titulo:
                    continue

                libro.setTitulo(limpiarTexto(titulo.text))

                autores = contenedorLibro.select("#autor a.dinSource")

                for a in autores:
                    libro.agregarAutor(limpiarTexto(a.text))

                generos = contenedorLibro.select("#genero a.dinSource")

                for g in generos:
                    libro.agregarGenero(limpiarTexto(g.text))

                serie = contenedorLibro.select_one("#serie a.dinSource")

                if serie:
                    libro.setSerie(limpiarTexto(serie.text))

                # El sitio envuelve la sinopsis de forma inconsistente: a veces en
                # <span>, a veces en <p class="description">, y a veces como texto
                # plano suelto dentro del div. Se toma el contenedor completo para
                # cubrir los tres casos por igual.
                sinopsis = contenedorLibro.select_one("#sinopsis")

                if sinopsis:
                    for salto in sinopsis.find_all("br"):
                        salto.replace_with(" ")
                    libro.setSinopsis(limpiarTexto(sinopsis.get_text()))

                elem_img = contenedorLibro.select_one("#cover img, .cover img")
                if elem_img and elem_img.has_attr("src"):
                    libro.setUrlPortada(elem_img["src"])

                libro.setUrl(urlCompletaDelLibro)

                libro.setCategoria(categoriaSeleccionada)

                listaLibrosProcesados.append(libro)

                # Se guarda cada registro apenas se procesa, para no perder lo ya
                # extraído si una ficha posterior falla o se interrumpe la ejecución.
                pd.DataFrame([libroAFila(libro)], columns=campos).to_csv(
                    archivo_csv, mode="a", header=False, index=False, encoding="utf-8"
                )

                print(
                    f"[{len(listaLibrosProcesados)}/{cantidadLibrosScraper}] Extraído: {libro.getTitulo()}"
                )

                page.wait_for_timeout(5000)
            except Exception as error:
                print(f"Error al procesar '{urlCompletaDelLibro}': {error}. Se continúa con la siguiente ficha.")
                continue

        browser.close()

    print(f"\nSe guardaron {len(listaLibrosProcesados)} registros en '{archivo_csv}'.")

    if listaLibrosProcesados:
        validarDataset(archivo_csv)











