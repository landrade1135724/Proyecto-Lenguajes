from typing import Dict, List, Optional
from os import path
from utils import hoy, parse_fecha, contar_frecuencias, max_por_valor, dedup_preservando_orden
from lector import leer_lineas
from validador import validar_usuario, validar_libro, validar_prestamo
from usuario import Usuario
from libro import Libro
from prestamo import Prestamo
from html_exporter import exportar

# Rutas relativas esperadas (asumiendo estructura propuesta de carpetas)
DATA_DIR = path.join(path.dirname(__file__), "..", "data")
OUT_DIR  = path.join(path.dirname(__file__), "..", "output")

class Almacen:
    """Contiene la información cargada en memoria."""
    def __init__(self) -> None:
        self.usuarios: Dict[str, Usuario] = {}   # id -> Usuario
        self.libros: Dict[str, Libro] = {}       # id -> Libro
        self.prestamos: List[Prestamo] = []      # lista de préstamos
        self.errores: List[str] = []             # acumulador de mensajes de error

    # ---------- Carga de archivos ----------
    def cargar_usuarios(self, ruta: str) -> None:
        lineas = leer_lineas(ruta)
        for num, linea in lineas:
            # Ignorar comentarios y líneas vacías
            if not linea or linea.strip().startswith("#"):
                continue
            ok, data, errores = validar_usuario(linea)
            if not ok:
                # Por requerimiento: reportar línea, posición y carácter erróneo.
                # Aquí 'errores' ya trae descripciones de posición si aplica.
                for msg in errores:
                    self.errores.append(f"[usuarios] Línea {num}: {msg}")
                # Pasar a la siguiente línea
                continue
            # Crear/actualizar el usuario
            u = Usuario(data["id_usuario"], data["nombre"])
            self.usuarios[u.id_usuario] = u

    def cargar_libros(self, ruta: str) -> None:
        lineas = leer_lineas(ruta)
        for num, linea in lineas:
            if not linea or linea.strip().startswith("#"):
                continue
            ok, data, errores = validar_libro(linea)
            if not ok:
                for msg in errores:
                    self.errores.append(f"[libros] Línea {num}: {msg}")
                continue
            l = Libro(data["id_libro"], data["titulo"])
            self.libros[l.id_libro] = l

    def cargar_prestamos(self, ruta: str) -> None:
        lineas = leer_lineas(ruta)
        for num, linea in lineas:
            if not linea or linea.strip().startswith("#"):
                continue
            ok, data, errores = validar_prestamo(linea)
            if not ok:
                for msg in errores:
                    self.errores.append(f"[prestamos] Línea {num}: {msg}")
                continue

            # Validar que IDs existan en catálogos si están cargados
            id_u = data["id_usuario"]
            id_l = data["id_libro"]
            if id_u not in self.usuarios:
                self.errores.append(f"[prestamos] Línea {num}: id_usuario {id_u!r} no existe en catálogo de usuarios")
            if id_l not in self.libros:
                self.errores.append(f"[prestamos] Línea {num}: id_libro {id_l!r} no existe en catálogo de libros")

            # Crear objeto préstamo (parsear fechas)
            fp = parse_fecha(data["fecha_prestamo"])
            fd = parse_fecha(data["fecha_devolucion"])
            p = Prestamo(
                id_usuario=id_u,
                id_libro=id_l,
                fecha_prestamo=fp,
                fecha_devolucion=fd,
                nombre_usuario=data.get("nombre_usuario",""),
                titulo_libro=data.get("titulo_libro",""),
            )
            self.prestamos.append(p)

    # ---------- Reportes en consola ----------
    def mostrar_historial(self) -> None:
        # Encabezado
        print("HISTORIAL DE PRÉSTAMOS")
        print("-" * 80)
        # Columnas
        print(f"{'ID_Usuario':<12} {'Usuario':<20} {'ID_Libro':<12} {'Libro':<20} {'F.Prestamo':<12} {'F.Devolucion':<12}")
        # Filas
        for p in self.prestamos:
            usuario = self.usuarios.get(p.id_usuario)
            libro = self.libros.get(p.id_libro)
            fila = p.to_row(
                usuario_resuelto=(usuario.nombre if usuario else ""),
                libro_resuelto=(libro.titulo if libro else ""),
            )
            # Imprimir con anchos fijos (truncar si excede)
            u_id, u_nom, l_id, l_tit, f_p, f_d = fila
            print(f"{u_id:<12} {u_nom[:20]:<20} {l_id:<12} {l_tit[:20]:<20} {f_p:<12} {f_d:<12}")
        print()

    def mostrar_usuarios_unicos(self) -> None:
        print("USUARIOS ÚNICOS (catálogo)")
        print("-" * 40)
        print(f"{'ID_Usuario':<12} {'Nombre':<25}")
        for u in self.usuarios.values():
            print(f"{u.id_usuario:<12} {u.nombre[:25]:<25}")
        print()

    def mostrar_libros_prestados(self) -> None:
        print("LIBROS PRESTADOS (sin duplicados en historial)")
        print("-" * 60)
        print(f"{'ID_Libro':<12} {'Titulo':<40}")
        # Determinar libros que aparecen en la lista de préstamos
        vistos = set()
        for p in self.prestamos:
            if p.id_libro not in vistos:
                vistos.add(p.id_libro)
                libro = self.libros.get(p.id_libro)
                titulo = libro.titulo if libro else (p.titulo_libro or "")
                print(f"{p.id_libro:<12} {titulo[:40]:<40}")
        print()

    def mostrar_estadisticas(self) -> None:
        print("ESTADÍSTICAS DE PRÉSTAMOS")
        print("-" * 40)
        total = len(self.prestamos)
        # Libro más prestado
        frec_libros = contar_frecuencias([p.id_libro for p in self.prestamos])
        mas_libro_id, mas_libro_freq = max_por_valor(frec_libros)
        mas_libro_titulo = self.libros[mas_libro_id].titulo if mas_libro_id in self.libros else ""
        # Usuario más activo
        frec_usuarios = contar_frecuencias([p.id_usuario for p in self.prestamos])
        mas_usr_id, mas_usr_freq = max_por_valor(frec_usuarios)
        mas_usr_nombre = self.usuarios[mas_usr_id].nombre if mas_usr_id in self.usuarios else ""
        # Usuarios únicos (que han prestado)
        unicos = set([p.id_usuario for p in self.prestamos])

        print(f"Total de préstamos: {total}")
        print(f"Libro más prestado: {mas_libro_id} - {mas_libro_titulo} (veces: {mas_libro_freq})")
        print(f"Usuario más activo: {mas_usr_id} - {mas_usr_nombre} (veces: {mas_usr_freq})")
        print(f"Total de usuarios únicos (en préstamos): {len(unicos)}")
        print()

    def mostrar_prestamos_vencidos(self) -> None:
        print("PRÉSTAMOS VENCIDOS")
        print("-" * 40)
        print(f"{'ID_Usuario':<12} {'Usuario':<20} {'ID_Libro':<12} {'Libro':<20} {'F.Prestamo':<12}")
        h = hoy()
        for p in self.prestamos:
            if p.esta_vencido(h):
                usuario = self.usuarios.get(p.id_usuario)
                libro = self.libros.get(p.id_libro)
                u_nom = usuario.nombre if usuario else (p.nombre_usuario or "")
                l_nom = libro.titulo if libro else (p.titulo_libro or "")
                print(f"{p.id_usuario:<12} {u_nom[:20]:<20} {p.id_libro:<12} {l_nom[:20]:<20} {p.fecha_prestamo.isoformat():<12}")
        print()

    # ---------- Exportar reportes a HTML ----------
    def exportar_reportes_html(self) -> None:
        # Historial
        headers_h = ["ID Usuario", "Usuario", "ID Libro", "Libro", "Fecha Préstamo", "Fecha Devolución"]
        filas_h: List[List[str]] = []
        for p in self.prestamos:
            usuario = self.usuarios.get(p.id_usuario)
            libro = self.libros.get(p.id_libro)
            filas_h.append(p.to_row(
                usuario_resuelto=(usuario.nombre if usuario else ""),
                libro_resuelto=(libro.titulo if libro else ""),
            ))
        exportar("Historial de Préstamos", headers_h, filas_h, path.join(OUT_DIR, "historial_prestamos.html"))

        # Usuarios únicos (catálogo)
        headers_u = ["ID Usuario", "Nombre"]
        filas_u = [u.to_row() for u in self.usuarios.values()]
        exportar("Listado de Usuarios", headers_u, filas_u, path.join(OUT_DIR, "usuarios.html"))

        # Libros prestados (únicos)
        headers_l = ["ID Libro", "Título"]
        filas_l: List[List[str]] = []
        vistos = set()
        for p in self.prestamos:
            if p.id_libro not in vistos:
                vistos.add(p.id_libro)
                libro = self.libros.get(p.id_libro)
                titulo = libro.titulo if libro else (p.titulo_libro or "")
                filas_l.append([p.id_libro, titulo])
        exportar("Listado de Libros Prestados", headers_l, filas_l, path.join(OUT_DIR, "libros.html"))

        # Estadísticas
        total = len(self.prestamos)
        frec_libros = contar_frecuencias([p.id_libro for p in self.prestamos])
        mas_libro_id, mas_libro_freq = max_por_valor(frec_libros)
        mas_libro_titulo = self.libros[mas_libro_id].titulo if mas_libro_id in self.libros else ""
        frec_usuarios = contar_frecuencias([p.id_usuario for p in self.prestamos])
        mas_usr_id, mas_usr_freq = max_por_valor(frec_usuarios)
        mas_usr_nombre = self.usuarios[mas_usr_id].nombre if mas_usr_id in self.usuarios else ""
        unicos = set([p.id_usuario for p in self.prestamos])
        headers_e = ["Métrica", "Valor"]
        filas_e = [
            ["Total de préstamos", str(total)],
            ["Libro más prestado", f"{mas_libro_id} - {mas_libro_titulo} (veces: {mas_libro_freq})"],
            ["Usuario más activo", f"{mas_usr_id} - {mas_usr_nombre} (veces: {mas_usr_freq})"],
            ["Total de usuarios únicos", str(len(unicos))],
        ]
        exportar("Estadísticas de Préstamos", headers_e, filas_e, path.join(OUT_DIR, "estadisticas.html"))

        # Vencidos
        headers_v = ["ID Usuario", "Usuario", "ID Libro", "Libro", "Fecha Préstamo"]
        filas_v: List[List[str]] = []
        h = hoy()
        for p in self.prestamos:
            if p.esta_vencido(h):
                usuario = self.usuarios.get(p.id_usuario)
                libro = self.libros.get(p.id_libro)
                filas_v.append([
                    p.id_usuario,
                    (usuario.nombre if usuario else (p.nombre_usuario or "")),
                    p.id_libro,
                    (libro.titulo if libro else (p.titulo_libro or "")),
                    p.fecha_prestamo.isoformat(),
                ])
        exportar("Préstamos Vencidos", headers_v, filas_v, path.join(OUT_DIR, "vencidos.html"))

        print(f"Reportes HTML generados en: {OUT_DIR}")

    # ---------- Utilidad ----------
    def mostrar_errores(self) -> None:
        if not self.errores:
            print("Sin errores reportados.")
            return
        print("ERRORES DETECTADOS")
        print("-" * 60)
        for e in self.errores:
            print(e)
        print()

# ---------------- Menú de consola ----------------
def pedir_ruta(defecto: str) -> str:
    """Pide una ruta al usuario. Si se deja vacío, usa el valor por defecto."""
    ruta = input(f"Ingrese ruta del archivo [Enter = {defecto}]: ").strip()
    return ruta or defecto

def asegurar_directorios() -> None:
    """Crea carpeta de salida si no existe."""
    # Usamos os.path para no depender de pathlib aquí
    import os
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR, exist_ok=True)

def main():
    print("=== SISTEMA DE BIBLIOTECA DIGITAL (Consola) ===")
    print("Nota: Formatos por defecto separados por '|'")
    print("Usuarios: id_usuario|nombre   Libros: id_libro|titulo")
    print("Préstamos: id_usuario|id_libro|YYYY-MM-DD|YYYY-MM-DD (vacío si no devuelto)")
    print()

    asegurar_directorios()
    store = Almacen()

    while True:
        print("MENÚ PRINCIPAL")
        print("1) Cargar usuarios")
        print("2) Cargar libros")
        print("3) Cargar préstamos")
        print("4) Mostrar historial de préstamos")
        print("5) Mostrar listado de usuarios únicos")
        print("6) Mostrar listado de libros prestados")
        print("7) Mostrar estadísticas de préstamos")
        print("8) Mostrar préstamos vencidos")
        print("9) Exportar todos los reportes a HTML")
        print("E) Mostrar errores de carga/validación")
        print("0) Salir")
        op = input("Seleccione una opción: ").strip().lower()
        print()

        if op == "1":
            ruta = pedir_ruta(path.join(DATA_DIR, "usuarios.lfa"))
            try:
                store.cargar_usuarios(ruta)
                print("Usuarios cargados.\n")
            except Exception as ex:
                print(f"Error cargando usuarios: {ex}\n")
        elif op == "2":
            ruta = pedir_ruta(path.join(DATA_DIR, "libros.lfa"))
            try:
                store.cargar_libros(ruta)
                print("Libros cargados.\n")
            except Exception as ex:
                print(f"Error cargando libros: {ex}\n")
        elif op == "3":
            ruta = pedir_ruta(path.join(DATA_DIR, "prestamos.lfa"))
            try:
                store.cargar_prestamos(ruta)
                print("Préstamos cargados.\n")
            except Exception as ex:
                print(f"Error cargando préstamos: {ex}\n")
        elif op == "4":
            store.mostrar_historial()
        elif op == "5":
            store.mostrar_usuarios_unicos()
        elif op == "6":
            store.mostrar_libros_prestados()
        elif op == "7":
            store.mostrar_estadisticas()
        elif op == "8":
            store.mostrar_prestamos_vencidos()
        elif op == "9":
            try:
                store.exportar_reportes_html()
            except Exception as ex:
                print(f"Error exportando reportes: {ex}\n")
        elif op == "e":
            store.mostrar_errores()
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.\n")

if __name__ == "__main__":
    main()
