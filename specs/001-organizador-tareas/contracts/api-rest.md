# Contrato de la API REST: Organizador de tareas académicas

Base: `/api`. Formato: JSON (`application/json`). Sin autenticación (un usuario por instancia).
Modelo de datos: [data-model.md](../data-model.md).

## Formato de errores

Todos los errores usan el mismo cuerpo, con mensajes en español:

```json
{ "errores": [ { "campo": "nombre", "mensaje": "El nombre no puede estar vacío." } ] }
```

`campo` es `null` cuando el error no pertenece a un campo concreto.

| Código | Cuándo |
|--------|--------|
| 422 | Datos de entrada inválidos (faltantes, vacíos, demasiado largos, formato o valor no permitido) |
| 404 | La materia o la tarea no existe |
| 409 | Conflicto: nombre de materia repetido, o intento de borrar una materia con tareas |

## Materias

### `GET /api/materias`

Devuelve todas las materias ordenadas por nombre.

**200**
```json
[ { "id": 1, "nombre": "Cálculo", "color": "azul" } ]
```

### `POST /api/materias`

**Cuerpo**
```json
{ "nombre": "Cálculo", "color": "azul" }
```

| Campo | Regla |
|-------|-------|
| `nombre` | obligatorio, sin espacios sobrantes, 1 a 50 caracteres, único sin distinguir mayúsculas |
| `color` | obligatorio, uno de `rojo`, `naranja`, `amarillo`, `verde`, `turquesa`, `azul`, `morado`, `rosa` |

**201** → la materia creada (`id`, `nombre`, `color`). **422** si hay datos inválidos. **409** si el
nombre ya existe.

### `DELETE /api/materias/{id}`

**204** sin cuerpo si se borró. **404** si no existe. **409** si la materia tiene tareas
(`"No se puede borrar la materia porque tiene tareas asociadas."`); las tareas se conservan.

## Tareas

### `GET /api/tareas`

Devuelve las tareas ordenadas por `fecha_entrega` ascendente y, a igual fecha, por orden de
creación.

**Parámetros de consulta (opcionales, combinables)**

| Parámetro | Valores |
|-----------|---------|
| `materia_id` | entero; solo tareas de esa materia |
| `estado` | `pendiente` o `completada` |

Un valor inválido de `estado` o `materia_id` responde **422**. Una materia inexistente devuelve
lista vacía.

**200**
```json
[
  {
    "id": 7,
    "titulo": "Taller 3",
    "descripcion": null,
    "fecha_entrega": "2026-10-28T15:00:00Z",
    "completada": false,
    "alerta": "urgente",
    "materia": { "id": 1, "nombre": "Cálculo", "color": "azul" }
  }
]
```

`alerta` vale `"vencida"`, `"urgente"` o `null` (ver regla en [research.md](../research.md)).

### `POST /api/tareas`

**Cuerpo**
```json
{
  "materia_id": 1,
  "titulo": "Taller 3",
  "descripcion": "Capítulos 4 y 5",
  "fecha_entrega": "2026-10-28T15:00:00Z"
}
```

| Campo | Regla |
|-------|-------|
| `materia_id` | obligatorio, debe existir |
| `titulo` | obligatorio, sin espacios sobrantes, 1 a 100 caracteres |
| `descripcion` | opcional, hasta 500 caracteres; vacía se trata como ausente |
| `fecha_entrega` | obligatoria, ISO 8601 con zona horaria; se acepta una fecha pasada |

**201** → la tarea creada con el mismo formato de `GET`. **422** si hay datos inválidos o la
materia no existe (`campo: "materia_id"`).

### `PATCH /api/tareas/{id}`

Cambia el estado de la tarea.

**Cuerpo**
```json
{ "completada": true }
```

**200** → la tarea actualizada con su `alerta` recalculada. **404** si no existe. **422** si
`completada` falta o no es booleano.

## Interfaz estática

`GET /` sirve `index.html` (con `estilos.css` y `app.js`). Las rutas `/api/*` tienen prioridad
sobre los archivos estáticos.
