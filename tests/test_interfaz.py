"""Pruebas de la interfaz en un navegador real (pytest-playwright).

Cubren lo que la API no puede comprobar: mensajes junto a cada campo, texto conservado tras un
rechazo, avisos de lista vacía, texto del estudiante mostrado como texto, etiquetas de alerta,
filtros y diseño sin desplazamiento horizontal en celular.
"""
import threading
import time
from datetime import datetime, timedelta, timezone

import httpx
import pytest
import uvicorn
from playwright.sync_api import Page, expect

from app.main import crear_app


@pytest.fixture
def servidor(tmp_path):
    """Levanta la aplicación en un puerto libre con una base de datos temporal."""
    configuracion = uvicorn.Config(crear_app(tmp_path / "interfaz.db"), host="127.0.0.1", port=0, log_level="warning")
    uvicorn_servidor = uvicorn.Server(configuracion)
    hilo = threading.Thread(target=uvicorn_servidor.run, daemon=True)
    hilo.start()

    limite = time.time() + 10
    while not uvicorn_servidor.started and time.time() < limite:
        time.sleep(0.05)
    assert uvicorn_servidor.started, "El servidor de pruebas no arrancó."

    puerto = uvicorn_servidor.servers[0].sockets[0].getsockname()[1]
    yield f"http://127.0.0.1:{puerto}"

    uvicorn_servidor.should_exit = True
    hilo.join(timeout=5)


def crear_materia(url, nombre="Cálculo", color="azul"):
    return httpx.post(f"{url}/api/materias", json={"nombre": nombre, "color": color}).json()["id"]


def crear_tarea(url, materia_id, titulo, **diferencia):
    """Crea una tarea que vence a `diferencia` de la hora actual."""
    fecha = (datetime.now(timezone.utc) + timedelta(**diferencia)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cuerpo = {"materia_id": materia_id, "titulo": titulo, "fecha_entrega": fecha}
    return httpx.post(f"{url}/api/tareas", json=cuerpo).json()["id"]


def test_error_de_validacion_aparece_junto_al_campo_y_conserva_lo_escrito(page: Page, servidor):
    page.goto(servidor)
    page.fill("#materia-nombre", "Cálculo")
    page.click("text=Registrar materia")

    expect(page.locator("#error-materia-color")).to_have_text("Elija uno de los colores disponibles.")
    expect(page.locator("#materia-nombre")).to_have_value("Cálculo")
    expect(page.locator("#materia-color")).to_have_attribute("aria-invalid", "true")


def test_avisos_de_lista_vacia(page: Page, servidor):
    page.goto(servidor)
    expect(page.locator("#vacio-materias")).to_be_visible()
    expect(page.locator("#aviso-sin-materias")).to_be_visible()
    expect(page.locator("#vacio-tareas")).to_be_visible()
    expect(page.locator("#form-tarea")).to_be_hidden()


def test_el_titulo_del_estudiante_se_muestra_como_texto(page: Page, servidor):
    crear_materia(servidor)
    page.goto(servidor)
    page.select_option("#tarea-materia", label="Cálculo")
    page.fill("#tarea-titulo", "<b>Taller 3</b>")
    page.fill("#tarea-fecha", "2030-01-01T12:00")
    page.click("text=Guardar tarea")

    expect(page.locator("#lista-tareas h3")).to_have_text("<b>Taller 3</b>")
    assert page.locator("#lista-tareas b").count() == 0
    expect(page.locator("#form-tarea [data-mensaje-exito]")).to_have_text("Tarea guardada.")


def test_no_se_borra_una_materia_con_tareas(page: Page, servidor):
    materia_id = crear_materia(servidor)
    crear_tarea(servidor, materia_id, "Taller", days=5)
    page.goto(servidor)

    page.click("button[aria-label='Borrar la materia Cálculo']")

    expect(page.locator("#error-borrado")).to_have_text("No se puede borrar la materia porque tiene tareas asociadas.")
    expect(page.locator("#lista-materias li")).to_have_count(1)


def test_etiquetas_de_vencida_y_urgente_con_texto(page: Page, servidor):
    materia_id = crear_materia(servidor)
    crear_tarea(servidor, materia_id, "Atrasada", days=-1)
    crear_tarea(servidor, materia_id, "Para mañana", hours=24)
    crear_tarea(servidor, materia_id, "Tranquila", days=10)
    page.goto(servidor)

    tarjetas = page.locator("#lista-tareas li")
    expect(tarjetas).to_have_count(3)
    expect(tarjetas.nth(0).locator(".etiqueta")).to_have_text("Vencida")
    expect(tarjetas.nth(1).locator(".etiqueta")).to_have_text("Urgente")
    expect(tarjetas.nth(2).locator(".etiqueta")).to_have_count(0)


def test_completar_y_filtrar(page: Page, servidor):
    materia_id = crear_materia(servidor)
    crear_tarea(servidor, materia_id, "Taller A", days=2)
    crear_tarea(servidor, materia_id, "Taller B", days=3)
    page.goto(servidor)

    # Sin tareas completadas, el filtro "Completadas" no encuentra nada.
    page.select_option("#filtro-estado", "completada")
    expect(page.locator("#sin-resultados")).to_be_visible()
    page.click("#quitar-filtros")
    expect(page.locator("#lista-tareas li")).to_have_count(2)

    page.click("button[aria-label='Marcar como completada: Taller A']")
    expect(page.locator("#lista-tareas li").first).to_contain_text("Completada")

    page.select_option("#filtro-estado", "pendiente")
    expect(page.locator("#lista-tareas li")).to_have_count(1)
    expect(page.locator("#lista-tareas h3")).to_have_text("Taller B")


def test_sin_desplazamiento_horizontal_en_celular(page: Page, servidor):
    materia_id = crear_materia(servidor, "M" * 50)
    crear_tarea(servidor, materia_id, "T" * 100, days=3)
    page.set_viewport_size({"width": 360, "height": 740})
    page.goto(servidor)
    expect(page.locator("#lista-tareas li")).to_have_count(1)

    ancho_documento = page.evaluate("document.documentElement.scrollWidth")
    assert ancho_documento <= 360
