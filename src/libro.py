class Libro:
    """Modelo simple para un libro del catálogo."""

    def __init__(self, id_libro: str, titulo: str) -> None:
        # id_libro: código único del libro
        self.id_libro = id_libro
        # titulo: título del libro
        self.titulo = titulo

    def to_row(self):
        # Para reportes tabulares
        return [self.id_libro, self.titulo]

    def __repr__(self) -> str:
        # Representación útil para depuración
        return f"Libro(id_libro={self.id_libro!r}, titulo={self.titulo!r})"
