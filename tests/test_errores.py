"""Pruebas del formato de errores inesperados."""
from fastapi.testclient import TestClient

from app.main import crear_app


def test_error_inesperado_responde_500_en_espanol(tmp_path, monkeypatch):
    app = crear_app(tmp_path / "prueba.db")

    def conexion_rota(ruta):
        raise RuntimeError("fallo simulado")

    monkeypatch.setattr("app.rutas.obtener_conexion", conexion_rota)
    cliente = TestClient(app, raise_server_exceptions=False)

    respuesta = cliente.get("/api/materias")
    assert respuesta.status_code == 500
    assert respuesta.json() == {
        "errores": [{"campo": None, "mensaje": "Ocurrió un error inesperado. Inténtelo de nuevo."}]
    }
