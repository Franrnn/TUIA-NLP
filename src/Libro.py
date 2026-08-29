class Libro:
    def __init__(self,
                 titulo: str,
                 autor: str,
                 generos: list[str],
                 serie: str,
                 sinopsis: str,
                 url: str,
                 categoria: str,
                 fechaExtraccion: str,
                 imgPortada: str):

        self._titulo = titulo
        self._autor = autor
        self._generos = generos
        self._serie = serie
        self._sinopsis = sinopsis
        self._url = url
        self._categoria = categoria
        self._fechaExtraccion = fechaExtraccion
        self._imgPortada = imgPortada

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        self._titulo = valor

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str):
        self._autor = valor

    @property
    def generos(self) -> list[str]:
        return self._generos

    @generos.setter
    def generos(self, valor: str):
        self._generos.append(valor)

    @property
    def serie(self) -> str:
        return self._serie

    @serie.setter
    def serie(self, valor: str):
        self._serie = valor

    @property
    def sinopsis(self) -> str:
        return self._sinopsis

    @sinopsis.setter
    def sinopsis(self, valor: str):
        self._sinopsis = valor

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, valor: str):
        self._url = valor

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor

    @property
    def fechaExtraccion(self) -> str:
        return self._fechaExtraccion

    @fechaExtraccion.setter
    def fechaExtraccion(self, valor: str):
        self._fechaExtraccion = valor

    @property
    def imgPortada(self) -> str:
        return self._imgPortada

    @imgPortada.setter
    def imgPortada(self, valor: str):
        self._imgPortada = valor
