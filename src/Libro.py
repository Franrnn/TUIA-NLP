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
        
        self.titulo = titulo
        self.autor = autor
        self.generos = generos
        self.serie = serie
        self.sinopsis = sinopsis
        self.url = url
        self.categoria = categoria
        self.fechaExtraccion = fechaExtraccion,
        self.imgPortada = imgPortada