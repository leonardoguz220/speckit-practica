---

description: "Lista de tareas para implementar el organizador de tareas académicas"
---

# Tareas: Organizador de tareas académicas

**Entrada**: documentos de diseño en `specs/001-organizador-tareas/`

**Prerrequisitos**: plan.md (obligatorio), spec.md (historias de usuario), research.md, data-model.md, contracts/api-rest.md

**Pruebas**: SON OBLIGATORIAS en este proyecto (constitución, principio II). Cada historia incluye sus pruebas con pytest, que se escriben primero y deben fallar antes de implementar.

**Organización**: las tareas se agrupan por historia de usuario para poder implementar y probar cada una de forma independiente.

## Formato: `[ID] [P?] [Historia] Descripción`

- **[P]**: se puede ejecutar en paralelo (archivos distintos, sin dependencias pendientes)
- **[Historia]**: historia de usuario a la que pertenece (US1, US2, US3, US4)
- Cada descripción incluye la ruta exacta del archivo

## Convenciones de rutas

Proyecto único en la raíz del repositorio, según plan.md: código en `app/`, interfaz en `app/static/`, pruebas en `tests/`.

## Fase 1: Preparación (infraestructura compartida)

**Propósito**: inicialización del proyecto y estructura básica

- [X] T001 Verificar que Python 3.12 esté disponible (`py -3.12 --version`) y crear el entorno virtual `.venv` en la raíz del repositorio
- [X] T002 Crear la estructura de carpetas y archivos vacíos `app/__init__.py`, `app/static/` y `tests/`, y el archivo `pytest.ini` en la raíz con `pythonpath = .` y `testpaths = tests`
- [X] T003 [P] Crear `requirements.txt` en la raíz con las dependencias `fastapi`, `uvicorn`, `pytest` y `httpx`
- [X] T004 [P] Crear `.gitignore` en la raíz que excluya `.venv/`, `datos/`, `__pycache__/` y `.pytest_cache/`

---

## Fase 2: Fundamentos (prerrequisitos bloqueantes)

**Propósito**: infraestructura central que DEBE estar completa antes de cualquier historia de usuario

**⚠️ CRÍTICO**: ninguna historia puede empezar hasta terminar esta fase

- [X] T005 Implementar `app/db.py`: función `obtener_conexion(ruta_db)` con `sqlite3`, `row_factory = sqlite3.Row` y `PRAGMA foreign_keys = ON`, y función `crear_tablas(conexion)` con el esquema de `data-model.md` (`materias`: `nombre TEXT NOT NULL COLLATE NOCASE UNIQUE`, `color TEXT NOT NULL`; `tareas`: `materia_id INTEGER NOT NULL REFERENCES materias(id)`, `titulo TEXT NOT NULL`, `descripcion TEXT`, `fecha_entrega TEXT NOT NULL`, `completada INTEGER NOT NULL DEFAULT 0`)
- [X] T006 [P] Implementar `app/errores.py`: excepción `ErrorApi(estado, mensaje, campo=None)` y manejadores que devuelvan siempre `{"errores": [{"campo": ..., "mensaje": ...}]}` con mensajes en español para `ErrorApi` (404 y 409), `RequestValidationError` (422, sustituyendo el texto en inglés por defecto) y rutas inexistentes
- [X] T007 Implementar `app/main.py`: función `crear_app(ruta_db=None)` que tome la ruta de la variable de entorno `TAREAS_DB` (por defecto `datos/tareas.db`, creando la carpeta `datos/`), cree las tablas, registre el router y los manejadores de errores, y monte `StaticFiles` con `html=True` en `/` DESPUÉS de las rutas `/api` (depende de T005, T006)
- [X] T008 Crear en `app/rutas.py` el `APIRouter(prefix="/api")` vacío y la dependencia `obtener_db` que abra una conexión por solicitud a partir de la ruta guardada en la aplicación y la cierre al terminar (depende de T005)
- [X] T009 Implementar `tests/conftest.py`: fixture `cliente` con `TestClient(crear_app(tmp_path / "prueba.db"))` para una base temporal por prueba, y fixtures auxiliares `crear_materia` y `crear_tarea` que llamen a la API (depende de T007)
- [X] T010 [P] Crear la base de la interfaz: `app/static/index.html` (`<html lang="es">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>`, regiones `<header>`/`<main>`, enlaces a `estilos.css` y `app.js`) y `app/static/estilos.css` (variables CSS con los 8 colores `rojo`, `naranja`, `amarillo`, `verde`, `turquesa`, `azul`, `morado`, `rosa` con contraste suficiente, diseño fluido de una columna en celular y dos en escritorio, `:focus-visible` visible)
- [X] T011 [P] Crear `app/static/app.js` con las funciones auxiliares: `pedirApi(metodo, ruta, cuerpo)` que devuelva datos o los errores del formato `{"errores": [...]}`, y `mostrarErrores(formulario, errores)` que escriba cada mensaje junto a su campo (región `aria-live="polite"`) usando solo `textContent`, nunca `innerHTML`
- [X] T012 Escribir `tests/test_estaticos.py`: `GET /` responde 200, el HTML contiene `lang="es"`, la etiqueta `viewport` y un `<title>`; `GET /api/inexistente` responde 404 con el formato de errores (depende de T007, T010)

**Punto de control**: base lista; ya se pueden empezar las historias de usuario

---

## Fase 3: Historia de usuario 1 - Registrar materias y crear tareas (Prioridad: P1) 🎯 MVP

**Meta**: el estudiante registra y borra materias y crea tareas asociadas a una materia, con validación completa.

**Prueba independiente**: registrar la materia "Cálculo" en azul, crear la tarea "Taller 3" y comprobar que se guarda con los datos de su materia; comprobar que los datos inválidos se rechazan con mensajes en español y que una materia con tareas no se puede borrar.

### Pruebas de la historia de usuario 1 (escribirlas primero; deben FALLAR antes de implementar) ⚠️

- [X] T013 [P] [US1] Escribir `tests/test_materias.py`: creación válida (201); `nombre` vacío, de solo espacios y de 51 caracteres rechazados (422) mientras uno de exactamente 50 se acepta; `color` fuera de `rojo`, `naranja`, `amarillo`, `verde`, `turquesa`, `azul`, `morado`, `rosa` rechazado; nombre repetido sin distinguir mayúsculas (`Cálculo`/`cálculo`, y también `Álgebra`/`álgebra`) responde 409; `GET /api/materias` ordenado por nombre; `DELETE` de materia sin tareas responde 204; `DELETE` de materia con tareas responde 409 y conserva las tareas; `DELETE` inexistente responde 404; todos los mensajes en español
- [X] T014 [P] [US1] Escribir `tests/test_tareas.py` (creación): tarea válida con descripción opcional (201, incluye la materia con nombre y color); `titulo` vacío, de solo espacios y de 101 caracteres rechazados mientras uno de exactamente 100 se acepta; `descripcion` de 501 caracteres rechazada y de exactamente 500 aceptada, y vacía guardada como `null`; `fecha_entrega` faltante, sin zona horaria o inválida rechazada; fecha pasada aceptada; `materia_id` inexistente rechazado con `campo: "materia_id"`; el texto se recorta (`strip`) antes de medir la longitud

### Implementación de la historia de usuario 1

- [X] T015 [US1] Crear `app/modelos.py` con modelos Pydantic: `MateriaEntrada` (`nombre`: obligatorio, recortado, 1 a 50 caracteres; `color`: uno de los 8 nombres de la paleta), `Materia`, `TareaEntrada` (`materia_id`; `titulo`: obligatorio, recortado, 1 a 100 caracteres; `descripcion`: opcional, recortada, máximo 500, vacía = `None`; `fecha_entrega`: ISO 8601 con zona horaria obligatoria, normalizada a UTC `AAAA-MM-DDTHH:MM:SSZ`) y `Tarea` (con `completada` y la `materia` anidada); mensajes de validación en español
- [X] T016 [US1] Implementar en `app/rutas.py` los endpoints de materias: `GET /api/materias` (orden por nombre), `POST /api/materias` (201; antes de insertar comparar el nombre con `casefold()` contra las materias existentes porque `COLLATE NOCASE` de SQLite solo ignora mayúsculas ASCII; 409 si ya existe) y `DELETE /api/materias/{id}` (204; 404 si no existe; 409 con "No se puede borrar la materia porque tiene tareas asociadas." si tiene tareas) (depende de T015)
- [X] T017 [US1] Implementar en `app/rutas.py` los endpoints de tareas: `POST /api/tareas` (201; 422 con `campo: "materia_id"` si la materia no existe) y `GET /api/tareas` devolviendo las tareas con su materia en orden de creación (el orden por fecha se hace en US2) (depende de T016)
- [X] T018 [US1] Interfaz de materias: en `app/static/index.html` y `app/static/app.js`, formulario con `<label>` para nombre y color (los 8 colores con nombre visible, no solo muestra de color), lista de materias con botón "Borrar" por materia, mostrar errores del servidor junto al campo sin borrar lo escrito, y renderizar con `textContent` (depende de T011, T016)
- [X] T019 [US1] Interfaz de tareas: en `app/static/index.html` y `app/static/app.js`, formulario con `<label>` para materia (lista desplegable), título, descripción y fecha y hora de entrega (`datetime-local` convertida con `new Date(valor).toISOString()`), mensaje que invite a registrar una materia si no existe ninguna, y errores junto al campo sin perder lo escrito (depende de T017, T018)
- [X] T020 [US1] Listado básico de tareas en `app/static/app.js` y `app/static/estilos.css`: tarjeta por tarea con título, fecha, estado y nombre y color de su materia, mensaje de lista vacía que invite a crear la primera tarea, diseño legible sin desplazamiento horizontal en 360 px (depende de T019)

**Punto de control**: la historia 1 es funcional y probada de forma independiente (MVP)

---

## Fase 4: Historia de usuario 2 - Listado con vencidas y urgentes (Prioridad: P2)

**Meta**: listado ordenado por fecha de entrega con tareas "vencidas" destacadas y "urgentes" en las próximas 48 horas.

**Prueba independiente**: con tareas de fecha pasada, cercana y lejana, verificar el orden y las marcas `vencida` y `urgente`.

### Pruebas de la historia de usuario 2 ⚠️

- [X] T021 [P] [US2] Escribir `tests/test_plazos.py` (unitarias de `calcular_alerta(fecha_entrega, completada, ahora)` con instantes fijos): 47 h → `"urgente"`; exactamente 48 h → `"urgente"`; 48 h y 1 minuto → `None`; fecha igual a `ahora` → `"vencida"`; fecha pasada → `"vencida"`; tarea completada vencida o urgente → `None`
- [X] T022 [P] [US2] Escribir `tests/test_listado.py`: `GET /api/tareas` ordenado por `fecha_entrega` ascendente y, con la misma fecha, por orden de creación; cada tarea trae `alerta` (`"vencida"`, `"urgente"` o `null`); lista vacía devuelve `[]`; fechas muy pasadas y muy futuras producen `"vencida"` y `null`

### Implementación de la historia de usuario 2

- [X] T023 [US2] Crear `app/plazos.py` con la función pura `calcular_alerta(fecha_entrega, completada, ahora)`: completada → `None`; `fecha_entrega <= ahora` → `"vencida"`; `ahora < fecha_entrega <= ahora + 48 h` → `"urgente"`; en otro caso `None`
- [X] T024 [US2] En `app/modelos.py` añadir el campo calculado `alerta` a `Tarea`, y en `app/rutas.py` cambiar `GET /api/tareas` para ordenar por `fecha_entrega, id` y calcular `alerta` con la hora UTC actual (depende de T023)
- [X] T025 [US2] Interfaz del listado en `app/static/app.js` y `app/static/estilos.css`: etiqueta con texto "Vencida" o "Urgente" (no solo color) y estilo destacado, fecha mostrada con `toLocaleString('es-CO')`, tareas sin marca especial cuando `alerta` es `null` (depende de T024)
- [X] T026 [US2] Actualización automática en `app/static/app.js`: volver a pedir el listado cada 60 segundos y cuando la pestaña recupere el foco (`visibilitychange`), para que las marcas cambien sin intervención del estudiante (FR-016) (depende de T025)

**Punto de control**: las historias 1 y 2 funcionan de forma independiente

---

## Fase 5: Historia de usuario 3 - Completar tareas (Prioridad: P3)

**Meta**: marcar una tarea como completada y poder desmarcarla.

**Prueba independiente**: completar una tarea vencida, comprobar que pierde la marca y que la recupera al desmarcarla.

### Pruebas de la historia de usuario 3 ⚠️

- [X] T027 [P] [US3] Escribir `tests/test_completar.py`: `PATCH /api/tareas/{id}` con `{"completada": true}` responde 200 y la tarea queda completada y con `alerta` `null` aunque esté vencida o urgente; con `false` vuelve a pendiente y recupera su `alerta`; el estado persiste en un nuevo `GET`; `id` inexistente responde 404; cuerpo sin `completada` o con valor no booleano responde 422

### Implementación de la historia de usuario 3

- [X] T028 [US3] Añadir en `app/modelos.py` el modelo `TareaEstado` (`completada`: booleano obligatorio) y en `app/rutas.py` el endpoint `PATCH /api/tareas/{id}` que actualice el estado y devuelva la tarea con su `alerta` recalculada (depende de T024)
- [X] T029 [US3] Interfaz en `app/static/app.js` y `app/static/estilos.css`: casilla o botón con etiqueta accesible para marcar y desmarcar cada tarea con una sola acción, actualización inmediata del listado y estilo visible para las tareas completadas (depende de T028, T025)

**Punto de control**: las historias 1, 2 y 3 funcionan de forma independiente

---

## Fase 6: Historia de usuario 4 - Filtrar por materia y estado (Prioridad: P4)

**Meta**: filtrar el listado por materia, por estado o por ambos.

**Prueba independiente**: con tareas de varias materias y estados, aplicar cada filtro y verificar que solo aparecen las que coinciden.

### Pruebas de la historia de usuario 4 ⚠️

- [X] T030 [P] [US4] Escribir `tests/test_filtros.py`: `GET /api/tareas?materia_id=`, `?estado=pendiente`, `?estado=completada` y la combinación de ambos devuelven solo las coincidentes; `estado` inválido o `materia_id` no numérico responde 422; materia inexistente devuelve `[]`; el orden por fecha se mantiene con filtros

### Implementación de la historia de usuario 4

- [X] T031 [US4] Añadir en `app/rutas.py` los parámetros opcionales `materia_id` (entero) y `estado` (`pendiente` o `completada`) a `GET /api/tareas`, aplicados con parámetros enlazados de SQL (depende de T024)
- [X] T032 [US4] Interfaz de filtros en `app/static/app.js`, `app/static/index.html` y `app/static/estilos.css`: selectores con `<label>` para materia (con opción "Todas") y estado (con opción "Todos"), botón "Quitar filtros" y mensaje de sin resultados; los filtros se conservan al refrescar el listado (depende de T031, T026)

**Punto de control**: las cuatro historias funcionan de forma independiente

---

## Fase 7: Pulido y temas transversales

**Propósito**: mejoras que afectan a varias historias

- [X] T033 [P] Escribir `README.md` en español en la raíz: descripción, instalación con Python 3.12, cómo ejecutar (`uvicorn app.main:crear_app --factory`), cómo probar (`pytest`) y alcance de la versión 1
- [X] T034 [P] Ampliar `tests/test_estaticos.py`: cada `<input>`, `<select>` y `<textarea>` de `index.html` tiene su `<label>`; `app.js` no contiene `innerHTML` (los datos del estudiante solo se escriben con `textContent`)
- [X] T035 Revisar accesibilidad y diseño responsivo en `app/static/estilos.css` y `app/static/index.html`: contraste de los 8 colores y de las etiquetas "Vencida"/"Urgente", uso completo con teclado, foco visible, áreas táctiles cómodas en celular y ausencia de desplazamiento horizontal a 360 px
- [X] T036 Ejecutar `pytest` completo y corregir fallos; comprobar que no queda código ni dependencias fuera de lo que el plan necesita (principio I)
- [X] T037 Ejecutar la validación manual de `specs/001-organizador-tareas/quickstart.md` en una pantalla de escritorio y en una de celular, y anotar los resultados

---

## Dependencias y orden de ejecución

### Dependencias entre fases

- **Preparación (Fase 1)**: sin dependencias; puede empezar de inmediato
- **Fundamentos (Fase 2)**: depende de la Preparación y BLOQUEA todas las historias
- **Historias (Fases 3 a 6)**: dependen de los Fundamentos
  - En orden de prioridad: P1 → P2 → P3 → P4
  - US2 y US3 amplían el listado de US1 (`GET /api/tareas`, `app.js`), por lo que conviene hacerlas en ese orden
  - US4 depende del listado de US2 (T024, T026)
- **Pulido (Fase 7)**: depende de las historias que se vayan a entregar

### Dependencias entre historias

- **US1 (P1)**: puede empezar tras los Fundamentos; no depende de otras historias
- **US2 (P2)**: usa los endpoints y el listado de US1; se prueba de forma independiente con tareas creadas por la API
- **US3 (P3)**: usa el modelo `Tarea` con `alerta` de US2 (T024)
- **US4 (P4)**: usa `GET /api/tareas` de US2 (T024)

### Dentro de cada historia

- Las pruebas se escriben primero y deben fallar antes de implementar
- Modelos → rutas → interfaz
- Terminar la historia antes de pasar a la siguiente prioridad

### Oportunidades de paralelismo

- En la Preparación: T003 y T004
- En los Fundamentos: T006, T010 y T011 (archivos distintos)
- Las pruebas de una misma historia: T013 con T014; T021 con T022
- Las tareas que tocan `app/rutas.py` o `app/static/app.js` NO son paralelas entre sí

---

## Ejemplo de paralelismo: historia de usuario 1

```text
# Lanzar juntas las pruebas de la historia 1:
Tarea: "Escribir tests/test_materias.py" (T013)
Tarea: "Escribir tests/test_tareas.py" (T014)
```

---

## Estrategia de implementación

### Primero el MVP (solo historia 1)

1. Completar la Fase 1: Preparación
2. Completar la Fase 2: Fundamentos (bloquea todo)
3. Completar la Fase 3: historia de usuario 1
4. **DETENERSE y VALIDAR**: probar la historia 1 de forma independiente (`pytest` y el escenario 1 y 2 del quickstart)
5. Demostrar si ya está lista

### Entrega incremental

1. Preparación + Fundamentos → base lista
2. Historia 1 → probar → demostrar (MVP)
3. Historia 2 → probar → demostrar
4. Historia 3 → probar → demostrar
5. Historia 4 → probar → demostrar
6. Cada historia agrega valor sin romper las anteriores

---

## Notas

- [P] = archivos distintos, sin dependencias
- La etiqueta [Historia] relaciona cada tarea con su historia para dar trazabilidad
- Cada historia debe poder completarse y probarse por separado
- Verificar que las pruebas fallen antes de implementar
- Hacer commit después de cada tarea o grupo lógico
- Puntos del checklist `checklists/ux-validacion.md` todavía sin resolver (por ejemplo CHK004 confirmación al borrar, CHK009 presentación de tareas completadas, CHK039 hora del dispositivo frente a un servidor remoto): las tareas siguen la especificación y el plan actuales; ajústelas si se aclaran esos puntos
- Evitar: tareas vagas, conflictos en un mismo archivo y dependencias entre historias que rompan su independencia

---

## Phase 8: Convergence

- [X] T038 CRÍTICA: agregar pruebas automáticas de la interfaz en `tests/test_interfaz.py` (error de validación junto al campo y texto conservado tras un rechazo, avisos de lista vacía, borrado de materia con tareas bloqueado, `<b>` escrito como texto) usando un navegador automatizado dentro de pytest, y registrar la dependencia en `requirements.txt` y en `plan.md`; si el equipo decide no hacerlo, registrar la desviación justificada en el Seguimiento de complejidad de `plan.md` per Constitution II (contradicts)
- [X] T039 Escribir `tests/test_persistencia.py`: crear una materia y una tarea con `crear_app(ruta)`, volver a llamar a `crear_app` con la misma ruta y comprobar que los datos siguen ahí per FR-012 y SC-007 (missing)
- [X] T040 Escribir `tests/test_volumen.py`: crear 200 tareas por la API y comprobar que `GET /api/tareas` y los filtros responden en menos de 1 segundo, y fijar ese umbral en `spec.md` si se aprueba per SC-006 (missing)
- [X] T041 Registrar en `app/errores.py` un manejador de errores inesperados que responda 500 con `{"errores": [{"campo": null, "mensaje": "Ocurrió un error inesperado. Inténtelo de nuevo."}]}` y probarlo en `tests/test_estaticos.py` per FR-014 (partial)
- [X] T042 Refactorizar `validar_fecha_entrega` en `app/modelos.py` para que no dependa del texto del mensaje (`"zona horaria" in str(error)`): separar el análisis de la fecha de la comprobación de zona horaria, manteniendo las pruebas de `tests/test_tareas.py` en verde per Constitution III (partial)
- [X] T043 Actualizar `specs/001-organizador-tareas/data-model.md` y `specs/001-organizador-tareas/research.md` (punto 3) para indicar que la unicidad sin distinguir mayúsculas se verifica con `casefold()` en `app/rutas.py` además de `COLLATE NOCASE` per plan: acceso a datos (partial)
- [X] T044 Decidir si se conserva `specs/001-organizador-tareas/evidencia-us1-360px.png` (captura de verificación manual no solicitada por ninguna tarea): conservarla y citarla en el quickstart, o borrarla per plan: documentación (unrequested)

---

## Phase 9: Convergence

- [ ] T045 [Leonardo] Validar el rango de todos los identificadores numéricos (`materia_id` del cuerpo de `POST /api/tareas` en `app/modelos.py`, y `materia_id`, `materia_id` de la ruta y `tarea_id` en `app/rutas.py`) entre 1 y 9223372036854775807, para que un entero demasiado grande responda 422 en español y no 500; probarlo en `tests/test_tareas.py`, `tests/test_materias.py`, `tests/test_completar.py` y `tests/test_filtros.py` per Constitution IV y FR-004 (partial)
- [ ] T046 [Adrián] Agregar a `tests/test_interfaz.py` una prueba con el reloj de Playwright (`page.clock`) que avance 60 segundos y compruebe que el navegador vuelve a pedir `/api/tareas` sin intervención del estudiante (y otra al volver a mostrarse la pestaña) per FR-016 y Constitution II (missing)
- [ ] T047 [Adrián] Agregar a `tests/test_interfaz.py` una prueba de uso solo con teclado: registrar una materia y crear una tarea con Tab, escritura y Enter, y comprobar que el foco es visible y sigue un orden lógico per FR-015 (partial)
- [ ] T048 [Leonardo] Agregar a `tests/test_tareas.py` casos de fechas extremas con zona horaria (`0001-01-01T00:00:00+05:00` y `9999-12-31T23:59:59-05:00`) que respondan 422 con "La fecha de entrega no es válida." per Constitution IV (missing)
- [ ] T049 [Adrián] Agregar a `tests/test_interfaz.py` dos pruebas: el formulario de tareas conserva lo escrito cuando el servidor rechaza la tarea, y borrar una materia sin tareas la quita de la lista, per SC-004 y US1/AC5 (partial)
- [ ] T050 [Leonardo] Agregar a `tests/test_persistencia.py` una prueba de que `crear_app()` sin argumento usa la ruta de la variable de entorno `TAREAS_DB` per plan: configuración de la base de datos (missing)
- [X] T051 [Adrián] Dividir `crearTarjetaTarea` en `app/static/app.js` en funciones pequeñas (encabezado con etiqueta, datos de la materia, botón de estado) manteniendo verdes las pruebas de `tests/test_interfaz.py` per Constitution III (partial)
- [ ] T052 [Quien termine último] Actualizar `specs/001-organizador-tareas/spec.md`: fijar en SC-006 el umbral de 1 segundo con 200 tareas (el de `tests/test_volumen.py`), añadir a los Supuestos que el servidor corre en el dispositivo del estudiante (decisión sobre FR-008 y FR-013), y anotar en `quickstart.md` el resultado de la validación manual per SC-006 y FR-008 (partial)
