"""Reporte de notas.

Programa de consola que pide alumnos y sus notas, calcula el promedio y la
condicion (Aprobado/Desaprobado) de cada uno, y exporta la tabla a Excel.
"""

from pathlib import Path

import pandas as pd

NOTA_MINIMA: float = 0.0
NOTA_MAXIMA: float = 10.0
NOTA_APROBACION: float = 6.0
PALABRA_FIN: str = "fin"
ARCHIVO_SALIDA: str = "reporte_notas.xlsx"


def parsear_notas(texto: str) -> list[float]:
    """Convierte un texto con notas separadas por espacios en una lista.

    Acepta coma o punto como separador decimal (ej: "7,5 8 9.25").

    Args:
        texto: Texto ingresado por el usuario.

    Returns:
        Lista de notas como numeros decimales.

    Raises:
        ValueError: Si no hay notas, si alguna no es numerica o si esta
            fuera del rango permitido.
    """
    partes = texto.split()
    if not partes:
        raise ValueError("Debes ingresar al menos una nota.")

    notas: list[float] = []
    for parte in partes:
        try:
            nota = float(parte.replace(",", "."))
        except ValueError:
            raise ValueError(f"'{parte}' no es una nota numerica.") from None
        if not NOTA_MINIMA <= nota <= NOTA_MAXIMA:
            raise ValueError(
                f"La nota {parte} debe estar entre "
                f"{NOTA_MINIMA:g} y {NOTA_MAXIMA:g}."
            )
        notas.append(nota)
    return notas


def pedir_notas(nombre: str) -> list[float]:
    """Pide las notas de un alumno hasta que el ingreso sea valido.

    Args:
        nombre: Nombre del alumno, para mostrarlo en el mensaje.

    Returns:
        Lista de notas validas del alumno.
    """
    while True:
        texto = input(f"  Notas de {nombre} (separadas por espacio): ")
        try:
            return parsear_notas(texto)
        except ValueError as error:
            print(f"  [Error] {error}")


def pedir_alumnos() -> list[dict[str, object]]:
    """Pide por consola alumnos y notas hasta que se escriba "fin".

    Returns:
        Lista de diccionarios con las claves "nombre" y "notas".
    """
    alumnos: list[dict[str, object]] = []
    print(f"Ingresa los alumnos. Escribe '{PALABRA_FIN}' para terminar.\n")
    while True:
        nombre = input("Nombre del alumno: ").strip()
        if nombre.lower() == PALABRA_FIN:
            break
        if not nombre:
            print("  [Error] El nombre no puede estar vacio.")
            continue
        alumnos.append({"nombre": nombre, "notas": pedir_notas(nombre)})
    return alumnos


def calcular_condicion(promedio: float) -> str:
    """Determina si un alumno aprueba segun su promedio.

    Args:
        promedio: Promedio del alumno.

    Returns:
        "Aprobado" si alcanza la nota de aprobacion; si no, "Desaprobado".
    """
    return "Aprobado" if promedio >= NOTA_APROBACION else "Desaprobado"


def construir_tabla(alumnos: list[dict[str, object]]) -> pd.DataFrame:
    """Arma el DataFrame con notas, promedio y condicion de cada alumno.

    Args:
        alumnos: Lista de diccionarios con "nombre" y "notas".

    Returns:
        DataFrame con las columnas Alumno, Notas, Cantidad de notas,
        Promedio y Condicion.

    Raises:
        ValueError: Si la lista de alumnos esta vacia.
    """
    if not alumnos:
        raise ValueError("No se cargo ningun alumno.")

    filas: list[dict[str, object]] = []
    for alumno in alumnos:
        notas: list[float] = alumno["notas"]  # type: ignore[assignment]
        promedio = round(sum(notas) / len(notas), 2)
        filas.append(
            {
                "Alumno": alumno["nombre"],
                "Notas": ", ".join(f"{nota:g}" for nota in notas),
                "Cantidad de notas": len(notas),
                "Promedio": promedio,
                "Condicion": calcular_condicion(promedio),
            }
        )
    return pd.DataFrame(filas)


def exportar_excel(tabla: pd.DataFrame, ruta: Path) -> bool:
    """Guarda la tabla en un archivo Excel (.xlsx).

    Args:
        tabla: DataFrame a exportar.
        ruta: Ruta del archivo de destino.

    Returns:
        True si se guardo correctamente, False si hubo un error.
    """
    try:
        tabla.to_excel(ruta, index=False, sheet_name="Notas")
    except PermissionError:
        print(f"[Error] Sin permiso para escribir '{ruta}'. "
              "Si esta abierto en Excel, cerralo e intenta de nuevo.")
    except ModuleNotFoundError as error:
        print(f"[Error] Falta una libreria: {error}. "
              "Ejecuta: pip install -r requirements.txt")
    except OSError as error:
        print(f"[Error] No se pudo guardar el archivo: {error}")
    except ValueError as error:
        print(f"[Error] Datos invalidos al exportar: {error}")
    else:
        return True
    return False


def mostrar_resumen(tabla: pd.DataFrame, ruta: Path) -> None:
    """Imprime por consola la tabla y un resumen de lo generado.

    Args:
        tabla: DataFrame con los datos procesados.
        ruta: Ruta del archivo Excel generado.
    """
    aprobados = int((tabla["Condicion"] == "Aprobado").sum())
    mejor = tabla.loc[tabla["Promedio"].idxmax()]

    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    print(tabla.to_string(index=False))
    print("-" * 50)
    print(f"Alumnos cargados : {len(tabla)}")
    print(f"Aprobados        : {aprobados}")
    print(f"Desaprobados     : {len(tabla) - aprobados}")
    print(f"Promedio general : {tabla['Promedio'].mean():.2f}")
    print(f"Mejor promedio   : {mejor['Alumno']} ({mejor['Promedio']})")
    print(f"Archivo generado : {ruta.resolve()}")


def main() -> None:
    """Ejecuta el flujo completo del programa."""
    try:
        alumnos = pedir_alumnos()
        tabla = construir_tabla(alumnos)
    except ValueError as error:
        print(f"[Error] {error}")
        return
    except (KeyboardInterrupt, EOFError):
        print("\nIngreso cancelado por el usuario.")
        return

    ruta = Path(ARCHIVO_SALIDA)
    if exportar_excel(tabla, ruta):
        mostrar_resumen(tabla, ruta)
    else:
        print("No se genero el archivo Excel.")


if __name__ == "__main__":
    main()
