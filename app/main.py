"""Punto de entrada: crea la aplicación FastAPI y sirve la interfaz estática.

Ejecutar con: uvicorn app.main:crear_app --factory
"""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import crear_tablas, obtener_conexion
from app.errores import registrar_manejadores
from app.rutas import router

CARPETA_ESTATICA = Path(__file__).parent / "static"
RUTA_DB_POR_DEFECTO = "datos/tareas.db"


def crear_app(ruta_db=None):
    """Crea la aplicación; cada llamada con otra ruta usa su propia base de datos."""
    ruta = Path(ruta_db or os.environ.get("TAREAS_DB", RUTA_DB_POR_DEFECTO))
    ruta.parent.mkdir(parents=True, exist_ok=True)

    conexion = obtener_conexion(ruta)
    crear_tablas(conexion)
    conexion.close()

    app = FastAPI(title="Organizador de tareas académicas")
    app.state.ruta_db = ruta
    registrar_manejadores(app)
    app.include_router(router)
    # Debe montarse al final para que "/" no oculte las rutas /api.
    app.mount("/", StaticFiles(directory=CARPETA_ESTATICA, html=True), name="interfaz")
    return app
