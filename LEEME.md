# Pax Mundi

Juego de gran estrategia histórica: gobernás una nación desde la Antigüedad
hasta hoy, con las 4.594 provincias reales del mundo sobre un mapa navegable.

## Cómo correrlo

Con un solo archivo, sin nada más al lado:

```
python3 paxmundi_solo.py
```

O, si querés el código suelto para editarlo, con los tres archivos juntos:

```
python3 paxmundi.py
```

Se abre solo en el navegador. Necesita Python 3.8 o posterior y nada más —no
hay que instalar nada con pip, ni node, ni compilar.

Si el puerto 8000 está ocupado: `python3 paxmundi.py -p 8080`.

## Para que la IA funcione

La IA es **opcional**. El motor local resuelve los turnos, entiende las órdenes
que escribas en castellano y narra la crónica sin salir a ninguna red. El
interruptor MOTOR, debajo del campo de órdenes, elige cuál de los dos escribe.

Si querés probar el de la IA hace falta una clave de la API de Anthropic:

```
export ANTHROPIC_API_KEY=sk-ant-...        # Linux y macOS
set ANTHROPIC_API_KEY=sk-ant-...           # Windows (cmd)
```

Sin clave no falta nada: se juega entero con el motor local.

La clave se queda en el servidor local. El navegador nunca la ve: las llamadas
a la API salen desde Python, que además resuelve el CORS que le impediría al
navegador llamar directamente.

## Los archivos

| | |
|---|---|
| `paxmundi.jsx` | El juego. Un solo archivo, y es el que se edita. |
| `paxmundi.js`  | El mismo juego ya traducido a JavaScript común. |
| `paxmundi.py`  | El servidor local: sirve el juego y hace de intermediario con la API. |
| `paxmundi_solo.py` | Todo lo anterior en un único archivo: el juego va comprimido dentro. |

`paxmundi.js` está para que arranque al instante sin depender de Babel. Si
editás `paxmundi.jsx`, el servidor nota por la fecha que el `.js` quedó viejo
y pasa solo a traducir en el navegador: editás, recargás, y ves tus cambios.
Cuando quieras volver al arranque rápido, regenerá el `.js`:

```
npx esbuild paxmundi.jsx --bundle --format=esm --outfile=paxmundi.js \
    --external:react --external:react/jsx-runtime --external:react-dom/client
```

`paxmundi_solo.py` lleva el juego comprimido con lzma en base85 dentro del
propio archivo. Se regenera desde `paxmundi.js` y no se edita a mano; con
`--extraer` vuelve a escribir el `paxmundi.js` original, byte por byte.

## Lo único que se baja de afuera

React, desde un CDN, la primera vez (después queda en la caché del navegador).
Si estás sin conexión o detrás de un cortafuegos que lo bloquea, el juego no
puede arrancar y la página te lo dice en vez de quedarse en blanco.
