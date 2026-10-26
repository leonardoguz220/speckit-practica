"""Pruebas de la base de la interfaz y del formato de errores de rutas inexistentes."""
import re
from html.parser import HTMLParser


class RecolectorDeControles(HTMLParser):
    """Reúne los campos de formulario y los `for` de las etiquetas de un HTML."""

    def __init__(self):
        super().__init__()
        self.campos = []
        self.etiquetas = set()

    def handle_starttag(self, etiqueta, atributos):
        atributos = dict(atributos)
        if etiqueta in ("input", "select", "textarea") and atributos.get("type") != "hidden":
            self.campos.append(atributos.get("id"))
        if etiqueta == "label" and "for" in atributos:
            self.etiquetas.add(atributos["for"])


def test_pagina_principal_declara_idioma_espanol(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert '<html lang="es">' in respuesta.text


def test_pagina_principal_es_adaptable_a_celular(cliente):
    html = cliente.get("/").text
    assert re.search(r'<meta name="viewport" content="width=device-width, initial-scale=1">', html)


def test_pagina_principal_tiene_titulo(cliente):
    html = cliente.get("/").text
    assert re.search(r"<title>.+</title>", html)


def test_todos_los_campos_tienen_su_etiqueta(cliente):
    recolector = RecolectorDeControles()
    recolector.feed(cliente.get("/").text)

    assert recolector.campos, "No se encontraron campos de formulario."
    sin_etiqueta = [campo for campo in recolector.campos if campo not in recolector.etiquetas]
    assert sin_etiqueta == []


def test_el_javascript_nunca_escribe_con_inner_html(cliente):
    # Los datos del estudiante solo deben escribirse con textContent para evitar inyección de HTML.
    codigo = cliente.get("/app.js").text
    assert "innerHTML" not in codigo
    assert "insertAdjacentHTML" not in codigo


def test_ruta_api_inexistente_responde_404_con_formato_de_errores(cliente):
    respuesta = cliente.get("/api/inexistente")
    assert respuesta.status_code == 404
    errores = respuesta.json()["errores"]
    assert errores == [{"campo": None, "mensaje": "No se encontró el recurso solicitado."}]
