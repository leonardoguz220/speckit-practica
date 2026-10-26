"""Pruebas de las materias: creación, validación, unicidad, listado y borrado."""
import pytest

COLORES = ["rojo", "naranja", "amarillo", "verde", "turquesa", "azul", "morado", "rosa"]


def campos_con_error(respuesta):
    return [error["campo"] for error in respuesta.json()["errores"]]


def test_crear_materia_valida(crear_materia):
    respuesta = crear_materia("Cálculo", "azul")
    assert respuesta.status_code == 201
    assert respuesta.json() == {"id": 1, "nombre": "Cálculo", "color": "azul"}


@pytest.mark.parametrize("color", COLORES)
def test_acepta_los_ocho_colores_de_la_paleta(crear_materia, color):
    assert crear_materia(f"Materia {color}", color).status_code == 201


def test_recorta_espacios_del_nombre(crear_materia):
    respuesta = crear_materia("  Física  ", "verde")
    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Física"


@pytest.mark.parametrize("nombre", ["", "   ", "a" * 51])
def test_rechaza_nombre_vacio_solo_espacios_o_de_51_caracteres(crear_materia, nombre):
    respuesta = crear_materia(nombre, "azul")
    assert respuesta.status_code == 422
    assert campos_con_error(respuesta) == ["nombre"]


def test_acepta_nombre_de_exactamente_50_caracteres(crear_materia):
    assert crear_materia("a" * 50, "azul").status_code == 201


def test_rechaza_nombre_faltante(cliente):
    respuesta = cliente.post("/api/materias", json={"color": "azul"})
    assert respuesta.status_code == 422
    assert respuesta.json()["errores"] == [{"campo": "nombre", "mensaje": "Este campo es obligatorio."}]


@pytest.mark.parametrize("color", ["negro", "", "AZUL"])
def test_rechaza_color_fuera_de_la_paleta(crear_materia, color):
    respuesta = crear_materia("Cálculo", color)
    assert respuesta.status_code == 422
    assert campos_con_error(respuesta) == ["color"]


def test_rechaza_color_faltante(cliente):
    respuesta = cliente.post("/api/materias", json={"nombre": "Cálculo"})
    assert respuesta.status_code == 422
    assert campos_con_error(respuesta) == ["color"]


@pytest.mark.parametrize(
    "primero, segundo",
    [("Cálculo", "cálculo"), ("Álgebra", "álgebra"), ("Física", "FÍSICA")],
)
def test_rechaza_nombre_repetido_sin_distinguir_mayusculas(crear_materia, primero, segundo):
    assert crear_materia(primero, "azul").status_code == 201
    respuesta = crear_materia(segundo, "rojo")
    assert respuesta.status_code == 409
    assert respuesta.json()["errores"][0]["campo"] == "nombre"
    assert "Ya existe" in respuesta.json()["errores"][0]["mensaje"]


def test_mensajes_de_validacion_estan_en_espanol(crear_materia):
    respuesta = crear_materia("", "azul")
    assert respuesta.json()["errores"] == [
        {"campo": "nombre", "mensaje": "El nombre no puede estar vacío."}
    ]


def test_listar_materias_ordenadas_por_nombre(cliente, crear_materia):
    for nombre in ["Física", "Cálculo", "Álgebra"]:
        crear_materia(nombre, "azul")
    nombres = [materia["nombre"] for materia in cliente.get("/api/materias").json()]
    assert nombres == ["Álgebra", "Cálculo", "Física"]


def test_listar_sin_materias_devuelve_lista_vacia(cliente):
    assert cliente.get("/api/materias").json() == []


def test_borrar_materia_sin_tareas(cliente, crear_materia):
    materia_id = crear_materia().json()["id"]
    respuesta = cliente.delete(f"/api/materias/{materia_id}")
    assert respuesta.status_code == 204
    assert cliente.get("/api/materias").json() == []


def test_no_borra_materia_con_tareas_y_conserva_las_tareas(cliente, crear_materia, crear_tarea):
    materia_id = crear_materia().json()["id"]
    crear_tarea(materia_id)
    respuesta = cliente.delete(f"/api/materias/{materia_id}")
    assert respuesta.status_code == 409
    assert respuesta.json()["errores"][0]["mensaje"] == (
        "No se puede borrar la materia porque tiene tareas asociadas."
    )
    assert len(cliente.get("/api/materias").json()) == 1
    assert len(cliente.get("/api/tareas").json()) == 1


def test_borrar_materia_inexistente(cliente):
    respuesta = cliente.delete("/api/materias/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["errores"][0]["mensaje"] == "La materia no existe."


def test_borrar_materia_con_id_no_numerico(cliente):
    respuesta = cliente.delete("/api/materias/abc")
    assert respuesta.status_code == 422
