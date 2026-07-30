#!/usr/bin/env python3
"""
Pax Mundi — arranque local.

    python3 paxmundi.py

Levanta un servidor en http://localhost:8000 y abre el navegador. El juego
sigue siendo el mismo de siempre; este archivo se encarga de las dos cosas
que un archivo suelto no puede hacer por su cuenta:

  1 · Servirlo. Si está paxmundi.js —el juego ya traducido— lo usa y arranca
      al instante. Si editaste paxmundi.jsx, se da cuenta por la fecha y pasa
      solo a traducirlo en el navegador con Babel. No hay que compilar nada
      ni instalar node en ningún caso.

  2 · Hablar con la IA. El juego pide sus textos a la API de Anthropic, y un
      navegador no puede llamarla directamente: lo frena CORS y además haría
      falta dejar la clave a la vista de cualquiera. Las llamadas pasan por
      acá, que les agrega la clave del lado del servidor.

Para que la parte de IA funcione hace falta una clave:

    export ANTHROPIC_API_KEY=sk-ant-...        (Linux y macOS)
    set ANTHROPIC_API_KEY=sk-ant-...           (Windows, cmd)

Sin clave el mapa, las provincias y todo lo que no sea texto generado andan
igual; lo que falla es fundar la nación y pasar de turno.

Solo necesita Python 3.8 o posterior. No hay nada que instalar con pip.
"""

import argparse
import http.server
import json
import os
import socketserver
import sys
import threading
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FUENTE = RAIZ / "paxmundi.jsx"       # el juego, editable
ARMADO = RAIZ / "paxmundi.js"        # el mismo juego ya traducido, si está

API_ANTHROPIC = "https://api.anthropic.com/v1/messages"
VERSION_API = "2023-06-01"


def via():
    """Cuál de los dos caminos usar.

    Si paxmundi.js existe y no quedó viejo respecto del .jsx, se sirve ese:
    arranca al instante y el navegador no necesita Babel. Si tocaste el .jsx,
    el .js queda desactualizado y se pasa solo al camino con Babel, que
    traduce en el momento. Así editar y recargar siempre muestra tus cambios.
    """
    if ARMADO.exists() and (not FUENTE.exists()
                            or ARMADO.stat().st_mtime >= FUENTE.stat().st_mtime):
        return "armado"
    return "babel"

# En el camino con Babel el juego se monta al final, después de su propio
# código. Los `import` de un módulo se elevan al principio aunque estén
# escritos abajo, así que esto vale igual y deja el .jsx sin tocar.
ARRANQUE = """

// ——— añadido por paxmundi.py para montar el juego en la página ———
import { createRoot } from "react-dom/client";
createRoot(document.getElementById("raiz")).render(<PaxMundi />);
document.getElementById("cargando")?.remove();
"""

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pax Mundi</title>
<style>
  html, body { margin: 0; padding: 0; background: #0A0F17; color: #EDE3CC; }
  body { font-family: Georgia, 'Times New Roman', serif; }
  #cargando { position: fixed; inset: 0; display: flex; align-items: center;
    justify-content: center; flex-direction: column; gap: 14px; text-align: center;
    padding: 24px; }
  #cargando .t { font-size: 22px; letter-spacing: 1px; color: #D4AF37; }
  #cargando .s { font-size: 13px; color: #8E99AB; max-width: 30em; line-height: 1.6; }
  #cargando .b { width: 190px; height: 3px; background: rgba(212,175,55,0.18);
    border-radius: 2px; overflow: hidden; }
  #cargando .b i { display: block; width: 40%%; height: 100%%; background: #D4AF37;
    animation: vaiven 1.1s ease-in-out infinite; }
  @keyframes vaiven { 0%% { margin-left: -40%%; } 100%% { margin-left: 100%%; } }
  #fallo { position: fixed; inset: 0; display: none; padding: 32px;
    font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.7;
    background: #0A0F17; overflow: auto; white-space: pre-wrap; }
  #fallo b { color: #E05252; }
</style>

<!-- React sale de un CDN: es lo único que se baja de afuera. Hace falta
     internet la primera vez; después queda en la caché del navegador. -->
<script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@18.3.1",
    "react/jsx-runtime": "https://esm.sh/react@18.3.1/jsx-runtime",
    "react-dom": "https://esm.sh/react-dom@18.3.1?external=react",
    "react-dom/client": "https://esm.sh/react-dom@18.3.1/client?external=react"
  }
}
</script>
</head>
<body>

<div id="cargando">
  <div class="t">⚜ PAX MUNDI</div>
  <div class="b"><i></i></div>
  <div class="s">%(aviso)s</div>
</div>
<div id="fallo"></div>
<div id="raiz"></div>

<script>
// El juego pide sus textos a api.anthropic.com. Un navegador no puede llamar
// ahí directamente —CORS, y la clave quedaría a la vista— así que se desvía
// al servidor local, que la agrega del lado de acá. El .jsx queda intacto.
(function () {
  const original = window.fetch.bind(window);
  window.fetch = function (recurso, opciones) {
    const url = typeof recurso === "string" ? recurso : (recurso && recurso.url) || "";
    if (url.startsWith("https://api.anthropic.com/")) return original("/api/mensajes", opciones);
    return original(recurso, opciones);
  };
})();

function mostrarFallo(titulo, detalle) {
  const c = document.getElementById("cargando");
  if (c) c.remove();
  const f = document.getElementById("fallo");
  f.style.display = "block";
  f.innerHTML = "<b>" + titulo + "</b>\\n\\n" + detalle;
}
window.addEventListener("error", (e) => {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("No se pudo arrancar el juego", (e.message || e) + "\\n\\nMirá la consola del navegador (F12) para el detalle.");
});
setTimeout(() => {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("No cargó lo que viene de afuera",
      "React%(tambien)s se baja de un CDN y hace falta internet la primera vez.\\n" +
      "Si estás sin conexión, o detrás de un proxy o cortafuegos que lo bloquea,\\n" +
      "el juego no puede arrancar. En la consola del navegador (F12) se ve qué falló.");
}, 30000);
</script>

%(cargador)s

</body>
</html>
"""

# Camino rápido: el juego ya viene traducido, el navegador solo importa React.
CARGADOR_ARMADO = """<script type="module">
  import PaxMundi from "/app.js";
  import { createRoot } from "react-dom/client";
  import { jsx } from "react/jsx-runtime";
  createRoot(document.getElementById("raiz")).render(jsx(PaxMundi, {}));
  document.getElementById("cargando")?.remove();
</script>"""

# Camino con Babel: traduce el JSX en el momento, para poder editarlo y recargar.
CARGADOR_BABEL = """<script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>
<script type="text/babel" data-type="module" data-presets="react" src="/app.jsx"></script>"""


def pagina():
    if via() == "armado":
        return PLANTILLA % {"cargador": CARGADOR_ARMADO, "tambien": "",
                            "aviso": "Desplegando el mapa del mundo."}
    return PLANTILLA % {"cargador": CARGADOR_BABEL, "tambien": " —y Babel, que traduce el JSX—",
                        "aviso": "Traduciendo el juego y desplegando el mapa del mundo.<br>"
                                 "Con Babel tarda unos segundos."}


class Manejador(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "PaxMundi"

    # ——— utilidades ———
    def responder(self, codigo, cuerpo, tipo="text/plain; charset=utf-8"):
        if isinstance(cuerpo, str):
            cuerpo = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(cuerpo)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, formato, *args):
        if self.server.verboso:
            sys.stderr.write("  %s\n" % (formato % args))

    # ——— rutas ———
    def do_GET(self):
        ruta = self.path.split("?")[0]
        if ruta in ("/", "/index.html"):
            return self.responder(200, pagina(), "text/html; charset=utf-8")

        if ruta in ("/app.jsx", "/paxmundi.jsx"):
            # se lee en cada pedido: editás el .jsx, recargás, y ya está
            if not FUENTE.exists():
                return self.responder(500, "No encuentro paxmundi.jsx en %s" % RAIZ)
            fuente = FUENTE.read_text(encoding="utf-8")
            if ruta == "/app.jsx":
                fuente += ARRANQUE
            return self.responder(200, fuente, "text/plain; charset=utf-8")

        if ruta in ("/app.js", "/paxmundi.js"):
            if not ARMADO.exists():
                return self.responder(500, "No encuentro paxmundi.js en %s" % RAIZ)
            return self.responder(200, ARMADO.read_text(encoding="utf-8"),
                                  "text/javascript; charset=utf-8")

        if ruta == "/salud":
            return self.responder(
                200, json.dumps({"ok": True, "via": via(), "clave": bool(clave_api())}),
                "application/json; charset=utf-8")

        self.responder(404, "No hay nada en %s" % ruta)

    def do_POST(self):
        if self.path.split("?")[0] != "/api/mensajes":
            return self.responder(404, "No hay nada en %s" % self.path)

        clave = clave_api()
        if not clave:
            return self.responder(
                503,
                json.dumps({"error": {
                    "type": "sin_clave",
                    "message": "Falta ANTHROPIC_API_KEY. Pará el servidor, definila y volvé a arrancar."
                }}),
                "application/json; charset=utf-8")

        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(largo) if largo else b"{}"

        pedido = urllib.request.Request(
            API_ANTHROPIC, data=cuerpo, method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": clave,
                "anthropic-version": VERSION_API,
            })
        try:
            with urllib.request.urlopen(pedido, timeout=120) as r:
                return self.responder(r.status, r.read(), "application/json; charset=utf-8")
        except urllib.error.HTTPError as e:
            detalle = e.read()
            sys.stderr.write("  ✗ la API respondió %s: %s\n" % (e.code, detalle[:300].decode("utf-8", "replace")))
            return self.responder(e.code, detalle, "application/json; charset=utf-8")
        except Exception as e:                                   # red caída, DNS, proxy…
            sys.stderr.write("  ✗ no se pudo llegar a la API: %s\n" % e)
            return self.responder(
                502, json.dumps({"error": {"type": "sin_red", "message": str(e)}}),
                "application/json; charset=utf-8")


class Servidor(socketserver.ThreadingTCPServer):
    """Con hilos: si no, una llamada a la IA congelaría la página entera."""
    allow_reuse_address = True
    daemon_threads = True
    verboso = False


def clave_api():
    return (os.environ.get("ANTHROPIC_API_KEY") or "").strip()


def main():
    p = argparse.ArgumentParser(description="Arranca Pax Mundi en el navegador.")
    p.add_argument("-p", "--puerto", type=int, default=8000, help="puerto (por defecto 8000)")
    p.add_argument("--sin-navegador", action="store_true", help="no abrir el navegador solo")
    p.add_argument("-v", "--verboso", action="store_true", help="mostrar cada pedido")
    args = p.parse_args()

    if not FUENTE.exists() and not ARMADO.exists():
        sys.exit("No encuentro ni paxmundi.jsx ni paxmundi.js.\nAl menos uno tiene que "
                 "estar en la misma carpeta que paxmundi.py:\n  %s" % RAIZ)

    try:
        servidor = Servidor(("127.0.0.1", args.puerto), Manejador)
    except OSError as e:
        sys.exit("No pude abrir el puerto %d (%s).\nProbá con otro: python3 paxmundi.py -p 8080"
                 % (args.puerto, e))
    servidor.verboso = args.verboso

    url = "http://localhost:%d/" % args.puerto
    archivo = ARMADO if via() == "armado" else FUENTE
    print("⚜  PAX MUNDI")
    print("   %s  (%.0f KB)" % (archivo.name, archivo.stat().st_size / 1024))
    if via() == "armado":
        print("   Ya traducido: arranca al instante.")
    else:
        print("   Se traduce con Babel en el navegador: tarda unos segundos.")
        if ARMADO.exists():
            print("   (paxmundi.js quedó viejo respecto del .jsx y se ignora)")
    print("   %s" % url)
    if clave_api():
        print("   IA: clave encontrada")
    else:
        print("   IA: SIN CLAVE — el mapa anda, pero no vas a poder fundar la nación")
        print("       export ANTHROPIC_API_KEY=sk-ant-...   y volvé a arrancar")
    print("   Ctrl+C para parar\n")

    if not args.sin_navegador:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n   Hasta la próxima.")
    finally:
        servidor.shutdown()
        servidor.server_close()


if __name__ == "__main__":
    main()
