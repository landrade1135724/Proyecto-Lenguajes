from typing import Dict, List, Tuple, Optional
from utils import es_fecha_valida

PERMITIDOS_EXTRAS = set("|-_'.,():;/")

def _es_char_permitido(ch: str) -> bool:
    """Regla de alfabeto permitido a nivel de carácter."""
    if ch.isalpha():
        return True  # incluye acentos y ñ
    if ch.isdigit():
        return True
    if ch.isspace():
        return True
    if ch in PERMITIDOS_EXTRAS:
        return True
    return False

def escanear_caracteres(linea: str) -> List[Tuple[int, str]]:
    """Recorre la línea y devuelve lista de (posicion, caracter) inválidos (1-indexed)."""
    errores: List[Tuple[int, str]] = []
    # Recorremos con índice 1..n para reportar posiciones al usuario
    pos = 0
    for ch in linea:
        pos += 1
        if not _es_char_permitido(ch):
            errores.append((pos, ch))
    return errores

def _split_campos(linea: str) -> List[str]:
    """Divide por '|' y elimina espacios en extremos de cada campo."""
    partes_crudas = linea.split("|")
    partes_limpias: List[str] = []
    for p in partes_crudas:
        partes_limpias.append(p.strip())
    return partes_limpias

# --------- Validadores de registros por tipo de archivo ---------

def validar_usuario(linea: str) -> Tuple[bool, Optional[Dict], List[str]]:
    """Valida formato: id_usuario|nombre_usuario"""
    errores_chars = escanear_caracteres(linea)
    if errores_chars:
        # Construir mensajes por cada carácter inválido
        mensajes = [f"pos {p}: '{c}' inválido" for (p, c) in errores_chars]
        return False, None, mensajes

    partes = _split_campos(linea)
    if len(partes) != 2:
        return False, None, [f"Se esperaban 2 campos (id|nombre), recibidos: {len(partes)}"]

    id_usuario, nombre = partes
    if not id_usuario or not nombre:
        return False, None, ["id_usuario y nombre no pueden ser vacíos"]

    return True, {"id_usuario": id_usuario, "nombre": nombre}, []

def validar_libro(linea: str) -> Tuple[bool, Optional[Dict], List[str]]:
    """Valida formato: id_libro|titulo_libro"""
    errores_chars = escanear_caracteres(linea)
    if errores_chars:
        mensajes = [f"pos {p}: '{c}' inválido" for (p, c) in errores_chars]
        return False, None, mensajes

    partes = _split_campos(linea)
    if len(partes) != 2:
        return False, None, [f"Se esperaban 2 campos (id|titulo), recibidos: {len(partes)}"]

    id_libro, titulo = partes
    if not id_libro or not titulo:
        return False, None, ["id_libro y titulo no pueden ser vacíos"]

    return True, {"id_libro": id_libro, "titulo": titulo}, []

def validar_prestamo(linea: str) -> Tuple[bool, Optional[Dict], List[str]]:
    """Valida formatos admitidos (flexible):
       Opción A (recomendada): id_usuario|id_libro|fecha_prestamo|fecha_devolucion(yyyy-mm-dd o vacío)
       Opción B (extendida):   id_usuario|nombre_usuario|id_libro|titulo_libro|fecha_prestamo|fecha_devolucion
    """
    errores_chars = escanear_caracteres(linea)
    if errores_chars:
        mensajes = [f"pos {p}: '{c}' inválido" for (p, c) in errores_chars]
        return False, None, mensajes

    partes = _split_campos(linea)
    if len(partes) not in (4, 6):
        return False, None, [f"Formato no soportado. Use 4 o 6 campos. Recibidos: {len(partes)}"]

    if len(partes) == 4:
        id_usuario, id_libro, f_p, f_d = partes
        nombre_usuario = ""
        titulo_libro = ""
    else:
        id_usuario, nombre_usuario, id_libro, titulo_libro, f_p, f_d = partes

    # Validar fechas
    if not es_fecha_valida(f_p):
        return False, None, [f"fecha_prestamo inválida: {f_p!r}"]
    if f_d and (not es_fecha_valida(f_d)):
        return False, None, [f"fecha_devolucion inválida: {f_d!r}"]

    return True, {
        "id_usuario": id_usuario,
        "nombre_usuario": nombre_usuario,
        "id_libro": id_libro,
        "titulo_libro": titulo_libro,
        "fecha_prestamo": f_p,
        "fecha_devolucion": f_d,
    }, []
