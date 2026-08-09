#!/usr/bin/env python3
"""Arma conquista.html: la plantilla más los contornos de los Pirineos.

El banco de pruebas de la conquista se abre solo, sin servidor y sin el juego
al lado, así que los contornos van dentro del propio archivo. Se editan la
plantilla o los datos y se vuelve a correr esto.
"""
import json, pathlib, sys

aqui = pathlib.Path(__file__).parent
plantilla = aqui / "conquista_demo.html.plantilla"
datos = aqui / "pirineos.json"
salida = aqui / "conquista.html"

if not plantilla.exists() or not datos.exists():
    sys.exit("falta la plantilla o los contornos")

t = plantilla.read_text(encoding="utf-8")
a, b = t.index("/*DATOS*/"), t.index("/*FIN*/") + len("/*FIN*/")
d = json.loads(datos.read_text(encoding="utf-8"))
salida.write_text(t[:a] + json.dumps(d, separators=(",", ":"), ensure_ascii=False) + t[b:],
                  encoding="utf-8")
print(f"escrito {salida} ({salida.stat().st_size // 1024} KB, {len(d)} comarcas)")
