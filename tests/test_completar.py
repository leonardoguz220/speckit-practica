"""Pruebas de marcar y desmarcar tareas como completadas."""
from datetime import datetime, timedelta, timezone

import pytest


def en(**diferencia):
    fecha = datetime.now(timezone.utc) + timedelta(**diferencia)
    return fecha.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.fixture
def materia_id(crear_materia):
    return crear_materia().json()["id"]


@pytest.mark.parametrize("diferencia, alerta", [(dict(days=-1), "vencida"), (dict(hours=5), "urgente")])
def test_completar_quita_la_alerta_y_desmarcar_la_recupera(cliente, crear_tarea, materia_id, diferencia, alerta):
    tarea_id = crear_tarea(materia_id, "Taller", en(**diferencia)).json()["id"]

    completada = cliente.patch(f"/api/tareas/{tarea_id}", json={"completada": True})
    assert completada.status_code == 200
    assert completada.json()["completada"] is True
    assert completada.json()["alerta"] is None

    pendiente = cliente.patch(f"/api/tareas/{tarea_id}", json={"completada": False})
    assert pendiente.json()["completada"] is False
    assert pendiente.json()["alerta"] == alerta


def test_el_estado_persiste_en_el_listado(cliente, crear_tarea, materia_id):
    tarea_id = crear_tarea(materia_id, "Taller", en(days=5)).json()["id"]
    cliente.patch(f"/api/tareas/{tarea_id}", json={"completada": True})
    assert cliente.get("/api/tareas").json()[0]["completada"] is True


def test_tarea_inexistente_responde_404(cliente):
    respuesta = cliente.patch("/api/tareas/999", json={"completada": True})
    assert respuesta.status_code == 404
    assert respuesta.json()["errores"][0]["mensaje"] == "La tarea no existe."


@pytest.mark.parametrize("cuerpo", [{}, {"completada": "si"}, {"completada": None}, {"completada": "true"}])
def test_rechaza_completada_faltante_o_no_booleana(cliente, crear_tarea, materia_id, cuerpo):
    tarea_id = crear_tarea(materia_id).json()["id"]
    respuesta = cliente.patch(f"/api/tareas/{tarea_id}", json=cuerpo)
    assert respuesta.status_code == 422
    assert [e["campo"] for e in respuesta.json()["errores"]] == ["completada"]
