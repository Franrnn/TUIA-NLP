from datetime import datetime


class Libro:
    def __init__(self):

        self._id: str = ""
        self._titulo: str = ""
        self._autores: list[str] = []
        self._generos: list[str] = []
        self._serie: str = ""
        self._sinopsis: str = ""
        self._url: str = ""
        self._categoria: str = ""
        self._fechaExtraccion: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._urlPortada: str = ""

    def getId(self) -> str:
        return self._id

    def setId(self, valor: str):
        self._id = valor

    def getTitulo(self) -> str:
        return self._titulo

    def setTitulo(self, valor: str):
        self._titulo = valor


    def getAutores(self) -> list[str]:
        return self._autores

    def agregarAutor(self, valor: str):
        self._autores.append(valor)


    def getGeneros(self) -> list[str]:
        return self._generos

    def agregarGenero(self, valor: str):
        self._generos.append(valor)

    def getSerie(self) -> str:
        return self._serie

    def setSerie(self, valor: str):
        self._serie = valor

    def getSinopsis(self) -> str:
        return self._sinopsis

    def setSinopsis(self, valor: str):
        self._sinopsis = valor

    def getUrl(self) -> str:
        return self._url

    def setUrl(self, valor: str):
        self._url = valor

    def getCategoria(self) -> str:
        return self._categoria

    def setCategoria(self, valor: str):
        self._categoria = valor

    def getFechaExtraccion(self) -> str:
        return self._fechaExtraccion

    def setFechaExtraccion(self, valor: str):
        self._fechaExtraccion = valor

    def getUrlPortada(self) -> str:
        return self._urlPortada

    def setUrlPortada(self, valor: str):
        self._urlPortada = valor

    def __str__(self) -> str:
        autores = " | ".join(self._autores) if self._autores else "-"
        generos = " | ".join(self._generos) if self._generos else "-"
        return (
            f"ID: {self._id}\n"
            f"Título: {self._titulo}\n"
            f"Autores: {autores}\n"
            f"Serie: {self._serie}\n"
            f"Géneros: {generos}\n"
            f"Sinopsis: {self._sinopsis}\n"
            f"Categoría: {self._categoria}\n"
            f"URL: {self._url}\n"
            f"Fecha de extracción: {self._fechaExtraccion}\n"
            f"URL de portada: {self._urlPortada}"
        )
