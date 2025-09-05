from typing import List

def _plantilla_base(titulo: str, tabla_html: str) -> str:
    """Crea una página HTML mínima con una tabla y CSS embebido."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>{titulo}</title>
  <style>
    body {{ font-family: Arial, Helvetica, sans-serif; margin: 20px; }}
    h1 {{ font-size: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f0f0f0; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    .small {{ color:#666; font-size: 12px; margin-top:8px; }}
  </style>
</head>
<body>
  <h1>{titulo}</h1>
  {tabla_html}
  <div class="small">Generado por Biblioteca Digital (consola)</div>
</body>
</html>"""

def tabla(headers: List[str], filas: List[List[str]]) -> str:
    """Construye la tabla en HTML a partir de encabezados y filas (strings)."""
    # Encabezados
    thead = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>"
    # Filas
    rows_html = []
    for row in filas:
        celdas = "".join(f"<td>{(c if c is not None else '')}</td>" for c in row)
        rows_html.append(f"<tr>{celdas}</tr>")
    tbody = "<tbody>" + "".join(rows_html) + "</tbody>"
    return "<table>" + thead + tbody + "</table>"

def exportar(titulo: str, headers: List[str], filas: List[List[str]], destino: str) -> None:
    """Genera el HTML con plantilla y lo guarda en 'destino' (ruta de archivo)."""
    html_tabla = tabla(headers, filas)
    pagina = _plantilla_base(titulo, html_tabla)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina)
