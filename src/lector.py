from typing import List, Tuple

def leer_lineas(ruta: str) -> List[Tuple[int, str]]:
    """Lee un archivo de texto en UTF-8 y devuelve una lista de tuplas (num_linea, contenido).
    - Ignora el salto de línea, mantiene espacios internos.
    - No elimina líneas en blanco (útil para reportar exactamente lo que hay).
    """
    lineas: List[Tuple[int, str]] = []
    with open(ruta, "r", encoding="utf-8") as f:
        num = 0
        for cruda in f:
            num += 1
            lineas.append((num, cruda.rstrip("\n")))  # quitar solo salto de línea
    return lineas
