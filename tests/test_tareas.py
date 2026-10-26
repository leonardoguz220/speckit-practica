"""Pruebas de creación de tareas y de la validación de sus datos."""
import pytest


@pytest.fixture
def materia_id(crear_materia):
    return crear_materia("Cálculo", "azul").json()["id"]


def errores(respuesta):
    return respuesta.json()["errores"]


def test_crear_tarea_valida_incluye_la_materia(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, "Taller 3", "2030-01-01T12:00:00Z", descripcion="Capítulos 4 y 5")
    assert respuesta.status_code == 201
    tarea = respuesta.json()
    assert tarea["titulo"] == "Taller 3"
    assert tarea["descripcion"] == "Capítulos 4 y 5"
    assert tarea["fecha_entrega"] == "2030-01-01T12:00:00Z"
    assert tarea["completada"] is False
    assert tarea["materia"] == {"id": materia_id, "nombre": "Cálculo", "color": "azul"}


def test_la_descripcion_es_opcional(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id)
    assert respuesta.status_code == 201
    assert respuesta.json()["descripcion"] is None


@pytest.mark.parametrize("titulo", ["", "   ", "a" * 101])
def test_rechaza_titulo_vacio_solo_espacios_o_de_101_caracteres(crear_tarea, materia_id, titulo):
    respuesta = crear_tarea(materia_id, titulo)
    assert respuesta.status_code == 422
    assert [e["campo"] for e in errores(respuesta)] == ["titulo"]


def test_acepta_titulo_de_exactamente_100_caracteres(crear_tarea, materia_id):
    assert crear_tarea(materia_id, "a" * 100).status_code == 201


def test_recorta_espacios_del_titulo_antes_de_medir_la_longitud(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, "  " + "a" * 100 + "  ")
    assert respuesta.status_code == 201
    assert respuesta.json()["titulo"] == "a" * 100


def test_rechaza_descripcion_de_501_caracteres(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, descripcion="a" * 501)
    assert respuesta.status_code == 422
    assert [e["campo"] for e in errores(respuesta)] == ["descripcion"]


def test_acepta_descripcion_de_exactamente_500_caracteres(crear_tarea, materia_id):
    assert crear_tarea(materia_id, descripcion="a" * 500).status_code == 201


def test_recorta_espacios_de_la_descripcion_antes_de_medir_la_longitud(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, descripcion="a" * 500 + "   ")
    assert respuesta.status_code == 201


@pytest.mark.parametrize("descripcion", ["", "   "])
def test_descripcion_vacia_se_guarda_como_nula(crear_tarea, materia_id, descripcion):
    respuesta = crear_tarea(materia_id, descripcion=descripcion)
    assert respuesta.status_code == 201
    assert respuesta.json()["descripcion"] is None


def test_rechaza_fecha_faltante(cliente, materia_id):
    respuesta = cliente.post("/api/tareas", json={"materia_id": materia_id, "titulo": "Taller"})
    assert respuesta.status_code == 422
    assert errores(respuesta) == [{"campo": "fecha_entrega", "mensaje": "Este campo es obligatorio."}]


@pytest.mark.parametrize("fecha", ["", "no es una fecha", "2030-13-45T10:00:00Z", "2030-01-01T12:00:00"])
def test_rechaza_fecha_invalida_o_sin_zona_horaria(crear_tarea, materia_id, fecha):
    respuesta = crear_tarea(materia_id, fecha_entrega=fecha)
    assert respuesta.status_code == 422
    assert [e["campo"] for e in errores(respuesta)] == ["fecha_entrega"]


def test_la_fecha_se_normaliza_a_utc(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, fecha_entrega="2030-01-01T07:00:00-05:00")
    assert respuesta.json()["fecha_entrega"] == "2030-01-01T12:00:00Z"


def test_acepta_fecha_pasada(crear_tarea, materia_id):
    respuesta = crear_tarea(materia_id, fecha_entrega="2000-01-01T00:00:00Z")
    assert respuesta.status_code == 201


def test_rechaza_materia_inexistente(crear_tarea):
    respuesta = crear_tarea(999)
    assert respuesta.status_code == 422
    assert errores(respuesta) == [{"campo": "materia_id", "mensaje": "La materia seleccionada no existe."}]


def test_rechaza_materia_faltante_o_no_numerica(cliente):
    base = {"titulo": "Taller", "fecha_entrega": "2030-01-01T12:00:00Z"}
    sin_materia = cliente.post("/api/tareas", json=base)
    no_numerica = cliente.post("/api/tareas", json={**base, "materia_id": "abc"})
    assert sin_materia.status_code == 422
    assert no_numerica.status_code == 422
    assert [e["campo"] for e in errores(sin_materia)] == ["materia_id"]
    assert [e["campo"] for e in errores(no_numerica)] == ["materia_id"]


def test_listar_tareas_incluye_materia_en_orden_de_creacion(cliente, crear_tarea, materia_id):
    crear_tarea(materia_id, "Primera")
    crear_tarea(materia_id, "Segunda")
    tareas = cliente.get("/api/tareas").json()
    assert [t["titulo"] for t in tareas] == ["Primera", "Segunda"]
    assert tareas[0]["materia"]["color"] == "azul"
