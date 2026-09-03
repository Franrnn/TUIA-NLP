import random

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright

from Libro import Libro

urlBase = "https://ww3.lectulandia.co"
urlGenero = "/genero/ciencia-ficcion"
categoriaSeleccionada = "Ciencia ficción"
archivo_csv = "./data/libros.csv"
listaLibrosProcesados = []

def ObtenerUrlsLibros(page: Page) -> list[str]:
    listaUrlsLibros = []
    # nroUltimaPagina = int(page.locator("div.page-nav").locator("a").all()[2].text_content())
    nroUltimaPagina = 1
    for i in range(nroUltimaPagina):
        listaArticulosLibros  = page.locator("div.books-grid").locator("article").all()
        for articuloLibro in listaArticulosLibros:
            url = articuloLibro.locator("a").first.get_attribute("href")
            listaUrlsLibros.append(url)
        page.goto(f"{urlBase}{urlGenero}/page/{i+1}")
        page.wait_for_timeout(5000)

    return listaUrlsLibros
    
with sync_playwright() as p:
    cantidadLibrosScraper = 50
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(f"{urlBase}{urlGenero}")
    listaUrlsLibros = ObtenerUrlsLibros(page)
    rng = random.Random(42)

    while (len(listaUrlsLibros) > 0) and (len(listaLibrosProcesados) < cantidadLibrosScraper):
        indice = rng.randrange(len(listaUrlsLibros))
        urlLibroParaScrapear = listaUrlsLibros.pop(indice)
        urlCompletaDelLibro = f"{urlBase}{urlLibroParaScrapear}"
        page.goto(urlCompletaDelLibro, wait_until="domcontentloaded")

        htmlLibroParaScraper = BeautifulSoup(page.content(), "html.parser")
        libro = Libro()

        titulo = htmlLibroParaScraper.select_one("#title > h1")
        
        if not titulo:
            continue

        libro.setTitulo(titulo.text)     

        autor = htmlLibroParaScraper.select_one("#autor > a")
        
        if autor:
            libro.setAutor(autor.text)

        generos = htmlLibroParaScraper.select('#genero > a')
        
        for g in generos:
            libro.agregarGenero(g.text)
            
        serie = htmlLibroParaScraper.select_one("#serie > a")
        
        if serie:
            libro.setSerie(serie.text)
        
        sinopsis = htmlLibroParaScraper.select_one('#sinopsis > span')
        
        if sinopsis:
            libro.setSinopsis(sinopsis.text)

        elem_img = htmlLibroParaScraper.select_one("#cover img, .cover img")
        if elem_img and elem_img.has_attr("src"):
            libro.setImgPortada(elem_img["src"])

        libro.setUrl(urlCompletaDelLibro)

        libro.setCategoria(categoriaSeleccionada)

        listaLibrosProcesados.append(libro)
        
        print(
            f"[{len(listaLibrosProcesados)}/{cantidadLibrosScraper}] Extraído: {libro.getTitulo()}"
        )
        
        page.wait_for_timeout(5000)

    browser.close()

campos = [
    "titulo",
    "autor",
    "generos",
    "serie",
    "sinopsis",
    "url_libro",
    "categoria_origen",
    "fecha_extraccion",
    "img_portada",
]

filas = [
    {
        "titulo": lib.getTitulo(),
        "autor": lib.getAutor(),
        "generos": ", ".join(lib.getGeneros()) if lib.getGeneros() else "",
        "serie": lib.getSerie() or "",
        "sinopsis": lib.getSinopsis(),
        "url_libro": lib.getUrl(),
        "categoria_origen": lib.getCategoria(),
        "fecha_extraccion": lib.getFechaExtraccion(),
        "img_portada": lib.getImgPortada(),
    }
    for lib in listaLibrosProcesados
]

df = pd.DataFrame(filas, columns=campos)

df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

print(f"\nSe guardaron {len(listaLibrosProcesados)} registros en '{archivo_csv}'.")


    










