from datetime import datetime, date
from typing import Iterable, Dict, Tuple, List

def hoy() -> date:
    """Devuelve la fecha del sistema (hoy). Separado para facilitar pruebas."""
    return date.today()

def es_fecha_valida(fecha_str: str) -> bool:
    """Valida formato ISO simple YYYY-MM-DD usando datetime.strptime."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def parse_fecha(fecha_str: str):
    """Convierte YYYY-MM-DD -> date. Devuelve None si cadena vacía."""
    if not fecha_str:
        return None
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()

def contar_frecuencias(items: Iterable[str]) -> Dict[str, int]:
    """Cuenta ocurrencias de cada string en un iterable (sin usar collections.Counter)."""
    conteo: Dict[str, int] = {}
    for it in items:
        conteo[it] = conteo.get(it, 0) + 1
    return conteo

def max_por_valor(d: Dict[str, int]) -> Tuple[str, int]:
    """Devuelve (clave, valor) con el mayor valor en un diccionario (o ('',0) si vacío)."""
    max_k, max_v = "", 0
    for k, v in d.items():
        if v > max_v:
            max_k, max_v = k, v
    return max_k, max_v

def dedup_preservando_orden(seq: Iterable[str]) -> List[str]:
    """Elimina duplicados preservando el orden de primera aparición."""
    vistos = set()
    salida: List[str] = []
    for x in seq:
        if x not in vistos:
            vistos.add(x)
            salida.append(x)
    return salida
