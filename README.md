# Proyecto 1 - Biblioteca Digital

Simulador en consola para la gestión de préstamos de libros en una biblioteca digital.

## 📌 Autores
- Luis Antonio Andrade García - 1135724
- Juan Pablo Mazariegos Sepulveda - 1140024

## 🧾 Descripción General
Este sistema permite cargar catálogos de usuarios y libros, así como un archivo de préstamos. Procesa la información validando formato y caracteres permitidos, generando reportes en consola y exportando a HTML.

## 🖥️ Requisitos
- Python 3.8 o superior
- No requiere librerías externas

## ▶️ Ejecución del programa

Ubica el terminal en la carpeta `src` y ejecuta:

```bash
python main.py
```

## 📂 Estructura esperada de archivos

```
Proyecto1/
├── data/
│   ├── usuarios.lfa
│   ├── libros.lfa
│   ├── prestamos.lfa
│   └── errores.lfa
├── output/
│   └── [archivos HTML generados]
├── src/
│   └── [código fuente]
├── docs/
│   ├── Manual_Usuario.pdf
│   └── Manual_Tecnico.pdf
└── README.md
```

## 📥 Entrada esperada

**usuarios.lfa**
```
U001|Ana López
U002|Carlos Ruiz
```

**libros.lfa**
```
L001|Autómatas y Lenguajes Formales
```

**prestamos.lfa**
```
U001|L001|2025-08-01|2025-08-10
```

## 📤 Salidas

- Reportes en consola
- Reportes exportados en HTML en la carpeta `output/`.

## ⚠️ Validaciones

- Caracteres no válidos
- Cantidad de campos por línea
- Formato de fechas
- Existencia de IDs en catálogos

## 📝 Licencia
Proyecto académico - Universidad Rafael Landívar, 2025.
