"""Con hasta 200 tareas el listado y los filtros responden sin espera perceptible (SC-006)."""
import time

CANTIDAD_TAREAS = 200
LIMITE_SEGUNDOS = 1.0


def test_listado_y_filtros_con_200_tareas_responden_en_menos_de_un_segundo(cliente, crear_materia, crear_tarea):
    materia_id = crear_materia().json()["id"]
    for numero in range(CANTIDAD_TAREAS):
        dia = 1 + numero % 28
        crear_tarea(materia_id, f"Tarea {numero}", f"2030-02-{dia:02d}T10:00:00Z")

    for parametros in ({}, {"estado": "pendiente"}, {"materia_id": materia_id, "estado": "pendiente"}):
        inicio = time.perf_counter()
        respuesta = cliente.get("/api/tareas", params=parametros)
        duracion = time.perf_counter() - inicio

        assert respuesta.status_code == 200
        assert len(respuesta.json()) == CANTIDAD_TAREAS
        assert duracion < LIMITE_SEGUNDOS
