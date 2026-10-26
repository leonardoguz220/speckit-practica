# Cómo trabajar en equipo en este repositorio

Este documento explica cómo repartir el trabajo para que no haya conflictos. Léanlo antes de
empezar.

## Reglas básicas

1. **Nadie sube directo a `main`.** Cada tarea va en su propia rama y se une con una solicitud de
   cambios (PR) que revisa la otra persona.
2. **Una persona por archivo.** Las tareas que editan el mismo archivo las hace la misma persona
   (ver el reparto más abajo).
3. **El PR solo se une si `pytest` pasa completo.**
4. **Se marca como hecha (`[X]`) solo la propia tarea**, en el mismo PR donde se termina.

## Reparto de las tareas pendientes (Fase 9 de `specs/001-organizador-tareas/tasks.md`)

| Responsable | Tareas | Archivos que toca |
|-------------|--------|-------------------|
| Leonardo (backend) | T045, T048, T050 | `app/modelos.py`, `app/rutas.py`, `tests/test_tareas.py`, `tests/test_materias.py`, `tests/test_completar.py`, `tests/test_filtros.py`, `tests/test_persistencia.py` |
| Adrián (interfaz) | T046, T047, T049, T051 | `tests/test_interfaz.py`, `app/static/app.js` |
| La última persona en terminar | T052 | `specs/001-organizador-tareas/spec.md`, `specs/001-organizador-tareas/quickstart.md` |

Cada línea de `tasks.md` lleva el nombre del responsable entre corchetes, por ejemplo
`T045 [Leonardo]`. Si hay que cambiar el reparto, cámbienlo ahí y avísense antes de empezar.

## Preparación del entorno

```powershell
git clone https://github.com/leonardoguz220/speckit-practica.git
cd speckit-practica
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
pytest
```

## Flujo de trabajo para cada tarea

```powershell
git switch main
git pull origin main
git switch -c tarea/T045-validar-ids        # nombre: tarea/T###-descripcion-corta

# ...trabajar y probar con pytest...

git add -A
git commit -m "feat: T045 validar rango de identificadores"
git pull --rebase origin main               # traer lo nuevo ANTES de abrir el PR
pytest                                      # debe pasar completo
git push -u origin tarea/T045-validar-ids
```

Después se abre el PR en GitHub hacia `main`. La otra persona lo revisa y lo aprueba. Al unirlo,
ambos hacen `git switch main` y `git pull origin main`.

## Si hay un conflicto

- **Conflicto en `tasks.md`** (lo más común, porque ambos marcan tareas): conserven las dos
  líneas, cada una con su `[X]`, y borren las marcas `<<<<<<<`, `=======` y `>>>>>>>`.
- **Conflicto en otro archivo**: no lo resuelvan a ciegas; hablen primero, porque probablemente
  dos tareas tocaron el mismo archivo y habrá que decidir quién conserva qué.
- Tras resolver: `git add <archivo>`, `git rebase --continue` y volver a correr `pytest`.

## Recomendaciones

- Hagan commits pequeños y frecuentes, y traigan los cambios del otro (`git pull --rebase origin
  main`) al menos una vez al día.
- Sigan la constitución del proyecto (`.specify/memory/constitution.md`): solución simple, pruebas
  obligatorias, código legible, entradas validadas e interfaz accesible y responsiva.
- Todo el contenido (código, mensajes y documentos) se escribe en español.
