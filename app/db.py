"""Acceso a SQLite: conexión por solicitud y creación de las tablas."""
import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS materias (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL COLLATE NOCASE UNIQUE,
    color  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tareas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id    INTEGER NOT NULL REFERENCES materias(id),
    titulo        TEXT NOT NULL,
    descripcion   TEXT,
    fecha_entrega TEXT NOT NULL,
    completada    INTEGER NOT NULL DEFAULT 0
);
"""


def obtener_conexion(ruta_db):
    """Abre una conexión con filas accesibles por nombre y claves foráneas activas."""
    # check_same_thread=False: FastAPI puede atender una solicitud en hilos distintos
    # (dependencia y ruta); cada conexión se usa solo dentro de una solicitud.
    conexion = sqlite3.connect(ruta_db, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas(conexion):
    """Crea las tablas si todavía no existen."""
    conexion.executescript(ESQUEMA)
    conexion.commit()
