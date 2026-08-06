"""Genera paxmundi_solo.py: el juego entero dentro de un único archivo Python.

El juego va comprimido con lzma y codificado en base85 —el alfabeto de base85
no incluye comillas ni barras invertidas, así que entra tal cual en un literal
de Python sin escapar nada—. Se descomprime en memoria al arrancar.
"""
import base64
import lzma
import textwrap
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
js = (RAIZ / "paxmundi.js").read_bytes()
blob = base64.b85encode(lzma.compress(js, preset=9 | lzma.PRESET_EXTREME)).decode("ascii")
envuelto = "\n".join(textwrap.wrap(blob, 100))
# El motor de pantalla va adentro también: es lo único que se bajaba de un CDN
# y por eso el juego no arrancaba sin internet.
motor = (RAIZ / "runtime.js").read_bytes()
blobM = base64.b85encode(lzma.compress(motor, preset=9 | lzma.PRESET_EXTREME)).decode("ascii")
envueltoM = "\n".join(textwrap.wrap(blobM, 100))

CABEZA = '''#!/usr/bin/env python3
"""
Pax Mundi — el juego entero en un solo archivo.

    python3 paxmundi_solo.py

Levanta un servidor local y abre el navegador. No hay que instalar nada:
solo Python 3.8 o posterior. Ni pip, ni node, ni compilar.

El juego va comprimido dentro de este mismo archivo, al final. Este .py se
encarga de tres cosas:

  1 · Descomprimirlo y servirlo.

  2 · Hablar con la IA, si le das una clave. El juego pide sus textos a la API
      de Anthropic y un navegador no puede llamarla directamente: lo frena
      CORS, y además habría que dejar la clave a la vista. Las llamadas pasan
      por acá, que les agrega la clave del lado del servidor.

  3 · Avisarte con claridad si algo no carga, en vez de dejarte una página
      en blanco.

La clave es opcional:

    export ANTHROPIC_API_KEY=sk-ant-...        (Linux y macOS)
    set ANTHROPIC_API_KEY=sk-ant-...           (Windows, cmd)

Sin clave el juego funciona igual: el motor local resuelve los turnos, entiende
las órdenes que escribas y narra sin salir a ninguna red. La IA solo cambia
quién escribe la crónica, y se elige con el interruptor MOTOR dentro del juego.

No se baja nada de afuera: el motor de pantalla también va adentro. El juego
arranca sin internet, detrás de un proxy o en una máquina aislada. La única
llamada a la red posible es a la API de Anthropic, y solo si diste una clave.

    python3 paxmundi_solo.py --extraer    escribe paxmundi.js al lado, por si
                                          querés el código suelto
    python3 paxmundi_solo.py --probar     revisa que todo lo de adentro sale
                                          bien y dice qué falla, si algo falla
    python3 paxmundi_solo.py --red        atiende también desde afuera de esta
                                          máquina: hace falta si Python corre en
                                          un emulador o una máquina virtual y el
                                          navegador está del otro lado
"""

import argparse
import base64
import http.server
import json
import lzma
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

API_ANTHROPIC = "https://api.anthropic.com/v1/messages"
VERSION_API = "2023-06-01"

_juego = None
_motor = None


def juego():
    """El juego, descomprimido una sola vez y guardado en memoria."""
    global _juego
    if _juego is None:
        _juego = lzma.decompress(base64.b85decode(JUEGO.replace("\\n", "")))
    return _juego


def motor():
    """El motor de pantalla, tambien adentro. Es lo que antes se bajaba de un
    CDN: sin esto el juego no arrancaba sin internet."""
    global _motor
    if _motor is None:
        _motor = lzma.decompress(base64.b85decode(MOTOR.replace("\\n", "")))
    return _motor


PAGINA = r"""<!doctype html>
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
  #cargando .b i { display: block; width: 40%; height: 100%; background: #D4AF37;
    animation: vaiven 1.1s ease-in-out infinite; }
  @keyframes vaiven { 0% { margin-left: -40%; } 100% { margin-left: 100%; } }
  #fallo { position: fixed; inset: 0; display: none; padding: 32px;
    font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.7;
    background: #0A0F17; color: #EDE3CC; overflow: auto; white-space: pre-wrap; }
  #fallo b { color: #E05252; }
</style>

<!-- Nada se baja de afuera: el motor de pantalla sale de este mismo archivo. -->
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
  <div class="t">&#9884; PAX MUNDI</div>
  <div class="b"><i></i></div>
  <div class="s">Desplegando el mapa del mundo.</div>
</div>
<div id="fallo"></div>
<div id="raiz"></div>

<script>
// El juego pide sus textos a api.anthropic.com. Un navegador no puede llamar
// ahi directamente --CORS, y la clave quedaria a la vista-- asi que se desvia
// al servidor local, que la agrega de este lado.
(function () {
  var original = window.fetch.bind(window);
  window.fetch = function (recurso, opciones) {
    var url = typeof recurso === "string" ? recurso : (recurso && recurso.url) || "";
    if (url.indexOf("https://api.anthropic.com/") === 0) return original("/api/mensajes", opciones);
    return original(recurso, opciones);
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
      (e.message || e) + "\\n\\nMira la consola del navegador (F12) para el detalle.");
});
// Si a los siete segundos no se pinto nada, el juego se quedaria en la
// pantalla de carga para siempre y sin decir por que. Nada de esto se baja de
// afuera, asi que si falla, falla acá adentro: hay que decir donde mirar.
setTimeout(function () {
  if (document.getElementById("raiz").childElementCount === 0)
    mostrarFallo("El juego no llego a arrancar",
      "Todo lo que hace falta esta dentro de este archivo: no se baja nada de\\n" +
      "internet, asi que no es la conexion.\\n\\n" +
      "Que probar:\\n" +
      "  1. En la terminal donde arrancaste el juego: si algo se rompio del lado\\n" +
      "     de Python, quedo escrito ahi entero.\\n" +
      "  2. Parar el juego (Ctrl+C) y correr:  python3 paxmundi_solo.py --probar\\n" +
      "     Se revisa a si mismo y dice que parte falla.\\n" +
      "  3. Abrir la consola (F12), pestana Consola: si el error es del lado del\\n" +
      "     navegador, aparece ahi.");
}, 7000);
</script>

<script type="module">
  import PaxMundi from "/app.js";
  import { createRoot } from "react-dom/client";
  import { jsx } from "react/jsx-runtime";
  createRoot(document.getElementById("raiz")).render(jsx(PaxMundi, {}));
  var c = document.getElementById("cargando");
  if (c) c.remove();
</script>

</body>
</html>
"""


class Manejador(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "PaxMundi"

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
        if getattr(self.server, "verboso", False):
            sys.stderr.write("  %s\\n" % (formato % args))

    # Un fallo al servir dejaba la conexion cerrada sin una sola letra, y el
    # navegador solo sabe decir "localhost no envio ningun dato". Cualquier
    # cosa que se rompa acá se cuenta: en la pagina y en la consola.
    def do_GET(self):
        try:
            self.servir()
        except Exception:
            detalle = traceback.format_exc()
            sys.stderr.write("\\n  x se rompio al servir %s\\n%s\\n" % (self.path, detalle))
            try:
                self.responder(500, "Se rompio al servir %s\\n\\n%s\\n"
                               "Copiá esto entero: dice exactamente que fallo."
                               % (self.path, detalle))
            except Exception:
                pass

    def servir(self):
        ruta = self.path.split("?")[0]
        if ruta in ("/", "/index.html"):
            return self.responder(200, PAGINA, "text/html; charset=utf-8")
        if ruta in ("/app.js", "/paxmundi.js"):
            return self.responder(200, juego(), "text/javascript; charset=utf-8")
        if ruta in ("/runtime.js", "/react.js"):
            return self.responder(200, motor(), "text/javascript; charset=utf-8")
        if ruta == "/salud":
            return self.responder(200, json.dumps({"ok": True, "clave": bool(clave_api()),
                                                   "bytes": len(juego())}),
                                  "application/json; charset=utf-8")
        self.responder(404, "No hay nada en %s" % ruta)

    def do_POST(self):
        try:
            self.despachar()
        except Exception:
            detalle = traceback.format_exc()
            sys.stderr.write("\\n  x se rompio en %s\\n%s\\n" % (self.path, detalle))
            try:
                self.responder(500, json.dumps({"error": {"type": "roto", "message": detalle}}),
                               "application/json; charset=utf-8")
            except Exception:
                pass

    def despachar(self):
        if self.path.split("?")[0] != "/api/mensajes":
            return self.responder(404, "No hay nada en %s" % self.path)
        clave = clave_api()
        if not clave:
            return self.responder(503, json.dumps({"error": {
                "type": "sin_clave",
                "message": "Falta ANTHROPIC_API_KEY. El motor local no la necesita: "
                           "cambia el interruptor MOTOR a 'local' dentro del juego."}}),
                "application/json; charset=utf-8")
        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(largo) if largo else b"{}"
        pedido = urllib.request.Request(API_ANTHROPIC, data=cuerpo, method="POST",
            headers={"Content-Type": "application/json", "x-api-key": clave,
                     "anthropic-version": VERSION_API})
        try:
            with urllib.request.urlopen(pedido, timeout=120) as r:
                return self.responder(r.status, r.read(), "application/json; charset=utf-8")
        except urllib.error.HTTPError as e:
            detalle = e.read()
            sys.stderr.write("  x la API respondio %s: %s\\n"
                             % (e.code, detalle[:300].decode("utf-8", "replace")))
            return self.responder(e.code, detalle, "application/json; charset=utf-8")
        except Exception as e:
            sys.stderr.write("  x no se pudo llegar a la API: %s\\n" % e)
            return self.responder(502, json.dumps({"error": {"type": "sin_red", "message": str(e)}}),
                                  "application/json; charset=utf-8")


class Servidor(socketserver.ThreadingTCPServer):
    """Con hilos: si no, una llamada a la IA congelaria la pagina entera."""
    allow_reuse_address = True
    daemon_threads = True
    verboso = False


def mi_direccion():
    """La direccion de esta maquina en la red, para abrirla desde otro lado.

    No manda nada: abrir un socket UDP no habla con nadie, solo hace que el
    sistema elija por cual de sus placas saldria, y esa es la que sirve."""
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


def main():
    p = argparse.ArgumentParser(description="Pax Mundi en un solo archivo.")
    p.add_argument("-p", "--puerto", type=int, default=8000, help="puerto (por defecto 8000)")
    p.add_argument("--sin-navegador", action="store_true", help="no abrir el navegador solo")
    p.add_argument("--extraer", action="store_true", help="escribir paxmundi.js al lado y salir")
    p.add_argument("--probar", action="store_true",
                   help="revisar que todo lo de adentro sale bien, y salir")
    p.add_argument("--red", action="store_true",
                   help="atender tambien desde afuera de esta maquina "
                        "(emuladores, maquinas virtuales, otro aparato)")
    p.add_argument("--simple", action="store_true",
                   help="HTTP/1.0, una conexion por pedido: mas lento y mas compatible")
    p.add_argument("-v", "--verboso", action="store_true", help="mostrar cada pedido")
    args = p.parse_args()

    if args.simple:
        Manejador.protocol_version = "HTTP/1.0"

    if args.extraer:
        destino = Path(__file__).resolve().parent / "paxmundi.js"
        destino.write_bytes(juego())
        print("escrito %s (%.0f KB)" % (destino, destino.stat().st_size / 1024))
        return

    # ——— revision ———
    # Si el navegador dice "localhost no envio ningun dato", esto contesta por
    # que: levanta el servidor de verdad, se pide a si mismo cada cosa y dice
    # cual falla y con que error. Es una sola orden y se puede copiar entera.
    if args.probar:
        print("PAX MUNDI · revision")
        print("   python %s en %s" % (sys.version.split()[0], sys.platform))
        try:
            print("   el juego adentro: %.0f KB" % (len(juego()) / 1024))
            print("   el motor adentro: %.0f KB" % (len(motor()) / 1024))
        except Exception as e:
            print("   x no pude descomprimir lo de adentro: %s" % e)
            print("     el archivo pudo bajarse a medias. Bajalo de nuevo.")
            return
        import urllib.request as ur
        try:
            srv = Servidor(("127.0.0.1", args.puerto), Manejador)
        except OSError as e:
            print("   x no pude abrir el puerto %d: %s" % (args.puerto, e))
            print("     si el juego ya esta corriendo, pará ese y volvé a probar,")
            print("     o probá otro puerto: python3 paxmundi_solo.py --probar -p 8080")
            return
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = "http://127.0.0.1:%d" % args.puerto
        malas = 0
        for ruta in ("/", "/app.js", "/runtime.js", "/salud"):
            try:
                with ur.urlopen(base + ruta, timeout=20) as r:
                    cuerpo = r.read()
                print("   %-13s %s  %.0f KB" % (ruta, r.status, len(cuerpo) / 1024))
            except Exception as e:
                malas += 1
                print("   %-13s x %s" % (ruta, e))
        srv.shutdown()
        srv.server_close()
        if malas:
            print("\\n   Algo no sale. Copiá todo esto y mandalo: dice que ruta falla.")
            return
        print("\\n   Todo sale bien desde acá: el servidor sirve las cuatro cosas enteras.")
        print("   Si el navegador igual no muestra nada, el problema no es el archivo")
        print("   sino el camino entre Python y el navegador. Por orden:")
        print("     - El navegador, ¿corre del mismo lado que esto? Si Python esta en")
        print("       un emulador, una maquina virtual, un contenedor o WSL y el")
        print("       navegador esta afuera, '127.0.0.1' son dos sitios distintos y no")
        print("       se ven. Arranca con:  python3 paxmundi_solo.py --red")
        print("       y abri la direccion que te va a decir, no localhost.")
        print("     - Si aun estando del mismo lado no anda, proba:")
        print("       python3 paxmundi_solo.py --simple    (una conexion por pedido)")
        print("     - Y abri %s a mano, en vez de localhost." % base)
        return

    # Por defecto solo atiende a esta misma maquina, que es lo prudente: por
    # aca pasa la clave de la API. Con --red atiende a cualquiera que llegue,
    # que es lo que hace falta cuando el navegador esta de un lado y Python del
    # otro -un emulador, una maquina virtual, un contenedor, otro aparato-
    # porque ahi "127.0.0.1" son dos sitios distintos y no se ven.
    anfitrion = "0.0.0.0" if args.red else "127.0.0.1"
    try:
        servidor = Servidor((anfitrion, args.puerto), Manejador)
    except OSError as e:
        sys.exit("No pude abrir el puerto %d (%s).\\nProba con otro: "
                 "python3 paxmundi_solo.py -p 8080" % (args.puerto, e))
    servidor.verboso = args.verboso

    url = "http://localhost:%d/" % args.puerto
    print("PAX MUNDI")
    print("   un solo archivo, %.0f KB de juego dentro" % (len(juego()) / 1024))
    print("   %s" % url)
    if args.red:
        mia = mi_direccion()
        print("   desde otro aparato o desde afuera del emulador:")
        print("      http://%s:%d/" % (mia or "TU-IP", args.puerto))
        if clave_api():
            print("   ojo: asi lo alcanza cualquiera de tu red, y por aca pasa la clave.")
    if clave_api():
        print("   IA: clave encontrada (opcional; el motor local no la necesita)")
    else:
        print("   IA: sin clave. El motor local resuelve todo igual.")
    print("   Ctrl+C para parar\\n")

    if not args.sin_navegador:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\\n   Hasta la proxima.")
    finally:
        servidor.shutdown()
        servidor.server_close()


'''

COLA = '''
if __name__ == "__main__":
    main()
'''

salida = RAIZ / "paxmundi_solo.py"
salida.write_text(CABEZA + '# ' + '=' * 74 + '\n'
                  + '# El juego, comprimido con lzma y codificado en base85.\n'
                  + '# Se regenera con hacer_solo.py; no se edita a mano.\n'
                  + '# ' + '=' * 74 + '\n'
                  + 'JUEGO = """\\\n' + envuelto + '\n"""\n\n'
                  + '# Y el motor de pantalla, del mismo modo.\n'
                  + 'MOTOR = """\\\n' + envueltoM + '\n"""\n\n' + COLA, encoding="utf-8")
print("escrito %s (%.0f KB)" % (salida, salida.stat().st_size / 1024))

# ——— y se comprueba que lo escrito sirve ———
# La página va dentro de una cadena de Python que va dentro de otra cadena de
# Python. Un escape mal contado y lo que se sirve es JavaScript roto: el juego
# arranca igual, pero se queda sin el aviso que explica por qué no arrancó, que
# es justo cuando más falta hace. Ya pasó una vez; no vuelve a pasar callado.
import re, subprocess, tempfile
texto = salida.read_text(encoding="utf-8")
ini = texto.index('PAGINA = r"""') + len('PAGINA = r"""')
pagina = texto[ini:texto.index('"""', ini)]
bloques = re.findall(r"<script(?![^>]*importmap)[^>]*>(.*?)</script>", pagina, re.S)
assert len(bloques) >= 2, "la página perdió sus scripts"
for i, b in enumerate(bloques):
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False, encoding="utf-8") as f:
        f.write(b)
        ruta = f.name
    r = subprocess.run(["node", "--check", ruta], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("El script %d de la página no es JavaScript válido:\n%s"
                         % (i, r.stderr[:400]))
print("   la página que sirve: %d scripts, todos válidos" % len(bloques))
