"""Fixtures compartidas: una aplicación con base de datos temporal por prueba."""
import pytest
from fastapi.testclient import TestClient

from app.main import crear_app


@pytest.fixture
def cliente(tmp_path):
    return TestClient(crear_app(tmp_path / "prueba.db"))


@pytest.fixture
def crear_materia(cliente):
    """Crea una materia por la API y devuelve la respuesta."""

    def _crear(nombre="Cálculo", color="azul"):
        return cliente.post("/api/materias", json={"nombre": nombre, "color": color})

    return _crear


@pytest.fixture
def crear_tarea(cliente):
    """Crea una tarea por la API y devuelve la respuesta."""

    def _crear(materia_id, titulo="Taller 3", fecha_entrega="2030-01-01T12:00:00Z", **extra):
        cuerpo = {"materia_id": materia_id, "titulo": titulo, "fecha_entrega": fecha_entrega}
        cuerpo.update(extra)
        return cliente.post("/api/tareas", json=cuerpo)

    return _crear
