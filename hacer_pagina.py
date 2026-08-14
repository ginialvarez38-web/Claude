#!/usr/bin/env python3
"""Arma paxmundi.html: el juego entero en una página, sin servidor.

Hay entornos donde no se puede abrir un puerto —un Python online, una app de
teléfono, un sandbox—. Ahí ningún arreglo del servidor sirve, porque el
problema es que no puede haber servidor. Esto quita la pieza: una sola página
que se abre a mano y no habla con nadie.

Para eso el paquete no puede ser un módulo ES: los módulos, abiertos con
file://, los bloquea el propio navegador por CORS. Se arma como IIFE, un
guion clásico, que sí anda desde un archivo suelto.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
OBRA = RAIZ / "obrador"          # andamio de armado; se rehace solo
DESTINO = RAIZ / "paxmundi.html"

CABECERA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pax Mundi</title>
<style>
  html, body { margin: 0; padding: 0; background: #0A0F17; color: #EDE3CC; }
  body { font-family: 'Inter', 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif; }
  #cargando { position: fixed; inset: 0; display: flex; align-items: center;
    justify-content: center; flex-direction: column; gap: 14px; text-align: center;
    padding: 24px; }
  #cargando .t { font-size: 22px; letter-spacing: 1px; color: #D4AF37; }
  #cargando .s { font-size: 13px; color: #8E99AB; max-width: 30em; line-height: 1.6; }
  #cargando .b { width: 190px; height: 3px; background: rgba(212,175,55,0.18);
    border-radius: 2px; overflow: hidden; }
  #cargando .b i { display: block; width: 40%; height: 100%; background: #D4AF37;
    animation: vaiven 1.1s ease-in-out infinite; }
  @keyframes vaiven { 0% { margin-left: -40%; } 100% { margin-left: 100%; } }
  #fallo { position: fixed; inset: 0; display: none; padding: 32px;
    font-family: 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', 'Consolas', 'DejaVu Sans Mono', 'Liberation Mono', monospace; font-size: 13px; line-height: 1.7;
    background: #0A0F17; overflow: auto; white-space: pre-wrap; }
  #fallo b { color: #E05252; }
</style>
</head>
<body>

<div id="cargando">
  <div class="t">&#9884; PAX MUNDI</div>
  <div class="b"><i></i></div>
  <div class="s">Desplegando el mapa del mundo.</div>
</div>
<div id="fallo"></div>
<div id="raiz"></div>

<script>
// El juego puede pedirle los textos a la IA, y para eso hace falta un
// servidor que le agregue la clave: un navegador no puede llamar a
// api.anthropic.com por su cuenta. Aca no hay servidor, asi que ese camino no
// existe. Se corta de entrada, con el motivo dicho, en vez de dejar al juego
// esperando una respuesta que no va a llegar. El motor local no lo necesita:
// resuelve los turnos, entiende las ordenes y narra sin salir a ningun lado,
// y es el que viene puesto.
(function () {
  var original = window.fetch ? window.fetch.bind(window) : null;
  window.fetch = function (recurso, opciones) {
    var url = typeof recurso === "string" ? recurso : (recurso && recurso.url) || "";
    if (url.indexOf("https://api.anthropic.com/") === 0)
      return Promise.reject(new Error(
        "Esta version es una pagina sola, sin servidor: el motor de IA no esta " +
        "disponible. Usa el motor local, que hace todo sin red."));
    return original ? original(recurso, opciones) : Promise.reject(new Error("sin fetch"));
  };
})();

function mostrarFallo(titulo, detalle) {
  var c = document.getElementById("cargando");
  if (c) c.remove();
  var f = document.getElementById("fallo");
  f.style.display = "block";
  f.innerHTML = "<b>" + titulo + "</b>\\n\\n" + detalle;
}
window.addEventListener("error", function (e) {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("No se pudo arrancar el juego",
      (e.message || e) + "\\n\\nAbri la consola del navegador para el detalle.");
});
// Esta pagina no habla con nadie: no hay servidor, no hay red, no hay CDN.
// Si a los siete segundos no se pinto nada, el fallo esta en el navegador y
// no en ningun camino: hay que decir donde mirar.
setTimeout(function () {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("El juego no llego a arrancar",
      "Esta pagina no necesita servidor ni internet: el juego entero esta aca\\n" +
      "adentro. Si no arranco, el problema esta en el navegador.\\n\\n" +
      "Que probar:\\n" +
      "  1. Abrir la consola del navegador: ahi va a estar el error.\\n" +
      "  2. Probar con otro navegador. El juego necesita uno de los ultimos\\n" +
      "     anios; los muy viejos no entienden lo que usa.\\n" +
      "  3. Si el archivo se bajo a medias, bajarlo de nuevo: pesa unos 2 MB.");
}, 7000);
</script>

<script>
"""

PIE = """
</script>
</body>
</html>
"""


# El juego pide sus cosas a "react", pero acá React es runtime.js, que está al
# lado. Un node_modules de mentira con tres archivos hace que esos pedidos
# caigan donde tienen que caer, sin tocar una línea del juego.
PUENTES = {
    "node_modules/react/package.json":
        '{ "name": "react", "version": "18.0.0", "main": "index.js", "type": "module" }\n',
    "node_modules/react/index.js":
        'export * from "../../motor.js";\nimport M from "../../motor.js";\nexport default M;\n',
    "node_modules/react/jsx-runtime.js":
        'export { jsx, jsxs, Fragment } from "../../motor.js";\n',
    "node_modules/react-dom/package.json":
        '{ "name": "react-dom", "version": "18.0.0", "main": "index.js", "type": "module" }\n',
    "node_modules/react-dom/index.js":
        'export { createRoot } from "../../motor.js";\n',
    "node_modules/react-dom/client.js":
        'export { createRoot } from "../../motor.js";\n',
    "entrada.jsx":
        'import PaxMundi from "./juego.jsx";\n'
        'import { createRoot } from "react-dom/client";\n'
        'import { jsx } from "react/jsx-runtime";\n'
        'createRoot(document.getElementById("raiz")).render(jsx(PaxMundi, {}));\n'
        'var c = document.getElementById("cargando");\n'
        'if (c) c.remove();\n',
}


def andamio():
    """Se rehace en cada corrida: así no hay que acordarse de nada ni queda
    ningún resto viejo decidiendo cómo se arma el juego de hoy."""
    for nombre, texto in PUENTES.items():
        f = OBRA / nombre
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(texto, encoding="utf-8")


def armar():
    OBRA.mkdir(parents=True, exist_ok=True)
    andamio()
    shutil.copy(RAIZ / "paxmundi.jsx", OBRA / "juego.jsx")
    shutil.copy(RAIZ / "runtime.js", OBRA / "motor.js")
    r = subprocess.run(
        ["bun", "build", "entrada.jsx", "--format=iife", "--minify", "--production",
         "--outfile=todo.js"],
        cwd=OBRA, capture_output=True, text=True)
    if r.returncode:
        sys.exit("bun build fallo:\n%s\n%s" % (r.stdout, r.stderr))
    js = (OBRA / "todo.js").read_text(encoding="utf-8")

    # Un "</script" dentro del guion cerraria la etiqueta antes de tiempo y
    # el resto del juego se leeria como texto. Se parte en dos, que para el
    # que lee JavaScript es lo mismo y para el que lee HTML ya no cierra nada.
    js = js.replace("</script", "<\\/script")

    pagina = CABECERA + js + PIE
    DESTINO.write_text(pagina, encoding="utf-8")
    print("escrito %s (%.0f KB)" % (DESTINO, DESTINO.stat().st_size / 1024))
    revisar(pagina, js)


def revisar(pagina, js):
    import tempfile, os
    # El guion tiene que ser JavaScript valido: si no, la pagina se abre y no
    # hace nada, que es justo el fallo que estamos tratando de sacar de encima.
    p = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    p.write(js.replace("<\\/script", "</script"))
    p.close()
    r = subprocess.run(["node", "--check", p.name], capture_output=True, text=True)
    os.unlink(p.name)
    print("   el juego adentro: %s" % ("JavaScript valido" if not r.returncode
                                       else "ROTO: " + r.stderr[:200]))
    sueltas = len(re.findall(r"</script", pagina)) - pagina.count("<\\/script")
    print("   etiquetas </script> reales: %d (tienen que ser 2)" % sueltas)
    print("   no pide nada de afuera: %s" % ("si" if not re.search(
        r'(src|href)\s*=\s*["\']https?:', pagina) else "NO — hay algo externo"))


if __name__ == "__main__":
    armar()
