#!/usr/bin/env python3
"""Rehace todo lo que se genera a partir de paxmundi.jsx.

    python3 armar.py

El único archivo que se edita es paxmundi.jsx. De ahí salen los tres que se
reparten, y ninguno se toca a mano:

    paxmundi.js         el juego traducido a JavaScript común
    paxmundi.html       el juego en una página sola, sin servidor
    paxmundi_solo.py    el juego dentro de un único archivo de Python

Después de tocar el juego, correr esto. Si no, lo que se reparte sigue siendo
el de antes: es la manera más fácil de perder una tarde persiguiendo un
cambio que sí estaba hecho.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def paso(titulo, orden, **extra):
    print("· %s" % titulo)
    r = subprocess.run(orden, cwd=RAIZ, capture_output=True, text=True, **extra)
    salida = (r.stdout or "") + (r.stderr or "")
    for linea in salida.strip().splitlines():
        print("    %s" % linea)
    if r.returncode:
        sys.exit("\n✗ falló: %s" % titulo)
    return salida


def main():
    if not (RAIZ / "paxmundi.jsx").exists():
        sys.exit("No encuentro paxmundi.jsx en %s" % RAIZ)

    # 1 · el paquete como módulo ES, que es lo que sirve paxmundi.py y lo que
    #     va comprimido dentro de paxmundi_solo.py.
    paso("paxmundi.js — el juego traducido",
         ["bun", "build", "paxmundi.jsx", "--format=esm", "--minify", "--production",
          "--outfile=paxmundi.js",
          "--external", "react", "--external", "react/jsx-runtime",
          "--external", "react-dom/client"])
    print("    %.0f KB" % ((RAIZ / "paxmundi.js").stat().st_size / 1024))

    # 2 · la página sola. Va aparte porque no puede ser un módulo: abiertos con
    #     file:// los bloquea el navegador, así que se arma como guion clásico.
    paso("paxmundi.html — la página sin servidor", [sys.executable, "hacer_pagina.py"])

    # 3 · el archivo único de Python, que lleva adentro el .js y el motor.
    paso("paxmundi_solo.py — el archivo único", [sys.executable, "hacer_solo.py"])

    print("\nListo. Los tres al día con paxmundi.jsx.")


if __name__ == "__main__":
    main()
