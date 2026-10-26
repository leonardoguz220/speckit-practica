# Organizador de tareas académicas

Aplicación web para estudiantes de la UPB que les ayuda a organizar sus tareas: registran sus
materias (nombre y color), crean tareas con fecha de entrega, ven un listado ordenado donde las
tareas vencidas se destacan y las de las próximas 48 horas aparecen como "urgentes", las marcan
como completadas y las filtran por materia o por estado.

Es un proyecto académico de la UPB. La interfaz y los mensajes están en español.

## Alcance de la versión 1

- Un solo usuario por instalación, sin inicio de sesión. El servidor corre en el dispositivo del
  estudiante y los datos se guardan en un archivo local (`datos/tareas.db`).
- Una materia solo se puede borrar si no tiene tareas.
- Fuera de alcance: editar materias, editar o eliminar tareas, recordatorios, notificaciones,
  búsqueda por texto y compartir tareas.

## Requisitos

- Python 3.12
- Un navegador moderno

## Instalación

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

El último comando descarga el navegador que usan las pruebas de interfaz.

## Ejecución

```powershell
uvicorn app.main:crear_app --factory
```

Abrir `http://127.0.0.1:8000/`. La ruta de la base de datos se puede cambiar con la variable de
entorno `TAREAS_DB`.

## Pruebas

```powershell
pytest
```

Incluye pruebas de la API, de las reglas de validación y de los plazos (límite de 48 horas), y
pruebas de la interfaz en un navegador real.

## Estructura

```text
app/            código del servidor (FastAPI) y la interfaz estática (app/static/)
tests/          pruebas con pytest
specs/          especificación, plan y tareas de la funcionalidad (Spec Kit)
```

La guía de validación manual está en `specs/001-organizador-tareas/quickstart.md`.
