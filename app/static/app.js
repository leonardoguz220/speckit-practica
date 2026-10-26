"use strict";

// Convención de los formularios: cada campo tiene un <p class="error" data-error-para="nombre_del_campo"
// aria-live="polite"> y el formulario puede tener uno general con data-error-general.
// Todo texto del estudiante se escribe con textContent, para que nunca se interprete como HTML.

/**
 * Llama a la API y devuelve { ok, datos } o { ok: false, errores } con el formato
 * {"errores": [{"campo", "mensaje"}]} (también cuando el servidor no responde).
 */
async function pedirApi(metodo, ruta, cuerpo) {
  const opciones = { method: metodo, headers: {} };
  if (cuerpo !== undefined) {
    opciones.headers["Content-Type"] = "application/json";
    opciones.body = JSON.stringify(cuerpo);
  }

  let respuesta;
  try {
    respuesta = await fetch(ruta, opciones);
  } catch (error) {
    return {
      ok: false,
      errores: [{ campo: null, mensaje: "No se pudo conectar con el servidor. Inténtelo de nuevo." }],
    };
  }

  if (respuesta.status === 204) {
    return { ok: true, datos: null };
  }

  let datos = null;
  try {
    datos = await respuesta.json();
  } catch (error) {
    // Respuesta sin JSON: se trata más abajo como error inesperado.
  }

  if (respuesta.ok) {
    return { ok: true, datos };
  }
  const errores =
    datos && Array.isArray(datos.errores)
      ? datos.errores
      : [{ campo: null, mensaje: "Ocurrió un error inesperado. Inténtelo de nuevo." }];
  return { ok: false, errores };
}

/** Borra los mensajes de error previos de un formulario. */
function limpiarErrores(formulario) {
  formulario.querySelectorAll("[data-error-para], [data-error-general]").forEach((elemento) => {
    elemento.textContent = "";
  });
  formulario.querySelectorAll("[aria-invalid]").forEach((campo) => {
    campo.removeAttribute("aria-invalid");
  });
}

/** Muestra cada error junto a su campo; los que no tienen campo van al mensaje general. */
function mostrarErrores(formulario, errores) {
  limpiarErrores(formulario);
  const general = formulario.querySelector("[data-error-general]");

  errores.forEach((error) => {
    const contenedor = error.campo
      ? formulario.querySelector(`[data-error-para="${CSS.escape(error.campo)}"]`)
      : null;
    const destino = contenedor || general;
    if (destino) {
      destino.textContent = destino.textContent
        ? `${destino.textContent} ${error.mensaje}`
        : error.mensaje;
    }
    const campo = error.campo && formulario.elements ? formulario.elements[error.campo] : null;
    if (campo) {
      campo.setAttribute("aria-invalid", "true");
    }
  });
}

/** Muestra un mensaje de éxito en la región `data-mensaje-exito` del formulario. */
function mostrarExito(formulario, texto) {
  formulario.querySelector("[data-mensaje-exito]").textContent = texto;
}

function ocultarExito(formulario) {
  formulario.querySelector("[data-mensaje-exito]").textContent = "";
}

// ---------------------------------------------------------------------------
// Materias y tareas
// ---------------------------------------------------------------------------

const COLORES = [
  ["rojo", "Rojo"],
  ["naranja", "Naranja"],
  ["amarillo", "Amarillo"],
  ["verde", "Verde"],
  ["turquesa", "Turquesa"],
  ["azul", "Azul"],
  ["morado", "Morado"],
  ["rosa", "Rosa"],
];

const formMateria = document.getElementById("form-materia");
const formTarea = document.getElementById("form-tarea");
const selectColor = document.getElementById("materia-color");
const selectMateriaTarea = document.getElementById("tarea-materia");
const selectFiltroMateria = document.getElementById("filtro-materia");
const selectFiltroEstado = document.getElementById("filtro-estado");
const errorListado = document.getElementById("error-listado");
const listaMaterias = document.getElementById("lista-materias");
const listaTareas = document.getElementById("lista-tareas");
const errorBorrado = document.getElementById("error-borrado");

/** Crea un elemento con texto (siempre con textContent) y clases opcionales. */
function crearElemento(etiqueta, texto, clases) {
  const elemento = document.createElement(etiqueta);
  if (texto !== undefined) {
    elemento.textContent = texto;
  }
  if (clases) {
    elemento.className = clases;
  }
  return elemento;
}

function crearOpcion(valor, texto) {
  const opcion = crearElemento("option", texto);
  opcion.value = valor;
  return opcion;
}

function crearMuestraDeColor(color) {
  const muestra = crearElemento("span", undefined, `muestra color-${color}`);
  muestra.setAttribute("aria-hidden", "true");
  return muestra;
}

function formatearFecha(fechaIso) {
  return new Date(fechaIso).toLocaleString("es-CO", { dateStyle: "medium", timeStyle: "short" });
}

function llenarSelectorDeColores() {
  selectColor.replaceChildren(crearOpcion("", "Elija un color"));
  COLORES.forEach(([valor, nombre]) => selectColor.append(crearOpcion(valor, nombre)));
}

/** Llena un selector con las materias y conserva la selección si esa materia sigue existiendo. */
function llenarSelectorDeMaterias(selector, textoInicial, materias) {
  const seleccionada = selector.value;
  selector.replaceChildren(crearOpcion("", textoInicial));
  materias.forEach((materia) => selector.append(crearOpcion(materia.id, materia.nombre)));
  selector.value = materias.some((m) => String(m.id) === seleccionada) ? seleccionada : "";
}

// --- Materias ---------------------------------------------------------------

function crearItemMateria(materia) {
  const item = crearElemento("li", undefined, "item-materia");
  item.append(crearMuestraDeColor(materia.color), crearElemento("span", materia.nombre, "nombre-materia"));

  const boton = crearElemento("button", "Borrar", "secundario");
  boton.type = "button";
  boton.setAttribute("aria-label", `Borrar la materia ${materia.nombre}`);
  boton.addEventListener("click", () => borrarMateria(materia.id));
  item.append(boton);
  return item;
}

function mostrarMaterias(materias) {
  listaMaterias.replaceChildren(...materias.map(crearItemMateria));
  document.getElementById("vacio-materias").hidden = materias.length > 0;

  llenarSelectorDeMaterias(selectMateriaTarea, "Elija una materia", materias);
  llenarSelectorDeMaterias(selectFiltroMateria, "Todas", materias);

  document.getElementById("aviso-sin-materias").hidden = materias.length > 0;
  formTarea.hidden = materias.length === 0;
}

async function cargarMaterias() {
  const resultado = await pedirApi("GET", "/api/materias");
  if (resultado.ok) {
    mostrarMaterias(resultado.datos);
  }
}

async function registrarMateria(evento) {
  evento.preventDefault();
  ocultarExito(formMateria);
  const cuerpo = { nombre: formMateria.elements.nombre.value, color: formMateria.elements.color.value };

  const resultado = await pedirApi("POST", "/api/materias", cuerpo);
  if (!resultado.ok) {
    mostrarErrores(formMateria, resultado.errores);
    return;
  }
  limpiarErrores(formMateria);
  formMateria.reset();
  mostrarExito(formMateria, "Materia registrada.");
  await cargarMaterias();
}

async function borrarMateria(id) {
  errorBorrado.textContent = "";
  const resultado = await pedirApi("DELETE", `/api/materias/${id}`);
  if (!resultado.ok) {
    errorBorrado.textContent = resultado.errores.map((error) => error.mensaje).join(" ");
    return;
  }
  await cargarMaterias();
  // Si la materia borrada estaba en el filtro, este vuelve a "Todas" y el listado debe reflejarlo.
  await cargarTareas();
}

// --- Tareas -----------------------------------------------------------------

const ETIQUETAS_ALERTA = { vencida: "Vencida", urgente: "Urgente" };

function clasesDeTarjeta(tarea) {
  const clases = ["tarjeta", `color-${tarea.materia.color}`];
  if (tarea.alerta) {
    clases.push(tarea.alerta);
  }
  if (tarea.completada) {
    clases.push("completada");
  }
  return clases.join(" ");
}

/** Título de la tarea con su etiqueta "Vencida" o "Urgente", si la tiene. */
function crearEncabezadoTarea(tarea) {
  const encabezado = crearElemento("div", undefined, "encabezado-tarjeta");
  encabezado.append(crearElemento("h3", tarea.titulo));
  if (tarea.alerta) {
    // El texto de la etiqueta hace que la alerta no dependa solo del color.
    encabezado.append(crearElemento("span", ETIQUETAS_ALERTA[tarea.alerta], `etiqueta ${tarea.alerta}`));
  }
  return encabezado;
}

/** Materia (color y nombre), fecha de entrega, estado y descripción opcional. */
function crearDatosTarea(tarea) {
  const materia = crearElemento("p", undefined, "meta");
  materia.append(crearMuestraDeColor(tarea.materia.color), crearElemento("span", tarea.materia.nombre));

  const datos = [
    materia,
    crearElemento("p", `Entrega: ${formatearFecha(tarea.fecha_entrega)}`, "meta"),
    crearElemento("p", tarea.completada ? "Completada" : "Pendiente", "meta"),
  ];
  if (tarea.descripcion) {
    datos.push(crearElemento("p", tarea.descripcion, "descripcion"));
  }
  return datos;
}

/** Botón que marca la tarea como completada o la devuelve a pendiente. */
function crearBotonEstado(tarea) {
  const textoBoton = tarea.completada ? "Marcar como pendiente" : "Marcar como completada";
  const boton = crearElemento("button", textoBoton, "secundario");
  boton.type = "button";
  boton.setAttribute("aria-label", `${textoBoton}: ${tarea.titulo}`);
  boton.addEventListener("click", () => cambiarEstadoDeTarea(tarea));
  return boton;
}

function crearTarjetaTarea(tarea) {
  const tarjeta = crearElemento("li", undefined, clasesDeTarjeta(tarea));
  tarjeta.append(crearEncabezadoTarea(tarea), ...crearDatosTarea(tarea), crearBotonEstado(tarea));
  return tarjeta;
}

function hayFiltrosActivos() {
  return selectFiltroMateria.value !== "" || selectFiltroEstado.value !== "";
}

function mostrarTareas(tareas) {
  listaTareas.replaceChildren(...tareas.map(crearTarjetaTarea));
  const sinTareas = tareas.length === 0;
  document.getElementById("vacio-tareas").hidden = !(sinTareas && !hayFiltrosActivos());
  document.getElementById("sin-resultados").hidden = !(sinTareas && hayFiltrosActivos());
}

/** Pide el listado aplicando los filtros elegidos (materia y estado). */
async function cargarTareas() {
  const parametros = new URLSearchParams();
  if (selectFiltroMateria.value) {
    parametros.set("materia_id", selectFiltroMateria.value);
  }
  if (selectFiltroEstado.value) {
    parametros.set("estado", selectFiltroEstado.value);
  }
  const consulta = parametros.toString();

  const resultado = await pedirApi("GET", consulta ? `/api/tareas?${consulta}` : "/api/tareas");
  if (resultado.ok) {
    mostrarTareas(resultado.datos);
  }
}

async function cambiarEstadoDeTarea(tarea) {
  errorListado.textContent = "";
  const resultado = await pedirApi("PATCH", `/api/tareas/${tarea.id}`, { completada: !tarea.completada });
  if (!resultado.ok) {
    errorListado.textContent = resultado.errores.map((error) => error.mensaje).join(" ");
    return;
  }
  await cargarTareas();
}

function quitarFiltros() {
  selectFiltroMateria.value = "";
  selectFiltroEstado.value = "";
  cargarTareas();
}

/** Arma el cuerpo de la solicitud; los campos vacíos obligatorios se omiten para que el servidor los reporte. */
function leerFormularioDeTarea() {
  const campos = formTarea.elements;
  const cuerpo = { titulo: campos.titulo.value, descripcion: campos.descripcion.value };
  if (campos.materia_id.value) {
    cuerpo.materia_id = Number(campos.materia_id.value);
  }
  if (campos.fecha_entrega.value) {
    cuerpo.fecha_entrega = new Date(campos.fecha_entrega.value).toISOString();
  }
  return cuerpo;
}

async function guardarTarea(evento) {
  evento.preventDefault();
  ocultarExito(formTarea);

  const resultado = await pedirApi("POST", "/api/tareas", leerFormularioDeTarea());
  if (!resultado.ok) {
    mostrarErrores(formTarea, resultado.errores);
    return;
  }
  limpiarErrores(formTarea);
  formTarea.reset();
  mostrarExito(formTarea, "Tarea guardada.");
  await cargarTareas();
}

// --- Arranque ---------------------------------------------------------------

const SEGUNDOS_ENTRE_ACTUALIZACIONES = 60;

/** Vuelve a pedir el listado para que "vencida" y "urgente" se actualicen con el paso del tiempo. */
function actualizarListadoPeriodicamente() {
  setInterval(cargarTareas, SEGUNDOS_ENTRE_ACTUALIZACIONES * 1000);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
      cargarTareas();
    }
  });
}

formMateria.addEventListener("submit", registrarMateria);
formTarea.addEventListener("submit", guardarTarea);
selectFiltroMateria.addEventListener("change", cargarTareas);
selectFiltroEstado.addEventListener("change", cargarTareas);
document.getElementById("quitar-filtros").addEventListener("click", quitarFiltros);
document.getElementById("ir-a-materias").addEventListener("click", () => {
  document.getElementById("materia-nombre").focus();
});

llenarSelectorDeColores();
cargarMaterias();
cargarTareas();
actualizarListadoPeriodicamente();
