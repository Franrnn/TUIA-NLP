from Libro import Libro
import random
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright

urlBase = "https://ww3.lectulandia.co"
urlGenero = "/genero/ciencia-ficcion"

def ObtenerUrlsLibros(page: Page) -> list[str]:
    listaUrlsLibros = []
    nroUltimaPagina = 2
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
    cantidadLibrosScraper = 5
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(f"{urlBase}{urlGenero}")
    listaUrlsLibros = ObtenerUrlsLibros(page)
    rng = random.Random(42)
    for x in range(1, cantidadLibrosScraper):
        indice = rng.randrange(len(listaUrlsLibros))
        urlLibroParaScrapear = listaUrlsLibros.pop(indice)
        urlCompletaDelLibro = f"{urlBase}{urlLibroParaScrapear}"
        page.goto(urlCompletaDelLibro)
        htmlLibroParaScraper = BeautifulSoup(page.content(), "html.parser")






    










