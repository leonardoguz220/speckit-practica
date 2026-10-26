# Plan de implementación: Organizador de tareas académicas

**Rama**: `001-organizador-tareas` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](spec.md)

**Entrada**: especificación de la funcionalidad en `specs/001-organizador-tareas/spec.md`

## Resumen

Aplicación web para que estudiantes de la UPB organicen sus tareas: registran materias (nombre y
color), crean tareas asociadas a una materia, ven un listado ordenado por fecha de entrega con
marcas de "vencida" y "urgente", las completan y las filtran por materia o estado.

Enfoque técnico: un único proyecto Python con FastAPI que expone una API REST bajo `/api` y sirve
también el frontend (HTML, CSS y JavaScript sin frameworks). Los datos se guardan en SQLite con el
módulo estándar `sqlite3`, sin ORM. Todas las reglas (validación, unicidad, borrado de materias y
cálculo de vencida/urgente) viven en el backend y se prueban con pytest; el JavaScript solo
presenta datos y envía formularios.

## Contexto técnico

**Lenguaje/Versión**: Python 3.12

**Dependencias principales**: FastAPI, Uvicorn (servidor); `httpx` y `pytest-playwright` solo para las pruebas

**Almacenamiento**: SQLite (módulo estándar `sqlite3`), un archivo local

**Pruebas**: pytest con `TestClient` de FastAPI para la API y `pytest-playwright` (Chromium) para la interfaz

**Plataforma objetivo**: navegador web moderno en celular y computadora; el servidor corre en el
dispositivo del estudiante (un usuario por instancia)

**Tipo de proyecto**: aplicación web de un solo proyecto (API + archivos estáticos)

**Metas de rendimiento**: listado y filtros con hasta 200 tareas sin espera perceptible (SC-006)

**Restricciones**: sin Docker, sin microservicios, sin inicio de sesión, sin frameworks de
frontend, interfaz y mensajes en español

**Escala/Alcance**: un usuario, decenas de materias y hasta unos cientos de tareas; 1 pantalla
principal

## Verificación de la constitución

*PUERTA: debe cumplirse antes de la investigación (Fase 0). Se vuelve a verificar tras el diseño
(Fase 1).*

| Principio | Evaluación | Estado |
|-----------|------------|--------|
| I. Simplicidad primero | Un solo proyecto, `sqlite3` sin ORM, sin capa de repositorios, sin frameworks de frontend, sin Docker. Una sola dependencia de ejecución relevante (FastAPI + Uvicorn). | Cumple |
| II. Pruebas obligatorias | pytest cubre cada endpoint, las reglas de validación y el cálculo de plazos (incluidos los límites de 48 h). Hay pruebas automáticas de los archivos estáticos (idioma, viewport, etiquetas) y pruebas de la interfaz en un navegador real con `pytest-playwright` (mensajes junto al campo, texto conservado, avisos vacíos, alertas, filtros y celular de 360 px). | Cumple |
| III. Código legible | Módulos pequeños con una responsabilidad cada uno (`db`, `modelos`, `plazos`, `rutas`); nombres de dominio en español. | Cumple |
| IV. Validación de entradas | Toda entrada se valida en el servidor con modelos Pydantic y mensajes en español; el frontend repite las comprobaciones solo para dar respuesta inmediata. | Cumple |
| V. Accesible y responsivo | CSS adaptable (diseño fluido con `viewport`), campos con `<label>`, contraste suficiente, uso con teclado, el color nunca es el único indicador. | Cumple |

**Nota sobre el principio II**: no se agrega un entorno de pruebas de JavaScript (principio I);
en su lugar, el comportamiento del navegador se prueba de extremo a extremo con `pytest-playwright`
dentro de pytest, sin introducir otra herramienta. La validación manual de
[quickstart.md](quickstart.md) queda como verificación final de lo visual (aspecto y contraste).

**Re-verificación tras el diseño (Fase 1)**: sin cambios; el diseño mantiene los cinco principios
y no introduce violaciones.

## Estructura del proyecto

### Documentación (esta funcionalidad)

```text
specs/001-organizador-tareas/
├── plan.md              # Este archivo (salida de /speckit-plan)
├── research.md          # Fase 0 (salida de /speckit-plan)
├── data-model.md        # Fase 1 (salida de /speckit-plan)
├── quickstart.md        # Fase 1 (salida de /speckit-plan)
├── contracts/
│   └── api-rest.md      # Fase 1 (salida de /speckit-plan)
└── tasks.md             # Fase 2 (salida de /speckit-tasks; NO lo crea /speckit-plan)
```

### Código fuente (raíz del repositorio)

```text
app/
├── __init__.py
├── main.py              # crea la aplicación FastAPI, registra rutas y sirve /static
├── db.py                # conexión SQLite y creación de tablas
├── modelos.py           # modelos Pydantic: entradas validadas y respuestas
├── plazos.py            # función pura: calcula "vencida" / "urgente"
├── rutas.py             # endpoints /api/materias y /api/tareas
├── errores.py           # formato único de errores en español
└── static/
    ├── index.html       # pantalla única
    ├── estilos.css      # estilos responsivos y accesibles
    └── app.js           # llamadas a la API y renderizado

tests/
├── conftest.py          # app y base de datos temporal por prueba
├── test_materias.py
├── test_tareas.py
├── test_plazos.py       # límites de 48 h y de vencimiento
├── test_listado.py      # orden por fecha y marcas de vencida/urgente
├── test_completar.py    # marcar y desmarcar tareas
├── test_filtros.py
├── test_persistencia.py # los datos sobreviven al reinicio
├── test_volumen.py      # 200 tareas sin espera perceptible
├── test_errores.py      # error inesperado en español
├── test_estaticos.py    # idioma, viewport, etiquetas y uso seguro de textContent
└── test_interfaz.py     # interfaz en un navegador real (pytest-playwright)

requirements.txt
README.md
```

**Decisión de estructura**: un solo proyecto con el paquete `app/` y la carpeta `tests/`, tal como
pidió el equipo. No se separan `backend/` y `frontend/` porque FastAPI sirve ambos y así se evita
una segunda herramienta de construcción. La base de datos vive en `datos/tareas.db` (ruta
configurable con la variable de entorno `TAREAS_DB`; `datos/` queda fuera del control de versiones).

## Seguimiento de complejidad

Sin violaciones de la constitución; no hay nada que justificar.
