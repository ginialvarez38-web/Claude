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
import socket
import socketserver
import sys
import threading
import traceback
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FUENTE = RAIZ / "paxmundi.jsx"       # el juego, editable
ARMADO = RAIZ / "paxmundi.js"        # el mismo juego ya traducido, si está
MOTOR = RAIZ / "runtime.js"      # el motor de pantalla: React mínimo, propio

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

<!-- Nada se baja de afuera. El motor de pantalla va en /runtime.js, que sale
     de este mismo archivo: sin internet, sin CDN y sin sorpresas. -->
<script type="importmap">
{
  "imports": {
    "react": "/runtime.js",
    "react/jsx-runtime": "/runtime.js",
    "react-dom": "/runtime.js",
    "react-dom/client": "/runtime.js"
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
// Siete segundos y no treinta: si algo no llegó, el juego se queda en la
// pantalla de carga para siempre, y media hora mirando una barra que se mueve
// no le dice a nadie qué pasó ni qué hacer.
setTimeout(() => {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("El juego no llegó a arrancar", %(fallo)s);
}, 7000);
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


# Qué decir cuando no arranca depende del camino, porque no fallan por lo
# mismo. Por el camino armado no se baja nada: si no arranca, el problema está
# de este lado y hay que decir dónde mirar. Por el camino con Babel sí se baja
# algo, y entonces la conexión vuelve a ser sospechosa.
FALLO_ARMADO = (
    '"Todo lo que hace falta sale de esta misma carpeta: no se baja nada de\\n" +\n'
    '      "internet, así que no es la conexión.\\n\\n" +\n'
    '      "Qué probar:\\n" +\n'
    '      "  1. En la terminal donde arrancaste el juego: si algo se rompió del\\n" +\n'
    '      "     lado de Python, quedó escrito ahí entero.\\n" +\n'
    '      "  2. Parar el juego (Ctrl+C) y correr:  python3 paxmundi.py --probar\\n" +\n'
    '      "     Se revisa a sí mismo y dice qué parte falla.\\n" +\n'
    '      "  3. Abrir la consola (F12), pestaña Consola: si el error es del lado\\n" +\n'
    '      "     del navegador, aparece ahí."')
FALLO_BABEL = (
    '"Por este camino el JSX se traduce en el navegador con Babel, y Babel es lo\\n" +\n'
    '      "único que se baja de afuera (unpkg.com). Si estás sin internet, o detrás\\n" +\n'
    '      "de un proxy que lo bloquea, no hay manera de arrancar así.\\n\\n" +\n'
    '      "Qué probar:\\n" +\n'
    '      "  1. Regenerar paxmundi.js: con el juego ya traducido no hace falta\\n" +\n'
    '      "     Babel ni internet. La orden está en el LEEME.\\n" +\n'
    '      "  2. Parar el juego (Ctrl+C) y correr:  python3 paxmundi.py --probar\\n" +\n'
    '      "  3. Abrir la consola (F12), pestaña Red: ahí se ve qué dirección no\\n" +\n'
    '      "     responde."')


def pagina():
    if via() == "armado":
        return PLANTILLA % {"cargador": CARGADOR_ARMADO, "fallo": FALLO_ARMADO,
                            "aviso": "Desplegando el mapa del mundo."}
    return PLANTILLA % {"cargador": CARGADOR_BABEL, "fallo": FALLO_BABEL,
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
    # Si algo se rompe adentro, sin esto la conexión se cierra sin una sola
    # letra y el navegador solo sabe decir «localhost no envió ningún dato».
    # Con esto, dice qué se rompió: en la pantalla y en la terminal.
    def do_GET(self):
        try:
            self.servir()
        except Exception:
            self.confesar("servir")

    def do_POST(self):
        try:
            self.despachar()
        except Exception:
            self.confesar("responder a")

    def confesar(self, verbo):
        detalle = traceback.format_exc()
        sys.stderr.write("\n  ✗ se rompió al %s %s\n%s\n" % (verbo, self.path, detalle))
        try:
            self.responder(500, "Se rompió al %s %s\n\n%s\n"
                                "Copiá esto entero: dice exactamente qué falló."
                                % (verbo, self.path, detalle))
        except Exception:
            pass

    def servir(self):
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

        # El motor de pantalla. Antes venía de un CDN y era lo único que hacía
        # falta bajar; ahora sale de acá al lado, así que el juego arranca sin
        # internet.
        if ruta == "/runtime.js":
            if not MOTOR.exists():
                return self.responder(500, "No encuentro runtime.js en %s" % RAIZ)
            return self.responder(200, MOTOR.read_text(encoding="utf-8"),
                                  "text/javascript; charset=utf-8")

        if ruta == "/salud":
            return self.responder(
                200, json.dumps({"ok": True, "via": via(), "clave": bool(clave_api())}),
                "application/json; charset=utf-8")

        self.responder(404, "No hay nada en %s" % ruta)

    def despachar(self):
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


def mi_direccion():
    """La dirección de esta máquina en la red, para abrirla desde otro lado.

    No manda nada: abrir un socket UDP no habla con nadie, solo hace que el
    sistema elija por cuál de sus placas saldría, y esa es la que sirve."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
        finally:
            s.close()
    except Exception:
        return None


def clave_api():
    return (os.environ.get("ANTHROPIC_API_KEY") or "").strip()


def revisar(puerto):
    print("⚜  PAX MUNDI · revisión")
    print("   python %s en %s" % (sys.version.split()[0], sys.platform))
    for f in (FUENTE, ARMADO, MOTOR):
        print("   %-14s %s" % (f.name, "%.0f KB" % (f.stat().st_size / 1024)
                               if f.exists() else "✗ no está"))
    try:
        srv = Servidor(("127.0.0.1", puerto), Manejador)
    except OSError as e:
        print("   ✗ no pude abrir el puerto %d: %s" % (puerto, e))
        print("     si el juego ya está corriendo, pará ese y volvé a probar,")
        print("     o probá otro puerto: python3 paxmundi.py --probar -p 8080")
        return
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % puerto
    malas = 0
    rutas = ["/", "/runtime.js", "/salud"] + (["/app.js"] if ARMADO.exists() else ["/app.jsx"])
    for ruta in rutas:
        try:
            with urllib.request.urlopen(base + ruta, timeout=20) as r:
                cuerpo = r.read()
            print("   %-13s %s  %.0f KB" % (ruta, r.status, len(cuerpo) / 1024))
        except Exception as e:
            malas += 1
            print("   %-13s ✗ %s" % (ruta, e))
    srv.shutdown()
    srv.server_close()
    if malas:
        print("\n   Algo no sale. Copiá todo esto y mandalo: dice qué ruta falla.")
        return
    print("\n   Todo sale bien desde acá: el servidor sirve las cuatro cosas enteras.")
    print("   Si el navegador igual no muestra nada, el problema no es el archivo")
    print("   sino el camino entre Python y el navegador. Por orden:")
    print("     · ¿El navegador corre en el mismo lado que esto? Si Python está en")
    print("       un emulador, una máquina virtual, un contenedor o WSL y el")
    print("       navegador está afuera, «127.0.0.1» son dos sitios distintos y no")
    print("       se ven. Arrancá con:  python3 paxmundi.py --red")
    print("       y abrí la dirección que te va a decir, no localhost.")
    print("     · Si aun estando del mismo lado no anda, probá:")
    print("       python3 paxmundi.py --simple    (una conexión por pedido)")
    print("     · Y abrí %s a mano, en vez de localhost." % base)


def main():
    p = argparse.ArgumentParser(description="Arranca Pax Mundi en el navegador.")
    p.add_argument("-p", "--puerto", type=int, default=8000, help="puerto (por defecto 8000)")
    p.add_argument("--sin-navegador", action="store_true", help="no abrir el navegador solo")
    p.add_argument("--probar", action="store_true",
                   help="revisar que cada ruta contesta, y salir")
    p.add_argument("--red", action="store_true",
                   help="atender también desde afuera de esta máquina "
                        "(emuladores, máquinas virtuales, otro aparato)")
    p.add_argument("--simple", action="store_true",
                   help="HTTP/1.0, una conexión por pedido: más lento y más compatible")
    p.add_argument("-v", "--verboso", action="store_true", help="mostrar cada pedido")
    args = p.parse_args()

    if args.simple:
        Manejador.protocol_version = "HTTP/1.0"

    # ——— revisión ———
    # Si el navegador dice «localhost no envió ningún dato», esto contesta por
    # qué: levanta el servidor de verdad, se pide a sí mismo cada cosa y dice
    # cuál falla y con qué error. Es una sola orden y se puede copiar entera.
    if args.probar:
        return revisar(args.puerto)

    if not FUENTE.exists() and not ARMADO.exists():
        sys.exit("No encuentro ni paxmundi.jsx ni paxmundi.js.\nAl menos uno tiene que "
                 "estar en la misma carpeta que paxmundi.py:\n  %s" % RAIZ)

    # Por defecto solo atiende a esta misma máquina, que es lo prudente: por
    # acá pasa la clave de la API. Con --red atiende a cualquiera que llegue,
    # que es lo que hace falta cuando el navegador está de un lado y Python
    # del otro —un emulador, una máquina virtual, un contenedor, otro aparato—
    # porque ahí «127.0.0.1» son dos sitios distintos y no se ven.
    anfitrion = "0.0.0.0" if args.red else "127.0.0.1"
    try:
        servidor = Servidor((anfitrion, args.puerto), Manejador)
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
    if args.red:
        mia = mi_direccion()
        print("   desde otro aparato o desde afuera del emulador:")
        print("      http://%s:%d/" % (mia or "TU-IP", args.puerto))
        if clave_api():
            print("   ojo: así lo alcanza cualquiera de tu red, y por acá pasa la clave.")
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
