<!--
Informe de impacto de sincronización
- Cambio de versión: (plantilla sin completar) → 1.0.0
- Principios modificados: ninguno (constitución inicial)
- Principios añadidos: I. Simplicidad primero; II. Pruebas obligatorias (NO NEGOCIABLE);
  III. Código legible; IV. Validación de entradas; V. Accesible y responsivo
- Secciones añadidas: Restricciones adicionales; Flujo de desarrollo y revisión; Gobernanza
- Secciones eliminadas: ninguna
- Pendientes: ninguno
-->
# Constitución del Proyecto Académico UPB

## Principios fundamentales

### I. Simplicidad primero
Toda funcionalidad MUST resolverse con la solución mínima que funcione. Las
abstracciones, capas, configuraciones y dependencias para necesidades hipotéticas MUST NOT
agregarse (YAGNI). Si se
propone una solución más compleja que la mínima, la complejidad MUST justificarse por escrito en
el plan de la funcionalidad.

Justificación: en un proyecto académico, el código simple es más fácil de entender, probar,
evaluar y mantener dentro de los plazos de entrega.

### II. Pruebas obligatorias (NO NEGOCIABLE)
Toda funcionalidad MUST tener pruebas automatizadas antes de darse por terminada. Una tarea no
se considera completa mientras sus pruebas no existan y pasen. Las correcciones de errores MUST
incluir una prueba de regresión que falle sin la corrección.

Justificación: las pruebas automatizadas son la evidencia verificable de que el sistema cumple lo
especificado y evitan que los cambios posteriores rompan lo ya construido.

### III. Código legible
El código MUST usar nombres claros que expresen su intención. Las funciones MUST ser pequeñas y
tener una sola responsabilidad. Lo que no sea evidente por el código (decisiones, reglas de
negocio, restricciones) MUST documentarse con comentarios o documentación breve; lo obvio no
se comenta.

Justificación: el código se lee mucho más de lo que se escribe, y debe poder ser entendido por
cualquier integrante del equipo y por quien lo evalúe.

### IV. Validación de entradas
Todo dato proveniente del usuario MUST validarse (tipo, formato, rango y obligatoriedad) antes de
procesarse o almacenarse. Las entradas inválidas MUST rechazarse con un mensaje de error claro
en español, sin interrumpir el funcionamiento del sistema. La validación MUST cubrir también los
casos límite con pruebas automatizadas.

Justificación: validar en el punto de entrada evita errores, datos corruptos y vulnerabilidades
comunes.

### V. Accesible y responsivo
La interfaz MUST funcionar correctamente tanto en celular como en computadora, adaptando su
diseño al tamaño de pantalla. La interfaz MUST ser accesible: contraste suficiente, etiquetas en
los campos de formulario, texto alternativo en imágenes y uso con teclado.

Justificación: los usuarios acceden desde dispositivos distintos; una interfaz que no se adapta
o no es accesible excluye usuarios.

## Restricciones adicionales

- Toda la documentación y los documentos del proyecto (especificaciones, planes, tareas,
  README y esta constitución) MUST estar redactados en español.
- Los mensajes mostrados al usuario MUST estar en español.
- Los secretos y credenciales MUST NOT incluirse en el repositorio.
- Las dependencias externas MUST limitarse a las estrictamente necesarias (ver Principio I).

## Flujo de desarrollo y revisión

- Cada cambio MUST verificarse contra los cinco principios antes de considerarse terminado.
- Una funcionalidad MUST tener sus pruebas automatizadas pasando antes de integrarse.
- Las revisiones MUST comprobar: simplicidad de la solución, existencia de pruebas, legibilidad,
  validación de entradas y comportamiento en celular y computadora.
- Toda desviación de un principio MUST quedar justificada y documentada en el plan.

## Gobernanza

Esta constitución prevalece sobre cualquier otra práctica del proyecto. Las enmiendas MUST
documentarse, indicar su motivo y actualizar la versión y la fecha de última enmienda.

Política de versionado (versionado semántico):
- MAYOR: eliminación o redefinición incompatible de principios o de la gobernanza.
- MENOR: nuevo principio o sección, o ampliación sustancial de la guía.
- PARCHE: aclaraciones, correcciones de redacción o ajustes no semánticos.

Revisión de cumplimiento: toda especificación, plan y revisión de código MUST verificar el
cumplimiento de estos principios; la complejidad que se aparte de ellos MUST justificarse.

**Versión**: 1.0.0 | **Ratificada**: 2026-10-26 | **Última enmienda**: 2026-10-26
