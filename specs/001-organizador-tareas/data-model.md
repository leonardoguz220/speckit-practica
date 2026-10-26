# Modelo de datos (Fase 1): Organizador de tareas académicas

Almacenamiento en SQLite. Dos entidades: **Materia** y **Tarea**.

## Materia

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | entero, clave primaria autoincremental | generado por el sistema |
| `nombre` | texto | obligatorio; se recortan espacios; no vacío; máximo 50 caracteres; único sin distinguir mayúsculas (FR-002). La unicidad se verifica con `casefold()` en la aplicación (cubre tildes como "Álgebra"/"álgebra") y `COLLATE NOCASE` queda como respaldo en la base de datos |
| `color` | texto | obligatorio; uno de: `rojo`, `naranja`, `amarillo`, `verde`, `turquesa`, `azul`, `morado`, `rosa` |

**Relaciones**: una materia tiene cero o muchas tareas.

**Regla de borrado (FR-017)**: solo se puede borrar si no tiene tareas (pendientes ni completadas).
Si las tiene, el borrado se rechaza y las tareas se conservan.

## Tarea

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | entero, clave primaria autoincremental | generado por el sistema; define el orden de creación |
| `materia_id` | entero, clave foránea a `Materia.id` | obligatorio; debe existir (sin borrado en cascada) |
| `titulo` | texto | obligatorio; se recortan espacios; no vacío; máximo 100 caracteres |
| `descripcion` | texto o nulo | opcional; se recortan espacios; vacío se guarda como nulo; máximo 500 caracteres |
| `fecha_entrega` | texto UTC `AAAA-MM-DDTHH:MM:SSZ` | obligatorio; el cliente la envía en ISO 8601 con zona horaria; se acepta una fecha pasada |
| `completada` | booleano (0/1) | por defecto falso (pendiente) |

**Campo calculado (no se guarda)**: `alerta`, con valores `"vencida"`, `"urgente"` o `null`, según
`calcular_alerta` (ver [research.md](research.md), punto 1). Una tarea completada siempre tiene
`alerta = null`.

**Orden del listado (FR-005)**: `fecha_entrega` ascendente y, a igual fecha, `id` ascendente.

## Transiciones de estado

```text
pendiente  <──────────►  completada
        (marcar / desmarcar, FR-009)
```

- Marcar como completada elimina la `alerta`.
- Desmarcar la devuelve a pendiente y la `alerta` se recalcula según la hora actual.

## Esquema SQL de referencia

```sql
CREATE TABLE IF NOT EXISTS materias (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL COLLATE NOCASE UNIQUE,
    color  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tareas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id    INTEGER NOT NULL REFERENCES materias(id),
    titulo        TEXT NOT NULL,
    descripcion   TEXT,
    fecha_entrega TEXT NOT NULL,
    completada    INTEGER NOT NULL DEFAULT 0
);
```

Los límites de longitud y la paleta de colores se validan en la capa de entrada (modelos
Pydantic), que es la fuente de verdad de las reglas.
