from datetime import datetime


class Libro:
    def __init__(self):

        self._titulo:str = None
        self._autor:str = None
        self._generos:list[str] = []
        self._serie:str = None
        self._sinopsis:str = None
        self._url:str = None
        self._categoria:str = None
        self._fechaExtraccion:str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._imgPortada:str = None

    def getTitulo(self) -> str:
        return self._titulo

    def setTitulo(self, valor: str):
        self._titulo = valor


    def getAutor(self) -> str:
        return self._autor

    def setAutor(self, valor: str):
        self._autor = valor

    
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

    def getImgPortada(self) -> str:
        return self._imgPortada

    def setImgPortada(self, valor: str):
        self._imgPortada = valor

    def __str__(self) -> str:
        generos = ", ".join(self._generos) if self._generos else "-"
        return (
            f"Título: {self._titulo}\n"
            f"Autor: {self._autor}\n"
            f"Serie: {self._serie}\n"
            f"Géneros: {generos}\n"
            f"Sinopsis: {self._sinopsis}\n"
            f"Categoría: {self._categoria}\n"
            f"URL: {self._url}\n"
            f"Fecha de extracción: {self._fechaExtraccion}\n"
            f"Imagen de portada: {self._imgPortada}"
        )
