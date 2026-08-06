// ═══ EL MOTOR DE PANTALLA ═══════════════════════════════════════════════
//
// Pax Mundi se dibuja con React. React son ochenta kilobytes que hasta ahora
// se bajaban de un CDN la primera vez, y eso convertía un juego que cabe en un
// archivo en un juego que no arranca sin internet —y que, detrás de un proxy o
// de un cortafuegos que bloquee el CDN, no arranca nunca—. Acá está ese trozo,
// escrito a mano y adentro. Ya no se baja nada de ningún lado.
//
// No es React. Es lo que este juego usa de React, que es poco y está contado:
//
//   useState · useRef · useEffect · useMemo   (los cuatro ganchos)
//   jsx · jsxs · Fragment                     (lo que escribe el compilador)
//   createRoot                                (montarlo en la página)
//
// Ni contextos, ni reductores, ni portales, ni suspense, ni renderizado
// concurrente. Si algún día hicieran falta, se agregan; mientras tanto, lo que
// no está no puede fallar.
//
// Lo que sí hace igual que React, porque sin eso el mapa se arrastra:
//
//   · Reconcilia. Compara el árbol nuevo con el que ya está puesto y toca solo
//     lo que cambió, en vez de rehacer el DOM entero en cada cuadro.
//   · Se salta lo que no cambió de identidad. Cuando un trozo del árbol es el
//     mismo objeto que la vez pasada —lo que devuelve un useMemo— ni siquiera
//     entra a mirarlo. Ese atajo es la mitad del rendimiento del mapa.
//   · Guarda los ganchos por instancia, no por orden global: un componente que
//     aparece y desaparece —la rueda del clic derecho— no le corre los ganchos
//     a los demás.

const SVG = "http://www.w3.org/2000/svg";
// Nombres que en el DOM se escriben distinto que en JSX.
const ATR = { className: "class", strokeWidth: "stroke-width", strokeLinejoin: "stroke-linejoin",
  strokeLinecap: "stroke-linecap", strokeMiterlimit: "stroke-miterlimit",
  strokeDasharray: "stroke-dasharray", strokeDashoffset: "stroke-dashoffset",
  fillOpacity: "fill-opacity", strokeOpacity: "stroke-opacity", fillRule: "fill-rule",
  fontSize: "font-size", fontFamily: "font-family", fontWeight: "font-weight",
  textAnchor: "text-anchor", letterSpacing: "letter-spacing", shapeRendering: "shape-rendering",
  paintOrder: "paint-order", vectorEffect: "vector-effect", dominantBaseline: "dominant-baseline",
  stopColor: "stop-color", stopOpacity: "stop-opacity", pointerEvents: "pointer-events",
  clipPath: "clip-path", clipRule: "clip-rule", markerEnd: "marker-end", markerStart: "marker-start",
  gradientUnits: "gradientUnits", gradientTransform: "gradientTransform",
  patternUnits: "patternUnits", patternTransform: "patternTransform",
  preserveAspectRatio: "preserveAspectRatio", viewBox: "viewBox", tabIndex: "tabindex",
  ariaLabel: "aria-label", ariaHidden: "aria-hidden", autoComplete: "autocomplete",
  spellCheck: "spellcheck", readOnly: "readonly", maxLength: "maxlength" };
const EN_SVG = new Set(["svg", "g", "path", "rect", "circle", "ellipse", "line", "polygon",
  "polyline", "text", "tspan", "defs", "pattern", "clipPath", "mask", "marker", "use", "symbol",
  "image", "linearGradient", "radialGradient", "stop", "filter", "feGaussianBlur", "feOffset",
  "feBlend", "feColorMatrix", "title", "desc", "foreignObject"]);
// Propiedades de estilo que son números sin unidad.
const SIN_PX = /^(opacity|zIndex|flex|flexGrow|flexShrink|fontWeight|lineHeight|order|zoom|columnCount|fillOpacity|strokeOpacity|gridRow|gridColumn)$/;

// ——— los elementos ———
export const Fragment = Symbol.for("react.fragment");
export const jsx = (type, props, key) => ({ __v: true, type, props: props || {}, key });
export const jsxs = jsx;
export function createElement(type, props, ...hijos) {
  const p = { ...(props || {}) };
  const key = p.key != null ? p.key : undefined;
  delete p.key;
  if (hijos.length) p.children = hijos.length === 1 ? hijos[0] : hijos;
  return { __v: true, type, props: p, key };
}

// ——— los ganchos ———
// Cada instancia de componente guarda los suyos. `actual` es la que se está
// dibujando en este momento; `i` cuenta en qué gancho va.
let actual = null;
let repintar = null, pendiente = false;
const efectos = [];

function ranura(hacer) {
  if (!actual) throw new Error("un gancho fuera de un componente");
  const g = actual.ganchos;
  const k = actual.i++;
  if (!(k in g)) g[k] = hacer();
  return g[k];
}
function agendar() {
  if (pendiente) return;
  pendiente = true;
  // En microtarea: veinte cambios de estado seguidos son un solo repintado,
  // que es lo que hace React con su cola.
  Promise.resolve().then(() => { pendiente = false; if (repintar) repintar(); });
}
export function useState(inicial) {
  const r = ranura(() => ({ v: typeof inicial === "function" ? inicial() : inicial }));
  if (!r.poner) {
    r.poner = (nv) => {
      const n = typeof nv === "function" ? nv(r.v) : nv;
      if (Object.is(n, r.v)) return;
      r.v = n;
      agendar();
    };
  }
  return [r.v, r.poner];
}
export function useRef(v) { return ranura(() => ({ current: v })); }
const iguales = (a, b) => a && b && a.length === b.length && a.every((v, i) => Object.is(v, b[i]));
export function useMemo(f, deps) {
  const r = ranura(() => ({ vacio: true }));
  if (r.vacio || !deps || !iguales(deps, r.deps)) { r.v = f(); r.deps = deps; r.vacio = false; }
  return r.v;
}
export const useCallback = (f, deps) => useMemo(() => f, deps);
export function useEffect(f, deps) {
  const r = ranura(() => ({ vacio: true }));
  if (r.vacio || !deps || !r.deps || !iguales(deps, r.deps)) {
    r.deps = deps;
    r.vacio = false;
    efectos.push(r);
    r.correr = f;
  }
}
// Los efectos se corren después de tocar el DOM, no durante: lo que un efecto
// mida —el tamaño de una caja, dónde quedó un rótulo— tiene que ser lo que ya
// está en pantalla.
function correrEfectos() {
  while (efectos.length) {
    const r = efectos.shift();
    if (typeof r.limpiar === "function") { try { r.limpiar(); } catch (e) { console.error(e); } }
    let c = null;
    try { c = r.correr(); } catch (e) { console.error(e); }
    r.limpiar = typeof c === "function" ? c : null;
  }
}
function limpiarInstancia(ins) {
  for (const g of ins.ganchos || []) {
    if (g && typeof g.limpiar === "function") { try { g.limpiar(); } catch (e) { console.error(e); } }
  }
  for (const h of ins.hijas || []) limpiarInstancia(h);
}

// ——— del vnode al DOM ———
const guion = (p) => (p.startsWith("--") ? p : p.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase()));
function ponerEstilo(el, nuevo, viejo) {
  const n = nuevo || {}, v = viejo || {};
  for (const p of Object.keys(v)) if (!(p in n)) el.style.removeProperty(guion(p));
  for (const [p, q] of Object.entries(n)) {
    if (q == null || Object.is(q, v[p])) continue;
    el.style.setProperty(guion(p), typeof q === "number" && !SIN_PX.test(p) ? q + "px" : String(q));
  }
}
const esEvento = (k, v) => k.length > 2 && k[0] === "o" && k[1] === "n" && typeof v === "function";
function nombreEvento(k, el) {
  let ev = k.slice(2).toLowerCase();
  // React llama «change» a cada tecla; el DOM llama «change» a soltar el foco.
  // Menos en un campo de archivo: ahí no se escribe nada, y el evento propio
  // de «se eligió un archivo» es «change».
  if (ev === "change" && el.type !== "file"
      && (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT"))
    ev = "input";
  return ev;
}
function ponerProps(el, props, antes, svg) {
  const p = props || {}, a = antes || {};
  for (const k of Object.keys(a)) {
    if (k === "children" || k === "key" || k === "ref" || k in p) continue;
    if (esEvento(k, a[k])) { el.removeEventListener(nombreEvento(k, el), a[k]); continue; }
    if (k === "style") { ponerEstilo(el, null, a.style); continue; }
    el.removeAttribute(ATR[k] || k);
  }
  for (const [k, v] of Object.entries(p)) {
    if (k === "children" || k === "key") continue;
    if (k === "ref") {
      if (typeof v === "function") v(el);
      else if (v && typeof v === "object") v.current = el;
      continue;
    }
    if (esEvento(k, v)) {
      if (a[k] === v) continue;
      if (esEvento(k, a[k])) el.removeEventListener(nombreEvento(k, el), a[k]);
      el.addEventListener(nombreEvento(k, el), v);
      continue;
    }
    if (Object.is(v, a[k])) continue;
    if (k === "style") { ponerEstilo(el, typeof v === "object" ? v : null, a.style); continue; }
    // Un campo controlado se maneja por propiedad: el atributo solo fija el
    // valor inicial y, en cuanto alguien escribió, deja de tener efecto. Y no
    // se toca si tiene el foco, o un repintado tardío le borraría la letra
    // recién escrita.
    if (k === "value" && (el.tagName === "INPUT" || el.tagName === "TEXTAREA")) {
      const s = v == null ? "" : String(v);
      if (el.value !== s && el.ownerDocument.activeElement !== el) el.value = s;
      continue;
    }
    if (k === "checked" && el.tagName === "INPUT") { el.checked = !!v; continue; }
    if (v == null || v === false) { el.removeAttribute(ATR[k] || k); continue; }
    if (v === true) { el.setAttribute(ATR[k] || k, ""); continue; }
    if (!svg && k === "className") { el.className = v; continue; }
    el.setAttribute(ATR[k] || k, v);
  }
}

// Los fragmentos y las listas no son nodos: son hijos del padre. Se aplanan,
// igual que hace React.
function plano(n, out) {
  if (n == null || n === false || n === true) return out;
  if (Array.isArray(n)) { for (const x of n) plano(x, out); return out; }
  if (n.__v && n.type === Fragment) return plano(n.props.children, out);
  out.push(n);
  return out;
}
const claveDe = (v) => (v && v.__v && v.key != null ? "k" + v.key : null);

function llamar(ins, v) {
  const antes = actual;
  actual = ins;
  ins.i = 0;
  let salida = null;
  try { salida = v.type(v.props); } finally { actual = antes; }
  return salida;
}
function crear(v, padre, svg, ancla) {
  if (!v || !v.__v) {
    const t = document.createTextNode(String(v));
    padre.insertBefore(t, ancla || null);
    return { v, dom: t, texto: true };
  }
  if (typeof v.type === "function") {
    const ins = { v, comp: true, ganchos: [], i: 0, hijas: [] };
    const salida = llamar(ins, v);
    ins.hijas = plano(salida, []).map((h) => crear(h, padre, svg, ancla));
    return ins;
  }
  const esSvg = svg || EN_SVG.has(v.type);
  const el = esSvg ? document.createElementNS(SVG, v.type) : document.createElement(v.type);
  ponerProps(el, v.props, null, esSvg);
  const ins = { v, dom: el, svg: esSvg, hijas: [] };
  ins.hijas = plano(v.props.children, []).map((h) =>
    crear(h, el, esSvg && v.type !== "foreignObject", null));
  padre.insertBefore(el, ancla || null);
  return ins;
}
function domsDe(ins) {
  if (ins.dom) return [ins.dom];
  const out = [];
  for (const h of ins.hijas || []) out.push(...domsDe(h));
  return out;
}
function quitar(ins, padre) {
  limpiarInstancia(ins);
  for (const d of domsDe(ins)) if (d.parentNode === padre) padre.removeChild(d);
}
// ¿Cuelga un componente de este vnode? Se anota en el propio vnode: recorrerlo
// entero en cada comparación costaría más que lo que ahorra el atajo.
function tieneComponente(v) {
  if (!v || !v.__v) return false;
  if (v.__comp !== undefined) return v.__comp;
  let hay = typeof v.type === "function";
  if (!hay) for (const h of plano(v.props && v.props.children, [])) {
    if (tieneComponente(h)) { hay = true; break; }
  }
  try { Object.defineProperty(v, "__comp", { value: hay, enumerable: false }); } catch (e) { /* congelado */ }
  return hay;
}
function parchear(ins, v, padre, svg) {
  // El atajo que sostiene el mapa: si el vnode es el mismo objeto que la vez
  // pasada —lo que devuelve un useMemo— no hay nada que mirar.
  if (ins.v === v && !ins.comp && !tieneComponente(v)) return ins;
  const eraTexto = !!ins.texto, esTexto = !v || !v.__v;
  if (eraTexto !== esTexto || (!esTexto && ins.v.type !== v.type)) {
    const doms = domsDe(ins);
    const ancla = doms.length ? doms[doms.length - 1].nextSibling : null;
    quitar(ins, padre);
    return crear(v, padre, svg, ancla);
  }
  if (esTexto) {
    if (String(v) !== String(ins.v)) ins.dom.nodeValue = String(v);
    ins.v = v;
    return ins;
  }
  if (typeof v.type === "function") {
    const salida = llamar(ins, v);
    ins.hijas = parchearLista(ins.hijas, plano(salida, []), padre, svg);
    ins.v = v;
    return ins;
  }
  ponerProps(ins.dom, v.props, ins.v.props, ins.svg);
  ins.hijas = parchearLista(ins.hijas, plano(v.props.children, []),
    ins.dom, ins.svg && v.type !== "foreignObject");
  ins.v = v;
  return ins;
}
// Emparejar lo nuevo con lo viejo, y dejar cada cosa en su sitio.
//
// Los que traen clave se buscan por clave; los que no, por posición —que es lo
// que hace React—. Antes la clave de los que no la traían era «tipo +
// posición», y eso parecía más prudente pero costaba carísimo: alcanzaba con
// que apareciera un panel para que sus hermanos de más abajo corrieran un
// lugar, no encontraran su clave y se rehicieran enteros.
//
// Y lo que costaba todavía más: los nodos nuevos se agregaban al final y
// después había que reacomodar la fila entera. En ese reacomodo viajaba el
// mapa —quinientos cincuenta nodos— cada vez que se abría un panel que no
// tenía nada que ver con él. Mover un subárbol así obliga al navegador a
// rasterizarlo de nuevo: eso es el parpadeo, y también el tirón.
//
// Ahora se recorre de atrás para adelante llevando el ancla —el nodo que tiene
// que quedar a la derecha— y cada hijo se crea o se mueve directo a su lugar.
// Lo que ya está donde va, no se toca.
function parchearLista(viejas, vs, padre, svg) {
  const porClave = new Map();
  const sinClave = [];
  viejas.forEach((ins) => {
    const k = claveDe(ins.v);
    if (k != null) { if (!porClave.has(k)) porClave.set(k, ins); }
    else sinClave.push(ins);
  });
  // Primero se decide con quién va cada uno, sin tocar el DOM.
  const usadas = new Set();
  const pares = new Array(vs.length);
  let n = 0;
  for (let i = 0; i < vs.length; i++) {
    const k = claveDe(vs[i]);
    let vieja = null;
    if (k != null) {
      const c = porClave.get(k);
      if (c && !usadas.has(c)) vieja = c;
    } else {
      while (n < sinClave.length && usadas.has(sinClave[n])) n++;
      if (n < sinClave.length) vieja = sinClave[n++];
    }
    if (vieja) usadas.add(vieja);
    pares[i] = vieja;
  }
  // Los que sobran se van antes de colocar: así el ancla no apunta a un nodo
  // que está por desaparecer.
  for (const ins of viejas) if (!usadas.has(ins)) quitar(ins, padre);

  const salida = new Array(vs.length);
  let ancla = null;
  for (let i = vs.length - 1; i >= 0; i--) {
    const vieja = pares[i];
    const ins = vieja ? parchear(vieja, vs[i], padre, svg)
                      : crear(vs[i], padre, svg, ancla);
    salida[i] = ins;
    const doms = domsDe(ins);
    if (doms.length) {
      // Se recolocan de atrás para adelante y solo los que no están en su
      // sitio: mover un nodo le quita el foco a lo que tenga dentro.
      let esperado = ancla;
      for (let j = doms.length - 1; j >= 0; j--) {
        const d = doms[j];
        if (d.nextSibling !== esperado) padre.insertBefore(d, esperado);
        esperado = d;
      }
      ancla = doms[0];
    }
  }
  return salida;
}

// ——— montarlo ———
export function createRoot(contenedor) {
  let arbol = null, raiz = null;
  const pintar = () => {
    // Recolocar nodos le quita el foco al que lo tenga; se guarda y se devuelve.
    const foco = document.activeElement;
    const escribia = foco && (foco.tagName === "INPUT" || foco.tagName === "TEXTAREA");
    const ini = escribia ? foco.selectionStart : null;
    const fin = escribia ? foco.selectionEnd : null;
    if (!raiz) { contenedor.textContent = ""; raiz = crear(arbol, contenedor, false, null); }
    else raiz = parchear(raiz, arbol, contenedor, false);
    if (escribia && document.activeElement !== foco && foco.isConnected) {
      foco.focus();
      try { foco.setSelectionRange(ini, fin); } catch (e) { /* no todos lo admiten */ }
    }
    correrEfectos();
  };
  repintar = pintar;
  return {
    render(v) { arbol = v; pintar(); },
    unmount() { if (raiz) quitar(raiz, contenedor); raiz = null; contenedor.textContent = ""; },
  };
}

export default { createElement, Fragment, useState, useRef, useMemo, useCallback, useEffect,
  jsx, jsxs, createRoot };
