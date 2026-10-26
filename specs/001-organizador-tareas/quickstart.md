# Guía de validación rápida: Organizador de tareas académicas

Pasos para ejecutar la aplicación y comprobar de punta a punta que funciona. Detalles de la API en
[contracts/api-rest.md](contracts/api-rest.md) y reglas de datos en [data-model.md](data-model.md).

## Requisitos previos

- Python 3.12 (por ejemplo, `winget install Python.Python.3.12`).
- Un navegador moderno (para la validación manual en celular y computadora).

## Preparación

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Pruebas automatizadas

```powershell
pytest
```

**Resultado esperado**: todas las pruebas pasan (materias, tareas, plazos de 48 h, filtros,
persistencia, volumen de 200 tareas, archivos estáticos y pruebas de interfaz en un navegador real).

## Ejecución

```powershell
uvicorn app.main:crear_app --factory --reload
```

Abrir `http://127.0.0.1:8000/`. El servidor corre en el mismo dispositivo que usa el estudiante
(un usuario por instalación). Para probar el diseño de celular, reduzca el ancho de la ventana del
navegador a unos 360 px o use el modo de dispositivos de sus herramientas de desarrollo.

## Escenarios de validación manual

1. **Materias y tareas (historia 1)**: registrar la materia "Cálculo" en azul; crear la tarea
   "Taller 3" con fecha futura. *Esperado*: aparece en el listado con el color de la materia.
2. **Validaciones**: intentar guardar una materia vacía, repetida ("cálculo") o de más de 50
   caracteres; una tarea sin título, con título de más de 100 caracteres o sin fecha.
   *Esperado*: mensaje claro en español junto al campo y el texto escrito no se pierde.
3. **Borrado de materia**: borrar una materia sin tareas (desaparece) y otra con tareas.
   *Esperado*: la segunda no se borra y se explica el motivo.
4. **Vencidas y urgentes (historia 2)**: crear tareas con entrega en el pasado, dentro de 24 h y
   dentro de 5 días. *Esperado*: orden por fecha; la primera "vencida", la segunda "urgente", la
   tercera sin marca; al pasar el tiempo las marcas se actualizan solas (hasta 1 minuto).
5. **Completar (historia 3)**: marcar una tarea vencida como completada y luego desmarcarla.
   *Esperado*: al completarla pierde la marca; al desmarcarla la recupera.
6. **Filtros (historia 4)**: filtrar por materia, por estado y por ambos; quitar los filtros.
   *Esperado*: solo se ven las tareas que coinciden; sin resultados aparece un mensaje.
7. **Persistencia**: cerrar el servidor, volver a iniciarlo y recargar. *Esperado*: los datos
   siguen ahí.
8. **Celular y computadora**: abrir en una pantalla de unos 360 px y en una de escritorio.
   *Esperado*: sin desplazamiento horizontal, formularios y listado utilizables; navegar y enviar
   formularios solo con el teclado; "vencida" y "urgente" se distinguen sin depender del color.
