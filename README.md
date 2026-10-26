# Reporte de notas

Programa de consola en Python que:

1. Pide nombres de alumnos y sus notas (un alumno por vez, hasta escribir `fin`).
2. Organiza los datos en una tabla (DataFrame de **pandas**).
3. Calcula el promedio de cada alumno y su condición (Aprobado/Desaprobado).
4. Exporta la tabla a `reporte_notas.xlsx` (usando **openpyxl**).
5. Muestra por consola un resumen de lo generado.

**Criterios:** las notas van de 0 a 10 y se aprueba con promedio >= 6
(se pueden cambiar en las constantes al inicio de `reporte_notas.py`).

## Requisitos

- Python 3.9 o superior

## Crear el entorno virtual

```bash
python -m venv .venv
```

Activarlo:

- Linux / Mac: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

> **Windows / PowerShell:** si aparece el error "running scripts is
> disabled on this system", ejecutar una sola vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
> o bien usar el Símbolo del sistema (cmd) con `.venv\Scripts\activate.bat`.

## Instalar las dependencias

```bash
pip install -r requirements.txt
```

(Si empezás desde cero: `pip install pandas openpyxl` y luego
`pip freeze > requirements.txt`.)

## Ejecutar

```bash
python reporte_notas.py
```

Ejemplo de uso:

```
Nombre del alumno: Ana
  Notas de Ana (separadas por espacio): 7 8,5 9
Nombre del alumno: Luis
  Notas de Luis (separadas por espacio): 4 5 3
Nombre del alumno: fin
```

Al terminar se crea `reporte_notas.xlsx` en la carpeta actual.

## Manejo de errores

- Nota no numérica o fuera de rango: se avisa y se vuelve a pedir.
- Nombre vacío: se avisa y se vuelve a pedir.
- Lista vacía (se escribe `fin` sin cargar alumnos): se informa y termina.
- Error al guardar (archivo abierto en Excel, sin permisos, etc.): se informa.
- Ctrl+C / fin de entrada: el programa se cierra de forma ordenada.

## Estructura

```
reporte_notas/
├── .gitignore
├── reporte_notas.py
├── requirements.txt
└── README.md
```
