from datetime import date, timedelta
from typing import Optional

class Prestamo:
    """Modelo de un préstamo: enlaza usuario y libro por sus IDs."""

    # Plazo por defecto (días) para considerar vencimiento si no se ha devuelto
    PLAZO_DIAS = 30

    def __init__(
        self,
        id_usuario: str,
        id_libro: str,
        fecha_prestamo: date,
        fecha_devolucion: Optional[date],
        nombre_usuario: str = "",
        titulo_libro: str = "",
    ) -> None:
        # id_usuario: ref a Usuario.id_usuario
        self.id_usuario = id_usuario
        # id_libro: ref a Libro.id_libro
        self.id_libro = id_libro
        # fecha_prestamo: fecha en que se realizó el préstamo
        self.fecha_prestamo = fecha_prestamo
        # fecha_devolucion: fecha REAL de devolución (si vacía -> aún no devuelto)
        self.fecha_devolucion = fecha_devolucion
        # Campos opcionales solo para mostrar en reportes si vienen en archivo de préstamos
        self.nombre_usuario = nombre_usuario
        self.titulo_libro = titulo_libro

    def esta_vencido(self, hoy: date) -> bool:
        """Determina si el préstamo está vencido con base en una política simple.
        Política adoptada:
          - Si no hay fecha_devolucion (no devuelto) y han pasado PLAZO_DIAS desde fecha_prestamo.
        """
        if self.fecha_devolucion is not None:
            # Si ya tiene fecha de devolución, no se considera "vencido"
            return False
        # Calcular fecha límite
        fecha_limite = self.fecha_prestamo + timedelta(days=self.PLAZO_DIAS)
        return hoy > fecha_limite

    def to_row(self, usuario_resuelto: str = "", libro_resuelto: str = ""):
        """Fila estándar para reportes. Intenta usar los nombres/títulos resueltos del catálogo."""
        nombre = self.nombre_usuario or usuario_resuelto or self.id_usuario
        titulo = self.titulo_libro or libro_resuelto or self.id_libro
        fp = self.fecha_prestamo.isoformat()
        fd = self.fecha_devolucion.isoformat() if self.fecha_devolucion else ""
        return [self.id_usuario, nombre, self.id_libro, titulo, fp, fd]

    def __repr__(self) -> str:
        return (
            "Prestamo("
            f"id_usuario={self.id_usuario!r}, id_libro={self.id_libro!r}, "
            f"fecha_prestamo={self.fecha_prestamo!r}, fecha_devolucion={self.fecha_devolucion!r}, "
            f"nombre_usuario={self.nombre_usuario!r}, titulo_libro={self.titulo_libro!r})"
        )
