"""Modelos de entrada (validados) y de respuesta de la API."""
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, StrictBool, field_validator

COLORES = ("rojo", "naranja", "amarillo", "verde", "turquesa", "azul", "morado", "rosa")

MAX_NOMBRE_MATERIA = 50
MAX_TITULO = 100
MAX_DESCRIPCION = 500

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"


def _texto_obligatorio(valor, etiqueta, maximo):
    """Recorta espacios y exige entre 1 y `maximo` caracteres."""
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{etiqueta} no puede estar vacío.")
    if len(valor) > maximo:
        raise ValueError(f"{etiqueta} no puede tener más de {maximo} caracteres.")
    return valor


def _leer_fecha_iso(valor):
    try:
        return datetime.fromisoformat(valor.strip())
    except ValueError:
        raise ValueError("La fecha de entrega no es válida.")


def _a_texto_utc(fecha):
    """Convierte a UTC y da formato; falla si la conversión se sale del rango de fechas."""
    try:
        return fecha.astimezone(timezone.utc).strftime(FORMATO_FECHA)
    except (OverflowError, ValueError):
        raise ValueError("La fecha de entrega no es válida.")


class MateriaEntrada(BaseModel):
    nombre: str
    color: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        return _texto_obligatorio(valor, "El nombre", MAX_NOMBRE_MATERIA)

    @field_validator("color")
    @classmethod
    def validar_color(cls, valor):
        if valor not in COLORES:
            raise ValueError("Elija uno de los colores disponibles.")
        return valor


class Materia(BaseModel):
    id: int
    nombre: str
    color: str


class TareaEntrada(BaseModel):
    materia_id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_entrega: str

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor):
        return _texto_obligatorio(valor, "El título", MAX_TITULO)

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        if valor is None:
            return None
        valor = valor.strip()
        if not valor:
            return None
        if len(valor) > MAX_DESCRIPCION:
            raise ValueError(f"La descripción no puede tener más de {MAX_DESCRIPCION} caracteres.")
        return valor

    @field_validator("fecha_entrega")
    @classmethod
    def validar_fecha_entrega(cls, valor):
        """Exige ISO 8601 con zona horaria y la normaliza a UTC con precisión de segundos."""
        fecha = _leer_fecha_iso(valor)
        if fecha.tzinfo is None:
            raise ValueError("La fecha de entrega debe incluir la zona horaria.")
        return _a_texto_utc(fecha)


class TareaEstado(BaseModel):
    """Cambio de estado de una tarea; StrictBool evita aceptar "true", 1 o "si"."""

    completada: StrictBool


class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    fecha_entrega: str
    completada: bool
    alerta: Optional[Literal["vencida", "urgente"]]
    materia: Materia
