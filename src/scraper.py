from Libro import Libro
import random
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright
from datetime import datetime

urlBase = "https://ww3.lectulandia.co"
urlGenero = "/genero/ciencia-ficcion"
categoriaSeleccionada = "Ciencia ficción"

def ObtenerUrlsLibros(page: Page) -> list[str]:
    listaUrlsLibros = []
    nroUltimaPagina = 15
    # nroUltimaPagina = int(page.locator("div.page-nav").locator("a").all()[2].text_content())
    for i in range(1 , nroUltimaPagina):
        listaArticulosLibros  = page.locator("div.books-grid").locator("article").all()
        for articuloLibro in listaArticulosLibros:
            url = articuloLibro.locator("a").first.get_attribute("href")
            listaUrlsLibros.append(url)
        page.goto(f"{urlBase}{urlGenero}/page/{i+1}")
        page.wait_for_timeout(5000)

    return listaUrlsLibros
    
with sync_playwright() as p:
    cantidadLibrosScraper = 150
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(f"{urlBase}{urlGenero}")
    listaUrlsLibros = ObtenerUrlsLibros(page)
    rng = random.Random(42)
    libros_procesados = []

    for x in range(0, cantidadLibrosScraper):
        indice = rng.randrange(len(listaUrlsLibros))
        urlLibroParaScrapear = listaUrlsLibros.pop(indice)
        urlCompletaDelLibro = f"{urlBase}{urlLibroParaScrapear}"
        page.goto(urlCompletaDelLibro, wait_until="domcontentloaded")
        
        try:
            page.wait_for_selector("#title, h1", timeout=10000)
        except Exception:
            print(f"No cargó a tiempo la página: {urlCompletaDelLibro}")
            continue

        htmlLibroParaScraper = BeautifulSoup(page.content(), "html.parser")
        libro = Libro()

        titulo = htmlLibroParaScraper.select_one("#title > h1").text
        if titulo == None:
            print(f"Saltando libro (título no encontrado): {urlCompletaDelLibro}")
            continue
        else:
            libro.setTitulo(titulo)     
            

        autor = htmlLibroParaScraper.select_one("#autor > a").text
        libro.setAutor(autor)

        generos = htmlLibroParaScraper.select('#genero > a')
        for g in generos:
            libro.agregarGenero(g.text)
        serie = htmlLibroParaScraper.select_one("#serie > a")
        if serie:
            libro.setSerie(serie.text)
        sinopsis = htmlLibroParaScraper.select_one('#sinopsis > span').text
        libro.setSinopsis(sinopsis)

        elem_img = htmlLibroParaScraper.select_one("#cover img, .cover img")
        if elem_img and elem_img.has_attr("src"):
            libro.setImgPortada(elem_img["src"])

        canonical_link = htmlLibroParaScraper.select_one(
            "link[rel='canonical']"
        )
        if canonical_link and canonical_link.get("href"):
            libro.setUrl(canonical_link["href"])
        else:
            libro.setUrl(page.url)

        libro.setCategoria(categoriaSeleccionada)
        libro.setFechaExtraccion(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        print(libro)

        libros_procesados.append(libro)
        print(
            f"[{len(libros_procesados)}/{cantidadLibrosScraper}] Extraído: {libro.getTitulo()}"
        )

    browser.close()
        #url
        #categoria
        #fechaExtraccion
        #imgPortada


archivo_csv = "libros.csv"
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

with open(archivo_csv, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(campos)
    for lib in libros_procesados:
        writer.writerow(
            [
                lib.getTitulo(),
                lib.getAutor(),
                ", ".join(lib._generos) if lib._generos else "",
                lib.getSerie() if lib.getSerie() else "",
                lib.getSinopsis(),
                lib.getUrl(),
                lib.getCategoria(),
                lib.getFechaExtraccion(),
                lib.getImgPortada(),
            ]
        )
print(
    f"\nSe guardaron {len(libros_procesados)} registros en '{archivo_csv}'."
)


    










