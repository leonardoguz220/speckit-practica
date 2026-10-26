# Investigación (Fase 0): Organizador de tareas académicas

La pila tecnológica la definió el equipo (Python 3.12, FastAPI, SQLite, frontend sin frameworks,
pytest, un solo proyecto). No quedaron marcadores `NEEDS CLARIFICATION` en el contexto técnico;
aquí se documentan las decisiones de diseño que sí había que tomar.

## 1. Dónde se calcula "vencida" y "urgente"

- **Decisión**: se calcula en el backend con una función pura `calcular_alerta(fecha_entrega,
  completada, ahora)` y la API devuelve el campo `alerta` (`"vencida"`, `"urgente"` o `null`) en
  cada tarea.
- **Justificación**: es la regla de negocio más delicada (límites de 48 h) y así se prueba con
  pytest de forma exacta, sin navegador. El frontend solo muestra lo que recibe.
- **Alternativas descartadas**: calcularlo en JavaScript (no se puede probar con pytest y
  duplicaría reglas); guardar la marca en la base de datos (se desactualizaría con el tiempo,
  contradice FR-016).
- **Reglas exactas** (FR-007, FR-008, FR-010): con `ahora` y `limite = ahora + 48 h`:
  - completada → `null`
  - `fecha_entrega <= ahora` → `"vencida"`
  - `ahora < fecha_entrega <= limite` → `"urgente"`
  - `fecha_entrega > limite` → `null`
- **Reloj**: el servidor corre en el dispositivo del estudiante, así que su hora es la "hora del
  dispositivo" de FR-008. Las fechas se comparan como instantes en UTC, por lo que la zona
  horaria no altera el resultado.

## 2. Actualización de las marcas con el paso del tiempo (FR-016)

- **Decisión**: el frontend vuelve a pedir el listado cada 60 segundos y al volver a enfocar la
  pestaña.
- **Justificación**: es lo más simple que cumple FR-016 sin WebSockets ni tareas en segundo plano.
- **Alternativas descartadas**: WebSockets o eventos del servidor (sobreingeniería); calcular el
  paso del tiempo en el navegador (duplica la regla).

## 3. Acceso a datos

- **Decisión**: módulo estándar `sqlite3`, SQL escrito a mano con parámetros, sin ORM ni capa de
  repositorios; una conexión por solicitud.
- **Justificación**: dos tablas y consultas triviales; un ORM añadiría dependencias y conceptos sin
  beneficio (principio I). Los parámetros enlazados evitan inyección SQL (principio IV).
- **Alternativas descartadas**: SQLAlchemy/SQLModel (innecesario a esta escala).
- **Integridad**: `PRAGMA foreign_keys = ON`; nombre de materia único sin distinguir mayúsculas:
  `COLLATE NOCASE` solo ignora mayúsculas ASCII, así que la ruta además compara con `casefold()`
  en Python (así "Álgebra" y "álgebra" se consideran repetidas); la regla de "no borrar materia con tareas" se aplica en la ruta y,
  como respaldo, con la clave foránea sin borrado en cascada.

## 4. Validación y mensajes en español

- **Decisión**: modelos Pydantic definen los límites (materia 50, título 100, descripción 500) y
  validadores propios que recortan espacios y devuelven mensajes en español. Un manejador de
  `RequestValidationError` convierte el error por defecto (en inglés) en un cuerpo uniforme:
  `{"errores": [{"campo": "...", "mensaje": "..."}]}`. Los errores 404 y 409 usan el mismo formato.
- **Justificación**: cumple FR-004 y FR-014 con un único formato que el frontend sabe mostrar junto
  al campo correcto.
- **Alternativas descartadas**: validar a mano en cada ruta (repetitivo y propenso a omisiones).
- **Detalles**: el texto se recorta (`strip`) antes de medir la longitud; un texto de exactamente
  el máximo se acepta; la descripción vacía se guarda como ausente.

## 5. Fecha de entrega

- **Decisión**: el navegador envía la fecha y hora en formato ISO 8601 con zona horaria
  (`new Date(valor).toISOString()`); el servidor la exige con zona, la convierte a UTC y la guarda
  como texto `AAAA-MM-DDTHH:MM:SSZ` (precisión de segundos).
- **Justificación**: un formato único y ordenable como texto permite `ORDER BY fecha_entrega, id`,
  que además cumple "mismas fechas en orden de creación". Exigir zona evita ambigüedades de
  interpretación (FR-008).
- **Alternativas descartadas**: guardar hora local sin zona (ambigua); marca de tiempo numérica
  (menos legible al depurar).
- Se permiten fechas pasadas (caso límite de la especificación).

## 6. Colores de las materias

- **Decisión**: paleta fija de 8 nombres (`rojo`, `naranja`, `amarillo`, `verde`, `turquesa`,
  `azul`, `morado`, `rosa`). La API guarda y valida el nombre; el CSS define el tono de cada uno.
- **Justificación**: cumple el supuesto de "paleta predefinida", permite elegir tonos con
  contraste suficiente y evita validar códigos hexadecimales arbitrarios.
- **Accesibilidad**: el color nunca es el único indicador; cada tarea muestra además el nombre de
  su materia, y "vencida"/"urgente" llevan texto y no solo color.

## 7. Servir el frontend

- **Decisión**: `StaticFiles` de FastAPI montado en `/` con `html=True`, registrado después de las
  rutas `/api` para que no las oculte. Una sola página (`index.html`) con formularios y listado.
- **Justificación**: un solo proceso y un solo comando de arranque, como se pidió.
- **Alternativas descartadas**: servidor de archivos aparte o empaquetador de JavaScript.

## 8. Estrategia de pruebas

- **Decisión**: una función `crear_app(ruta_db)` permite que cada prueba use una base SQLite
  temporal (`tmp_path`) con `TestClient`. La función `calcular_alerta` se prueba de forma
  unitaria con instantes fijos (47 h, 48 h exactas, 48 h y 1 min, hora actual exacta, completada).
- **Cobertura**: validaciones y límites, unicidad sin distinguir mayúsculas, borrado de materia
  (con y sin tareas), orden por fecha y por creación, filtros combinados, cambio de estado y
  archivos estáticos (`lang="es"`, `viewport`, etiquetas en campos).
- **Pruebas de interfaz**: se hacen con `pytest-playwright` (Chromium) dentro de pytest, porque la
  constitución exige pruebas automatizadas de toda funcionalidad. El servidor se levanta en un
  puerto libre con una base temporal. La validación manual de [quickstart.md](quickstart.md) queda
  para lo visual.

## 9. Entorno

- Solo se detectó Python 3.14 en esta máquina; el proyecto exige Python 3.12. Se documenta en
  `quickstart.md` cómo crear el entorno virtual con 3.12 (`py -3.12 -m venv .venv`).
- Las versiones exactas de las dependencias se fijan al generar `requirements.txt` durante la
  implementación.
