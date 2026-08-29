##https://ww3.lectulandia.co/
from playwright.sync_api import Page, sync_playwright

urlBase = "https://ww3.lectulandia.co/genero/ciencia-ficcion/"

def ObternerUrlsLibros(page: Page) -> list[str]:
    listaUrlsLibros = []
    nroUltimaPagina = int(page.locator("div.page-nav").locator("a").all()[2].text_content())
    for i in range(1 , nroUltimaPagina):
        listaArticulosLibros  = page.locator("div.books-grid").locator("article").all()
        for articuloLibro in listaArticulosLibros:
            url = articuloLibro.locator("a").first.get_attribute("href")
            listaUrlsLibros.append(url)
        page.goto(f"{urlBase}/page/{i+1}")
        page.wait_for_timeout(5000)
    return listaUrlsLibros
    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(urlBase)
    listaUrlsLibros = ObternerUrlsLibros(page)
    










