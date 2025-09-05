class Usuario:
    """Modelo simple para un usuario de la biblioteca."""

    def __init__(self, id_usuario: str, nombre: str) -> None:
        # id_usuario: identificador único (mantenerlo como str para no perder ceros a la izquierda)
        self.id_usuario = id_usuario
        # nombre: nombre completo del usuario
        self.nombre = nombre

    def to_row(self):
        # Devuelve una lista con los campos en orden para reportes tabulares (consola/HTML)
        return [self.id_usuario, self.nombre]

    def __repr__(self) -> str:
        # Representación útil para depuración
        return f"Usuario(id_usuario={self.id_usuario!r}, nombre={self.nombre!r})"
