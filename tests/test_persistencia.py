"""Los datos del estudiante deben seguir ahí al reiniciar la aplicación (FR-012, SC-007)."""
from fastapi.testclient import TestClient

from app.main import crear_app


def test_materias_y_tareas_persisten_al_reiniciar(tmp_path):
    ruta = tmp_path / "persistente.db"

    primera = TestClient(crear_app(ruta))
    materia_id = primera.post("/api/materias", json={"nombre": "Cálculo", "color": "azul"}).json()["id"]
    tarea_id = primera.post(
        "/api/tareas",
        json={"materia_id": materia_id, "titulo": "Taller 3", "fecha_entrega": "2030-01-01T12:00:00Z"},
    ).json()["id"]
    primera.patch(f"/api/tareas/{tarea_id}", json={"completada": True})

    reiniciada = TestClient(crear_app(ruta))
    materias = reiniciada.get("/api/materias").json()
    tareas = reiniciada.get("/api/tareas").json()

    assert [m["nombre"] for m in materias] == ["Cálculo"]
    assert [t["titulo"] for t in tareas] == ["Taller 3"]
    assert tareas[0]["completada"] is True
