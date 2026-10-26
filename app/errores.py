"""Formato único de errores de la API, con mensajes en español.

Todos los errores responden {"errores": [{"campo": ..., "mensaje": ...}]}.
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

MENSAJES_POR_TIPO = {
    "missing": "Este campo es obligatorio.",
    "string_type": "Debe ser un texto.",
    "int_parsing": "Debe ser un número entero.",
    "int_type": "Debe ser un número entero.",
    "bool_parsing": "Debe ser verdadero o falso.",
    "bool_type": "Debe ser verdadero o falso.",
    "enum": "Valor no permitido.",
    "literal_error": "Valor no permitido.",
    "json_invalid": "El cuerpo de la solicitud no es un JSON válido.",
}

MENSAJES_HTTP = {
    404: "No se encontró el recurso solicitado.",
    405: "Método no permitido.",
}


class ErrorApi(Exception):
    """Error esperado de negocio (404, 409...) con un mensaje para el estudiante."""

    def __init__(self, estado, mensaje, campo=None):
        super().__init__(mensaje)
        self.estado = estado
        self.mensaje = mensaje
        self.campo = campo


def _respuesta(estado, errores):
    return JSONResponse(status_code=estado, content={"errores": errores})


async def manejar_error_api(solicitud: Request, error: ErrorApi):
    return _respuesta(error.estado, [{"campo": error.campo, "mensaje": error.mensaje}])


def _mensaje_validacion(error):
    """Traduce un error de Pydantic; los validadores propios ya traen texto en español."""
    if error["type"] == "value_error":
        return str(error["msg"]).removeprefix("Value error, ")
    return MENSAJES_POR_TIPO.get(error["type"], "Valor no válido.")


async def manejar_validacion(solicitud: Request, error: RequestValidationError):
    errores = []
    for detalle in error.errors():
        ubicacion = detalle["loc"]
        campo = ubicacion[-1] if len(ubicacion) > 1 and isinstance(ubicacion[-1], str) else None
        errores.append({"campo": campo, "mensaje": _mensaje_validacion(detalle)})
    return _respuesta(422, errores)


async def manejar_http(solicitud: Request, error: StarletteHTTPException):
    mensaje = MENSAJES_HTTP.get(error.status_code, "No se pudo completar la solicitud.")
    return _respuesta(error.status_code, [{"campo": None, "mensaje": mensaje}])


async def manejar_error_inesperado(solicitud: Request, error: Exception):
    mensaje = "Ocurrió un error inesperado. Inténtelo de nuevo."
    return _respuesta(500, [{"campo": None, "mensaje": mensaje}])


def registrar_manejadores(app: FastAPI):
    app.add_exception_handler(Exception, manejar_error_inesperado)
    app.add_exception_handler(ErrorApi, manejar_error_api)
    app.add_exception_handler(RequestValidationError, manejar_validacion)
    app.add_exception_handler(StarletteHTTPException, manejar_http)
