# Checklist de experiencia de usuario y validación de datos: Organizador de tareas académicas

**Propósito**: comprobar la calidad de los requisitos de experiencia de usuario (interacción, estados, accesibilidad, diseño responsivo) y de validación de datos (reglas, límites, mensajes), antes de pasar a las tareas
**Creada**: 2026-10-26
**Funcionalidad**: [spec.md](../spec.md) | [plan.md](../plan.md) | [contrato de la API](../contracts/api-rest.md)

**Nota**: este checklist lo genera el comando `/speckit-checklist` a partir del contexto y los requisitos de la funcionalidad. Evalúa la calidad de lo que está escrito, no el comportamiento del software.
**Responsable de la revisión**: es un artefacto de revisión de calidad de requisitos que pertenece a quien revisa. Marque un elemento con `[x]` solo cuando determine que el criterio de calidad del requisito se cumple.
**Significado de las marcas**: `[x]` significa que el criterio se revisó y se cumple en cuanto a calidad del requisito. No significa que el trabajo de implementación esté terminado.

## Estados de la interfaz y retroalimentación

- [ ] CHK001 ¿Están definidos los requisitos para el estado de carga del listado y de los formularios mientras se espera la respuesta del servidor? [Completitud, Brecha]
- [ ] CHK002 ¿Se especifica qué ve el estudiante cuando el servidor no responde o falla (error de red o error interno) y cómo puede reintentar sin perder lo escrito? [Cobertura, Flujo de excepción, Brecha]
- [ ] CHK003 ¿Se define la confirmación visible tras una acción exitosa (materia creada, tarea creada, tarea completada, materia borrada)? [Completitud, Brecha]
- [ ] CHK004 ¿Se define si el borrado de una materia pide confirmación antes de ejecutarse, dado que no hay forma de recuperarla? [Completitud, Spec §FR-017]
- [ ] CHK005 ¿Están definidos los estados vacíos de todas las vistas, incluidas la ausencia de materias (el selector al crear una tarea) y la ausencia de resultados con filtros? [Cobertura, Spec §Historias 2 y 4]
- [ ] CHK006 ¿Se evita la ambigüedad sobre el envío duplicado de un formulario (doble toque o doble clic) con un requisito explícito? [Caso límite, Brecha]

## Presentación del listado

- [ ] CHK007 ¿Está cuantificado o descrito de forma verificable qué significa "destacar visualmente" una tarea vencida? [Claridad, Medibilidad, Spec §FR-007]
- [ ] CHK008 ¿Se exige que "vencida" y "urgente" se distingan entre sí y de una tarea normal sin depender solo del color? [Cobertura, Spec §FR-007, §FR-008, §FR-015]
- [ ] CHK009 ¿Se especifica cómo se presentan las tareas completadas (visibles por defecto, atenuadas, al final) y su posición en el orden por fecha? [Ambigüedad, Spec §FR-005, §FR-009]
- [ ] CHK010 ¿Está definido el formato de presentación de la fecha y la hora de entrega (idioma, 12 o 24 horas, fecha relativa o absoluta)? [Claridad, Spec §FR-006]
- [ ] CHK011 ¿Se define qué se muestra de la descripción en el listado (completa, recortada, oculta) cuando tiene hasta 500 caracteres? [Brecha, Spec §FR-006]
- [ ] CHK012 ¿Se define cómo se muestran los textos largos (hasta 50 y 100 caracteres sin espacios) para que no rompan el diseño en pantallas pequeñas? [Caso límite, Spec §Casos límite]
- [ ] CHK013 ¿La paleta de colores de las materias está definida en la especificación (cuántos y cuáles), y no solo en el plan? [Consistencia, Spec §Supuestos, Plan §Investigación 6]

## Filtros e interacción

- [ ] CHK014 ¿Se define el estado inicial de los filtros (todas las materias, todos los estados) y si se conservan al recargar o tras crear una tarea? [Claridad, Spec §FR-011]
- [ ] CHK015 ¿Está definido el comportamiento del filtro por estado cuando "todas" es una opción, además de "pendiente" y "completada"? [Completitud, Spec §FR-011]
- [ ] CHK016 ¿Se define qué ocurre con un filtro de materia activo si esa materia se borra? [Caso límite, Spec §FR-017]
- [ ] CHK017 ¿Se define el límite de tiempo en que las marcas de "vencida" y "urgente" deben actualizarse sin intervención del estudiante? [Medibilidad, Spec §FR-016]

## Diseño responsivo y accesibilidad

- [ ] CHK018 ¿Están cuantificados los tamaños de pantalla que deben soportarse (ancho mínimo en celular, rangos de escritorio) en lugar de "celular y computadora"? [Claridad, Spec §FR-015]
- [ ] CHK019 ¿Se define un tamaño mínimo de las áreas táctiles para las acciones principales en celular? [Brecha, Spec §FR-015]
- [ ] CHK020 ¿Está definido el criterio de "contraste suficiente" con una referencia medible (por ejemplo, un nivel de las pautas WCAG)? [Medibilidad, Spec §FR-015]
- [ ] CHK021 ¿Se especifica cómo se comunican los errores de validación y los cambios de estado a lectores de pantalla y a quien navega con teclado (foco, anuncios)? [Cobertura, Brecha, Spec §FR-015]
- [ ] CHK022 ¿Se define el orden de navegación con teclado y el manejo del foco tras enviar un formulario o marcar una tarea? [Completitud, Spec §FR-015]
- [ ] CHK023 ¿Están definidos los criterios de aceptación de "sin desplazamiento horizontal" de forma verificable? [Medibilidad, Spec §Casos límite]

## Reglas de validación de datos

- [ ] CHK024 ¿Se especifica si los espacios al inicio y al final se recortan antes de validar y de medir la longitud, y no solo que se rechacen textos "de solo espacios"? [Claridad, Spec §FR-002, Plan §Investigación 4]
- [ ] CHK025 ¿Se define en qué unidad se cuenta la longitud máxima (caracteres visibles, puntos de código, bytes) para casos con tildes, eñes o emojis? [Ambigüedad, Spec §FR-002, §FR-003]
- [ ] CHK026 ¿La regla de nombre de materia "repetido, sin distinguir mayúsculas" aclara si también ignora las tildes (por ejemplo, "Cálculo" y "Calculo")? [Ambigüedad, Spec §FR-002]
- [ ] CHK027 ¿Es consistente el requisito de unicidad sin distinguir mayúsculas con la solución elegida, dado que la comparación de SQLite sin distinguir mayúsculas solo abarca letras ASCII (por ejemplo, "Álgebra" y "álgebra")? [Conflicto, Spec §FR-002, Plan §Investigación 3]
- [ ] CHK028 ¿Está especificado si el título y el nombre admiten saltos de línea o caracteres de control, y cómo se tratan en la descripción de varias líneas? [Brecha, Spec §FR-003]
- [ ] CHK029 ¿Existe un requisito explícito sobre cómo se trata contenido con formato de código o marcado (por ejemplo, `<script>`) escrito por el estudiante, de modo que se muestre como texto? [Brecha, Seguridad, Spec §FR-004]
- [ ] CHK030 ¿Se definen límites (mínimo y máximo) para la fecha de entrega, además de que "se acepta una fecha pasada" (por ejemplo, años lejanos o fechas imposibles)? [Caso límite, Brecha, Spec §Casos límite]
- [ ] CHK031 ¿Se especifica qué precisión tiene la fecha de entrega (minutos o segundos) y cómo se redondean los valores ingresados? [Claridad, Spec §Supuestos]
- [ ] CHK032 ¿FR-004 ("todos los datos ingresados") enumera cuáles son esos datos, incluidos los parámetros de filtro y la selección de materia y color? [Completitud, Spec §FR-004]
- [ ] CHK033 ¿Hay un límite máximo de materias y de tareas, o se declara explícitamente que no existe, dado que solo se mencionan "decenas" y "cientos"? [Brecha, Spec §Supuestos]

## Mensajes de error

- [ ] CHK034 ¿Se define dónde aparece cada mensaje de validación (junto al campo, resumen al inicio o ambos) y si se muestran todos los errores a la vez? [Claridad, Spec §Historia 1, escenario 3]
- [ ] CHK035 ¿Está definido el contenido de los mensajes ("indica qué corregir") con criterios verificables o un catálogo de textos para los casos principales? [Medibilidad, Spec §FR-004]
- [ ] CHK036 ¿El requisito de no perder lo escrito (SC-004) cubre también el caso de rechazo por parte del servidor, y no solo la validación en el navegador? [Cobertura, Spec §SC-004]
- [ ] CHK037 ¿Se define el mensaje y el comportamiento cuando la materia elegida se borra o deja de existir antes de enviar la tarea? [Caso límite, Flujo de excepción, Spec §FR-003, §FR-017]

## Criterios de aceptación y consistencia entre documentos

- [ ] CHK038 ¿Están cuantificados criterios vagos como "responden de forma inmediata" (SC-006) y "sin problemas" (SC-005) con umbrales verificables? [Medibilidad, Spec §SC-005, §SC-006]
- [ ] CHK039 ¿Se concilia "la hora actual del dispositivo" (FR-008) con la posibilidad, descrita en la guía rápida, de abrir la aplicación desde un celular conectado a un servidor que corre en otro computador? [Conflicto, Spec §FR-008, §FR-013, Quickstart]
- [ ] CHK040 ¿Es consistente el supuesto de "un solo usuario por dispositivo" con el uso desde varios dispositivos hacia un mismo servidor, y está documentada la consecuencia para los datos? [Consistencia, Spec §FR-013, §Supuestos]
- [ ] CHK041 ¿Los criterios de aceptación de las historias 1 a 4 cubren los límites exactos de longitud (50, 100 y 500 caracteres) y de tiempo (exactamente 48 horas), y no solo los casos generales? [Cobertura, Spec §Casos límite]

## Notas

- Marque los elementos con `[x]` solo después de que la revisión confirme que el criterio de calidad del requisito se cumple
- Deje sin marcar los elementos que aún necesitan aclaración, corrección o evaluación por parte de quien revisa
- `/speckit-implement` lee el estado de las casillas como una puerta de control y no debe modificar las marcas
- `checklists/requirements.md` tiene un ciclo de vida propio, mantenido por `/speckit-specify` y `/speckit-clarify`
- Agregue comentarios o hallazgos en línea
- Los elementos CHK013, CHK026, CHK027, CHK039 y CHK040 señalan posibles conflictos o ambigüedades entre la especificación y el plan; conviene resolverlos con `/speckit-clarify` antes de generar las tareas
- Los elementos están numerados de forma consecutiva para facilitar su referencia
