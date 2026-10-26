"""Cálculo de las marcas "vencida" y "urgente" de una tarea."""
from datetime import datetime, timedelta, timezone

from app.modelos import FORMATO_FECHA

VENTANA_URGENTE = timedelta(hours=48)


def calcular_alerta(fecha_entrega, completada, ahora):
    """Devuelve "vencida", "urgente" o None según la hora `ahora` (con zona horaria).

    - Una tarea completada nunca tiene alerta.
    - Vence ya (o antes) la hora actual: "vencida".
    - Vence después de ahora y dentro de 48 horas exactas (incluidas): "urgente".
    """
    if completada:
        return None
    entrega = datetime.strptime(fecha_entrega, FORMATO_FECHA).replace(tzinfo=timezone.utc)
    if entrega <= ahora:
        return "vencida"
    if entrega <= ahora + VENTANA_URGENTE:
        return "urgente"
    return None
