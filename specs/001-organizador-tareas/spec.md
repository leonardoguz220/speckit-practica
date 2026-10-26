# Especificación de la funcionalidad: Organizador de tareas académicas

**Rama de la funcionalidad**: `001-organizador-tareas`

**Creada**: 2026-10-26

**Estado**: Borrador

**Entrada**: Descripción del usuario: "Quiero una aplicación para estudiantes de la UPB que les ayude a organizar sus tareas académicas. El estudiante puede registrar sus materias (nombre y color). Puede crear tareas asociadas a una materia, con título, descripción opcional y fecha de entrega. Ve un listado de tareas ordenado por fecha de entrega, donde las tareas vencidas se destacan y las próximas 48 horas aparecen como "urgentes". Puede marcar tareas como completadas y filtrarlas por materia o por estado. En esta primera versión no hay inicio de sesión: es un solo usuario por dispositivo. Todo el contenido de la especificación debe estar en español."

## Aclaraciones

### Sesión 2026-10-26

- Q: ¿Qué debe pasar con las tareas de una materia cuando el estudiante la borra? → R: Solo se puede borrar una materia que no tenga tareas; si las tiene, el sistema lo impide y explica el motivo.
- Q: ¿Cuál es la longitud máxima permitida para el título de la tarea, el nombre de la materia y la descripción? → R: Materia: 50 caracteres; título: 100; descripción: 500.
- Q: ¿Cómo se calcula "urgente": ventana móvil de 48 horas o días calendario? → R: Ventana móvil de 48 horas exactas desde la hora actual: urgente si la entrega es en las próximas 48 horas (incluida exactamente 48 h) y aún no ha vencido.

## Escenarios de usuario y pruebas *(obligatorio)*

### Historia de usuario 1 - Registrar materias y crear tareas (Prioridad: P1)

El estudiante registra las materias que cursa, indicando un nombre y un color, y luego crea tareas
asociadas a una de esas materias, con título, descripción opcional y fecha de entrega.

**Por qué esta prioridad**: sin materias y tareas no existe nada que organizar. Es la base de todo
el resto y, por sí sola, ya permite al estudiante dejar registradas sus obligaciones.

**Prueba independiente**: se puede probar registrando una materia y creando una tarea asociada a
ella; la tarea debe aparecer guardada con sus datos y con el color de su materia.

**Escenarios de aceptación**:

1. **Dado** que el estudiante no tiene materias, **cuando** registra la materia "Cálculo" con el
   color azul, **entonces** la materia queda guardada y disponible para asociar tareas.
2. **Dado** que existe la materia "Cálculo", **cuando** crea una tarea con título "Taller 3", sin
   descripción y con una fecha de entrega futura, **entonces** la tarea queda guardada asociada a
   "Cálculo".
3. **Dado** que el estudiante intenta crear una tarea sin título, sin materia o sin fecha de
   entrega, **cuando** envía el formulario, **entonces** el sistema no la guarda y muestra un
   mensaje claro indicando qué dato falta.
4. **Dado** que el estudiante intenta registrar una materia sin nombre o con un nombre ya
   existente, **cuando** la envía, **entonces** el sistema no la guarda y explica el motivo.
5. **Dado** que existe una materia sin tareas, **cuando** el estudiante la borra, **entonces** la
   materia desaparece y ya no está disponible para asociar tareas.
6. **Dado** que existe una materia con una o más tareas (pendientes o completadas), **cuando** el
   estudiante intenta borrarla, **entonces** el sistema no la borra, conserva sus tareas y le
   explica que debe vaciarla de tareas antes.

---

### Historia de usuario 2 - Ver el listado de tareas con vencidas y urgentes (Prioridad: P2)

El estudiante ve todas sus tareas en un listado ordenado por fecha de entrega, de la más próxima a
la más lejana. Las tareas vencidas se destacan visualmente y las que vencen dentro de las próximas
48 horas se marcan como "urgentes".

**Por qué esta prioridad**: es el valor central de la aplicación: saber de un vistazo qué hay que
entregar y qué es más apremiante.

**Prueba independiente**: se puede probar con tareas de fechas pasadas, cercanas y lejanas, y
verificar el orden y las marcas "vencida" y "urgente".

**Escenarios de aceptación**:

1. **Dado** que existen tareas con distintas fechas de entrega, **cuando** el estudiante abre el
   listado, **entonces** las ve ordenadas de la fecha de entrega más próxima a la más lejana.
2. **Dado** que una tarea pendiente tiene una fecha de entrega ya pasada, **cuando** el estudiante
   ve el listado, **entonces** esa tarea aparece destacada como vencida.
3. **Dado** que una tarea pendiente vence dentro de las próximas 48 horas, **cuando** el estudiante
   ve el listado, **entonces** la tarea aparece marcada como "urgente".
4. **Dado** que una tarea pendiente vence en más de 48 horas, **cuando** el estudiante ve el
   listado, **entonces** la tarea aparece sin marca especial.
5. **Dado** que no hay tareas registradas, **cuando** el estudiante abre el listado, **entonces**
   ve un mensaje que lo invita a crear su primera tarea.

---

### Historia de usuario 3 - Completar tareas (Prioridad: P3)

El estudiante marca una tarea como completada cuando la entrega, y puede desmarcarla si se
equivocó.

**Por qué esta prioridad**: permite mantener el listado limpio y distinguir lo hecho de lo
pendiente, pero depende de que ya existan tareas.

**Prueba independiente**: se puede probar marcando una tarea como completada y verificando que su
estado cambia y que deja de mostrarse como vencida o urgente.

**Escenarios de aceptación**:

1. **Dado** que una tarea está pendiente, **cuando** el estudiante la marca como completada,
   **entonces** su estado cambia a completada y se conserva al volver a abrir la aplicación.
2. **Dado** que una tarea vencida o urgente se marca como completada, **cuando** el estudiante ve
   el listado, **entonces** ya no aparece destacada como vencida ni como urgente.
3. **Dado** que una tarea está completada, **cuando** el estudiante la desmarca, **entonces**
   vuelve a estar pendiente y recupera su marca de vencida o urgente si le corresponde.

---

### Historia de usuario 4 - Filtrar tareas por materia y por estado (Prioridad: P4)

El estudiante filtra el listado por materia, por estado (pendientes o completadas), o por ambos
criterios a la vez.

**Por qué esta prioridad**: mejora la comodidad cuando hay muchas tareas, pero el listado ya es
útil sin filtros.

**Prueba independiente**: se puede probar con tareas de varias materias y estados, aplicando cada
filtro y verificando que solo se muestran las tareas que coinciden.

**Escenarios de aceptación**:

1. **Dado** que existen tareas de varias materias, **cuando** el estudiante filtra por "Cálculo",
   **entonces** solo ve las tareas de esa materia.
2. **Dado** que existen tareas pendientes y completadas, **cuando** el estudiante filtra por
   "completadas", **entonces** solo ve las completadas.
3. **Dado** que se aplican filtro de materia y de estado a la vez, **cuando** el estudiante ve el
   listado, **entonces** solo aparecen las tareas que cumplen ambos criterios.
4. **Dado** que ninguna tarea cumple los filtros, **cuando** el estudiante los aplica, **entonces**
   ve un mensaje indicando que no hay resultados y puede quitar los filtros fácilmente.

---

### Casos límite

- ¿Qué pasa si el estudiante intenta crear una tarea y aún no tiene ninguna materia? El sistema le
  indica que primero debe registrar una materia y le facilita hacerlo.
- ¿Qué pasa si el título, el nombre de la materia o la descripción tienen solo espacios o superan
  la longitud máxima (50, 100 y 500 caracteres, respectivamente)? El sistema los rechaza con un
  mensaje claro. Un texto de exactamente la longitud máxima se acepta.
- ¿Qué pasa si la fecha de entrega de una tarea nueva ya pasó? El sistema permite guardarla (por
  ejemplo, para registrar una tarea atrasada) y la muestra como vencida.
- ¿Qué pasa con una tarea que vence exactamente en 48 horas? Se considera urgente. Una que vence
  en 48 horas y un minuto todavía no lo es, y pasa a serlo cuando falten 48 horas o menos.
- ¿Qué pasa con una tarea cuya hora de entrega es exactamente la hora actual? Se considera
  vencida, no urgente.
- ¿Qué pasa si dos tareas tienen la misma fecha de entrega? Se muestran juntas, en el orden en que
  fueron creadas.
- ¿Qué pasa si el estudiante cierra y vuelve a abrir la aplicación? Sus materias y tareas se
  conservan en el mismo dispositivo.
- ¿Qué pasa en una pantalla pequeña de celular con muchas tareas? El listado y los formularios
  siguen siendo legibles y utilizables sin desplazamiento horizontal.

## Requisitos *(obligatorio)*

### Requisitos funcionales

- **FR-001**: El sistema DEBE permitir registrar una materia con un nombre y un color.
- **FR-002**: El sistema DEBE rechazar materias sin nombre, con nombre vacío o de solo espacios,
  de más de 50 caracteres, o repetido (sin distinguir mayúsculas), mostrando un mensaje claro en
  español.
- **FR-003**: El sistema DEBE permitir crear una tarea asociada a una materia existente, con título
  obligatorio (máximo 100 caracteres), descripción opcional (máximo 500 caracteres) y fecha de
  entrega obligatoria.
- **FR-004**: El sistema DEBE validar todos los datos ingresados por el estudiante antes de
  guardarlos y rechazar los inválidos con un mensaje que indique qué corregir.
- **FR-005**: El sistema DEBE mostrar las tareas en un listado ordenado por fecha de entrega, de la
  más próxima a la más lejana.
- **FR-006**: El sistema DEBE mostrar en cada tarea el título, la fecha de entrega, el estado y el
  nombre y color de su materia.
- **FR-007**: El sistema DEBE destacar visualmente las tareas pendientes cuya fecha de entrega ya
  pasó, indicándolas como "vencidas".
- **FR-008**: El sistema DEBE marcar como "urgentes" las tareas pendientes cuya fecha y hora de
  entrega estén entre el momento actual (excluido) y 48 horas exactas después (incluido), medido
  con la hora actual del dispositivo y no por días calendario.
- **FR-009**: El sistema DEBE permitir marcar una tarea como completada y volver a marcarla como
  pendiente.
- **FR-010**: Las tareas completadas NO DEBEN mostrarse como vencidas ni como urgentes.
- **FR-011**: El sistema DEBE permitir filtrar el listado por materia, por estado (pendiente o
  completada) o por ambos criterios combinados, y permitir quitar los filtros.
- **FR-012**: El sistema DEBE conservar las materias y tareas del estudiante entre sesiones de uso
  en el mismo dispositivo.
- **FR-013**: El sistema NO DEBE requerir inicio de sesión; cada dispositivo maneja los datos de un
  único usuario.
- **FR-014**: Toda la interfaz y todos los mensajes del sistema DEBEN estar en español.
- **FR-015**: La interfaz DEBE ser utilizable tanto en celular como en computadora, y accesible
  (contraste suficiente, campos con etiquetas y uso con teclado).
- **FR-016**: El sistema DEBE actualizar las marcas de "vencida" y "urgente" según la hora actual,
  sin que el estudiante tenga que modificar la tarea.
- **FR-017**: El sistema DEBE permitir borrar una materia únicamente cuando no tiene tareas
  asociadas; si las tiene, DEBE impedir el borrado, conservar las tareas y explicar el motivo.

### Entidades clave *(incluir si la funcionalidad involucra datos)*

- **Materia**: asignatura que cursa el estudiante. Atributos: nombre (único) y color. Una materia
  puede tener muchas tareas y solo puede borrarse cuando no tiene ninguna.
- **Tarea**: obligación académica del estudiante. Atributos: título, descripción (opcional), fecha
  de entrega, estado (pendiente o completada) y la materia a la que pertenece. Cada tarea pertenece
  a exactamente una materia.

## Criterios de éxito *(obligatorio)*

### Resultados medibles

- **SC-001**: Un estudiante nuevo puede registrar una materia y crear su primera tarea en menos de
  2 minutos, sin ayuda.
- **SC-002**: Un estudiante identifica cuáles de sus tareas están vencidas y cuáles son urgentes con
  solo abrir el listado, sin realizar ninguna acción adicional.
- **SC-003**: Marcar una tarea como completada toma una sola acción y el cambio se refleja de
  inmediato en el listado.
- **SC-004**: El 100 % de los datos inválidos (campos vacíos, textos demasiado largos o repetidos)
  se rechaza con un mensaje claro, sin perder lo que el estudiante ya había escrito.
- **SC-005**: Todas las funciones principales (registrar materias, crear tareas, ver el listado,
  completar y filtrar) se pueden usar sin problemas en una pantalla de celular y en una de
  computadora.
- **SC-006**: Con hasta 200 tareas registradas, el listado y los filtros responden de forma
  inmediata, sin esperas perceptibles.
- **SC-007**: Los datos del estudiante siguen disponibles después de cerrar y volver a abrir la
  aplicación en el mismo dispositivo.

## Supuestos

- Los usuarios objetivo son estudiantes de la UPB que usan la aplicación desde su propio celular o
  computadora; la interfaz es solo en español.
- Cada dispositivo guarda sus propios datos; no hay sincronización entre dispositivos ni cuentas en
  esta primera versión, y cambiar de dispositivo implica empezar con datos vacíos.
- La fecha de entrega incluye fecha y hora, porque la regla de "próximas 48 horas" requiere
  precisión horaria; se interpreta según la zona horaria del dispositivo.
- El color de una materia se elige de una paleta predefinida de colores.
- Una tarea vencida es una tarea pendiente cuya fecha y hora de entrega ya pasaron; una tarea
  urgente es una tarea pendiente cuya entrega ocurre en las próximas 48 horas (ventana móvil
  desde la hora actual) y aún no ha vencido.
- Por simplicidad, en esta primera versión quedan fuera de alcance: editar materias, editar o
  eliminar tareas, recordatorios o notificaciones, tareas repetitivas, archivos adjuntos, búsqueda por texto
  y compartir tareas con otras personas.
- Se asume un uso individual con un volumen moderado de datos (decenas de materias y hasta unos
  cientos de tareas).
