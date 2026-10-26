"""Pruebas del listado: orden por fecha de entrega y marcas de vencida y urgente."""
from datetime import datetime, timedelta, timezone

import pytest


def en(**diferencia):
    """Fecha de entrega a `diferencia` de la hora actual, en el formato de la API."""
    fecha = datetime.now(timezone.utc) + timedelta(**diferencia)
    return fecha.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.fixture
def materia_id(crear_materia):
    return crear_materia().json()["id"]


def test_lista_vacia_devuelve_arreglo_vacio(cliente):
    assert cliente.get("/api/tareas").json() == []


def test_ordena_por_fecha_de_entrega_ascendente(cliente, crear_tarea, materia_id):
    crear_tarea(materia_id, "Lejana", en(days=10))
    crear_tarea(materia_id, "Pasada", en(days=-2))
    crear_tarea(materia_id, "Cercana", en(days=1))
    titulos = [tarea["titulo"] for tarea in cliente.get("/api/tareas").json()]
    assert titulos == ["Pasada", "Cercana", "Lejana"]


def test_misma_fecha_se_ordena_por_creacion(cliente, crear_tarea, materia_id):
    fecha = en(days=3)
    crear_tarea(materia_id, "Primera", fecha)
    crear_tarea(materia_id, "Segunda", fecha)
    crear_tarea(materia_id, "Tercera", fecha)
    titulos = [tarea["titulo"] for tarea in cliente.get("/api/tareas").json()]
    assert titulos == ["Primera", "Segunda", "Tercera"]


def test_cada_tarea_trae_su_alerta(cliente, crear_tarea, materia_id):
    crear_tarea(materia_id, "Vencida", en(hours=-1))
    crear_tarea(materia_id, "Urgente", en(hours=24))
    crear_tarea(materia_id, "Normal", en(days=5))
    alertas = {t["titulo"]: t["alerta"] for t in cliente.get("/api/tareas").json()}
    assert alertas == {"Vencida": "vencida", "Urgente": "urgente", "Normal": None}


def test_fechas_extremas(cliente, crear_tarea, materia_id):
    crear_tarea(materia_id, "Muy pasada", "2000-01-01T00:00:00Z")
    crear_tarea(materia_id, "Muy futura", "2999-12-31T23:59:00Z")
    alertas = {t["titulo"]: t["alerta"] for t in cliente.get("/api/tareas").json()}
    assert alertas == {"Muy pasada": "vencida", "Muy futura": None}


def test_la_tarea_recien_creada_tambien_trae_alerta(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, "Atrasada", en(days=-1))
    assert respuesta.json()["alerta"] == "vencida"
