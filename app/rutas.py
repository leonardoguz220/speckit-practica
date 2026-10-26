"""Endpoints de la API bajo /api."""
import sqlite3
import unicodedata
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Request, Response

from app.db import obtener_conexion
from app.errores import ErrorApi
from app.modelos import Materia, MateriaEntrada, Tarea, TareaEntrada, TareaEstado
from app.plazos import calcular_alerta

router = APIRouter(prefix="/api")

CONSULTA_TAREAS = """
    SELECT t.id, t.titulo, t.descripcion, t.fecha_entrega, t.completada,
           m.id AS materia_id, m.nombre AS materia_nombre, m.color AS materia_color
    FROM tareas t
    JOIN materias m ON m.id = t.materia_id
"""


def obtener_db(solicitud: Request):
    """Entrega una conexión a la base de datos por solicitud y la cierra al terminar."""
    conexion = obtener_conexion(solicitud.app.state.ruta_db)
    try:
        yield conexion
    finally:
        conexion.close()


def _clave_orden(nombre):
    """Ordena sin distinguir mayúsculas ni tildes ("Álgebra" antes que "Cálculo")."""
    return unicodedata.normalize("NFD", nombre.casefold())


def _tarea_desde_fila(fila):
    completada = bool(fila["completada"])
    return {
        "id": fila["id"],
        "titulo": fila["titulo"],
        "descripcion": fila["descripcion"],
        "fecha_entrega": fila["fecha_entrega"],
        "completada": completada,
        "alerta": calcular_alerta(fila["fecha_entrega"], completada, datetime.now(timezone.utc)),
        "materia": {
            "id": fila["materia_id"],
            "nombre": fila["materia_nombre"],
            "color": fila["materia_color"],
        },
    }


@router.get("/materias", response_model=list[Materia])
def listar_materias(db=Depends(obtener_db)):
    filas = db.execute("SELECT id, nombre, color FROM materias").fetchall()
    materias = [dict(fila) for fila in filas]
    return sorted(materias, key=lambda materia: _clave_orden(materia["nombre"]))


@router.post("/materias", response_model=Materia, status_code=201)
def crear_materia(entrada: MateriaEntrada, db=Depends(obtener_db)):
    error_repetido = ErrorApi(409, "Ya existe una materia con ese nombre.", "nombre")
    # COLLATE NOCASE de SQLite solo ignora mayúsculas ASCII; casefold() cubre "Álgebra"/"álgebra".
    existentes = db.execute("SELECT nombre FROM materias").fetchall()
    if any(fila["nombre"].casefold() == entrada.nombre.casefold() for fila in existentes):
        raise error_repetido
    try:
        cursor = db.execute(
            "INSERT INTO materias (nombre, color) VALUES (?, ?)", (entrada.nombre, entrada.color)
        )
    except sqlite3.IntegrityError:
        raise error_repetido
    db.commit()
    return {"id": cursor.lastrowid, "nombre": entrada.nombre, "color": entrada.color}


@router.delete("/materias/{materia_id}", status_code=204)
def borrar_materia(materia_id: int, db=Depends(obtener_db)):
    if db.execute("SELECT 1 FROM materias WHERE id = ?", (materia_id,)).fetchone() is None:
        raise ErrorApi(404, "La materia no existe.")
    cantidad = db.execute("SELECT COUNT(*) FROM tareas WHERE materia_id = ?", (materia_id,)).fetchone()[0]
    if cantidad:
        raise ErrorApi(409, "No se puede borrar la materia porque tiene tareas asociadas.")
    db.execute("DELETE FROM materias WHERE id = ?", (materia_id,))
    db.commit()
    return Response(status_code=204)


@router.post("/tareas", response_model=Tarea, status_code=201)
def crear_tarea(entrada: TareaEntrada, db=Depends(obtener_db)):
    if db.execute("SELECT 1 FROM materias WHERE id = ?", (entrada.materia_id,)).fetchone() is None:
        raise ErrorApi(422, "La materia seleccionada no existe.", "materia_id")
    cursor = db.execute(
        "INSERT INTO tareas (materia_id, titulo, descripcion, fecha_entrega) VALUES (?, ?, ?, ?)",
        (entrada.materia_id, entrada.titulo, entrada.descripcion, entrada.fecha_entrega),
    )
    db.commit()
    fila = db.execute(CONSULTA_TAREAS + " WHERE t.id = ?", (cursor.lastrowid,)).fetchone()
    return _tarea_desde_fila(fila)


@router.get("/tareas", response_model=list[Tarea])
def listar_tareas(
    materia_id: Optional[int] = None,
    estado: Optional[Literal["pendiente", "completada"]] = None,
    db=Depends(obtener_db),
):
    condiciones, parametros = [], []
    if materia_id is not None:
        condiciones.append("t.materia_id = ?")
        parametros.append(materia_id)
    if estado is not None:
        condiciones.append("t.completada = ?")
        parametros.append(1 if estado == "completada" else 0)

    consulta = CONSULTA_TAREAS
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    filas = db.execute(consulta + " ORDER BY t.fecha_entrega, t.id", parametros).fetchall()
    return [_tarea_desde_fila(fila) for fila in filas]


@router.patch("/tareas/{tarea_id}", response_model=Tarea)
def cambiar_estado_de_tarea(tarea_id: int, entrada: TareaEstado, db=Depends(obtener_db)):
    cursor = db.execute(
        "UPDATE tareas SET completada = ? WHERE id = ?", (1 if entrada.completada else 0, tarea_id)
    )
    if cursor.rowcount == 0:
        raise ErrorApi(404, "La tarea no existe.")
    db.commit()
    fila = db.execute(CONSULTA_TAREAS + " WHERE t.id = ?", (tarea_id,)).fetchone()
    return _tarea_desde_fila(fila)
