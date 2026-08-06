# Pax Mundi

Juego de gran estrategia histórica: gobernás una nación desde la Antigüedad
hasta hoy, con las 4.594 provincias reales del mundo sobre un mapa navegable.

## Cómo correrlo

Lo más simple, y lo que anda en todos lados: abrir `paxmundi.html` en el
navegador. Doble clic y listo. No hace falta Python, ni servidor, ni internet:
el juego entero está adentro de esa página.

Es la única manera que funciona en un Python online, en una app de teléfono o
en cualquier sandbox donde no se pueda abrir un puerto. Lo único que no tiene
es el motor de IA, porque eso sí necesita un servidor que guarde la clave; el
motor local hace todo lo demás igual.

Si preferís levantarlo como servidor —y así tener también el motor de IA—, con
un solo archivo y nada más al lado:

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

## Si el navegador no muestra nada

Antes que nada: si lo que falla es el servidor, probá `paxmundi.html`. Sin
servidor no hay nada que pueda fallar entre Python y el navegador, que es
donde están casi todos estos problemas.

Y si querés el servidor igual: arranca pero la pestaña queda en blanco, o dice
«localhost no envió ningún dato» (`ERR_EMPTY_RESPONSE`). Preguntale al propio
archivo qué le pasa:

```
python3 paxmundi_solo.py --probar
```

Levanta el servidor de verdad, se pide a sí mismo cada cosa que la página
necesita y dice cuál falla y con qué error. `paxmundi.py --probar` hace lo
mismo con los archivos sueltos. Sale una tabla corta que se puede copiar
entera.

Si la revisión dice que todo sale bien, el archivo no tiene nada roto: lo que
falla es el camino entre Python y el navegador.

**El caso más común: no corren del mismo lado.** Si Python corre dentro de un
emulador, una máquina virtual, un contenedor o WSL, y el navegador está afuera,
`127.0.0.1` no es el mismo sitio para los dos: cada uno tiene el suyo y no se
ven. Por defecto el servidor solo atiende a su propia máquina, así que desde
afuera no hay nadie. Se arregla abriéndolo:

```
python3 paxmundi_solo.py --red
```

Al arrancar te dice la dirección con la que llegar desde afuera —algo como
`http://192.168.1.40:8000/`—. Esa es la que hay que abrir, no `localhost`.

Con `--red` cualquiera de tu red puede abrir el juego. Sin clave de la API no
hay nada que perder; con clave, tené en cuenta que las llamadas a la IA pasan
por ahí.

Si están del mismo lado y aun así no anda, hay intermediarios que se llevan mal
con las conexiones reutilizadas:

```
python3 paxmundi_solo.py --simple
```

Una conexión por pedido: algo más lento y mucho más compatible.

Y como último recurso, probá con otro navegador, o abrí `http://127.0.0.1:8000`
a mano en vez de `localhost`.

## La partida se guarda sola

Al terminar cada turno, y también cuando dejás el juego —cambiás de pestaña,
de aplicación, o cerrás—. Ese último momento es el que importa en un teléfono:
el sistema descarta la página sin avisar, y sin eso la campaña se perdería.

Al volver a abrir, arriba de todo aparece **seguir con \<tu nación\>**, con el
año, el turno y cuánto hace que la dejaste.

Dentro del juego, el botón **💾 PARTIDA** de la barra de arriba tiene lo que
decidís vos: tres copias aparte —para dejar una antes de una guerra que puede
salir mal— y bajar la partida a un archivo.

Ese archivo sirve para llevártela a otro aparato: la bajás en uno y la traés en
el otro con «traer una partida de un archivo», abajo de la pantalla de
fundación. Es también la manera de que no se pierda si el navegador limpia lo
suyo.

Una partida ocupa unos 200 KB y se guarda en el navegador, así que es de ese
navegador y de ese aparato. El juego está en desarrollo: cuando cambia la forma
de la partida, las guardadas de antes dejan de servir, y el juego lo dice en vez
de cargarlas a medias y romperse tres turnos después.

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
| `runtime.js`   | El motor de pantalla: lo que el juego usa de React, escrito acá. |
| `paxmundi.py`  | El servidor local: sirve el juego y hace de intermediario con la API. |
| `paxmundi_solo.py` | Todo lo anterior en un único archivo: el juego va comprimido dentro. |
| `paxmundi.html` | El juego en una sola página, sin servidor: se abre a mano. |

`paxmundi.html` no puede ser un módulo ES como el resto: abiertos con `file://`
los módulos los bloquea el propio navegador por CORS. Por eso se arma aparte,
como un guion clásico —un IIFE— que sí anda desde un archivo suelto.

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

## No se baja nada de afuera

Ni una sola cosa. El juego arranca sin internet, detrás de un proxy, en una
máquina aislada o en un avión.

Hasta hace poco React se bajaba de un CDN la primera vez, y eso convertía un
juego que cabe en un archivo en uno que no arranca sin conexión —y que, con el
CDN bloqueado, no arranca nunca—. `runtime.js` es ese trozo, escrito acá: los
cuatro ganchos que el juego usa (`useState`, `useRef`, `useEffect`, `useMemo`),
lo que escribe el compilador de JSX (`jsx`, `jsxs`, `Fragment`) y `createRoot`.
Nada más. Ni contextos, ni reductores, ni portales: lo que no está no puede
fallar.

Reconcilia como React —compara el árbol nuevo con el puesto y toca solo lo que
cambió— y, sobre todo, se salta los trozos que siguen siendo el mismo objeto,
que es lo que devuelve un `useMemo`. Ese atajo es la mitad del rendimiento del
mapa.

La única llamada a la red que puede hacer el juego es a la API de Anthropic
para que la IA narre, y solo si le diste una clave. Sin clave no sale ni un
paquete.
