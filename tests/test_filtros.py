"""Pruebas de los filtros del listado por materia y por estado."""
import pytest


@pytest.fixture
def escenario(cliente, crear_materia, crear_tarea):
    """Dos materias; Cálculo con una pendiente y una completada, Física con una pendiente."""
    calculo = crear_materia("Cálculo", "azul").json()["id"]
    fisica = crear_materia("Física", "verde").json()["id"]
    crear_tarea(calculo, "Cálculo pendiente", "2030-01-02T12:00:00Z")
    hecha = crear_tarea(calculo, "Cálculo hecha", "2030-01-01T12:00:00Z").json()["id"]
    crear_tarea(fisica, "Física pendiente", "2030-01-03T12:00:00Z")
    cliente.patch(f"/api/tareas/{hecha}", json={"completada": True})
    return {"calculo": calculo, "fisica": fisica}


def titulos(cliente, **parametros):
    respuesta = cliente.get("/api/tareas", params=parametros)
    assert respuesta.status_code == 200
    return [tarea["titulo"] for tarea in respuesta.json()]


def test_sin_filtros_devuelve_todo(cliente, escenario):
    assert len(titulos(cliente)) == 3


def test_filtra_por_materia(cliente, escenario):
    assert titulos(cliente, materia_id=escenario["fisica"]) == ["Física pendiente"]
    assert titulos(cliente, materia_id=escenario["calculo"]) == ["Cálculo hecha", "Cálculo pendiente"]


def test_filtra_por_estado(cliente, escenario):
    assert titulos(cliente, estado="completada") == ["Cálculo hecha"]
    assert titulos(cliente, estado="pendiente") == ["Cálculo pendiente", "Física pendiente"]


def test_combina_materia_y_estado(cliente, escenario):
    assert titulos(cliente, materia_id=escenario["calculo"], estado="pendiente") == ["Cálculo pendiente"]
    assert titulos(cliente, materia_id=escenario["fisica"], estado="completada") == []


def test_materia_inexistente_devuelve_lista_vacia(cliente, escenario):
    assert titulos(cliente, materia_id=999) == []


@pytest.mark.parametrize("parametros, campo", [({"estado": "otro"}, "estado"), ({"materia_id": "abc"}, "materia_id")])
def test_parametros_invalidos_responden_422(cliente, parametros, campo):
    respuesta = cliente.get("/api/tareas", params=parametros)
    assert respuesta.status_code == 422
    assert [e["campo"] for e in respuesta.json()["errores"]] == [campo]


def test_el_orden_por_fecha_se_mantiene_con_filtros(cliente, escenario):
    # La completada vence antes (2030-01-01) que la pendiente (2030-01-02).
    assert titulos(cliente, materia_id=escenario["calculo"]) == ["Cálculo hecha", "Cálculo pendiente"]
