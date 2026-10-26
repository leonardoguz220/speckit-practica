"""Pruebas unitarias de calcular_alerta: límites de vencimiento y de las 48 horas."""
from datetime import datetime, timedelta, timezone

import pytest

from app.plazos import calcular_alerta

AHORA = datetime(2030, 1, 10, 12, 0, 0, tzinfo=timezone.utc)


def entrega(**diferencia):
    """Fecha de entrega en el formato guardado, a `diferencia` de AHORA."""
    return (AHORA + timedelta(**diferencia)).strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.mark.parametrize(
    "diferencia, esperado",
    [
        (dict(hours=47), "urgente"),
        (dict(hours=48), "urgente"),
        (dict(hours=48, minutes=1), None),
        (dict(hours=1), "urgente"),
        (dict(seconds=1), "urgente"),
        (dict(seconds=0), "vencida"),
        (dict(seconds=-1), "vencida"),
        (dict(days=-30), "vencida"),
        (dict(days=30), None),
    ],
)
def test_alerta_de_tarea_pendiente(diferencia, esperado):
    assert calcular_alerta(entrega(**diferencia), False, AHORA) == esperado


@pytest.mark.parametrize("diferencia", [dict(days=-3), dict(hours=5), dict(days=10)])
def test_tarea_completada_no_tiene_alerta(diferencia):
    assert calcular_alerta(entrega(**diferencia), True, AHORA) is None
