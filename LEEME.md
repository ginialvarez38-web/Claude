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

## En el teléfono

El juego se acomoda solo. En una pantalla angosta —menos de 640 px— el panel
de la derecha deja de ser una columna y sube desde abajo tapando poco más de la
mitad: un panel lateral es una idea de escritorio, y en vertical partía el mapa
al medio. Los avisos arrancan plegados, la cabecera va en dos filas para que el
tesoro no quede reducido a una astilla, y el mapa se encuadra sobre lo que se
ve de él y no sobre la pantalla entera, que era como el reino terminaba
escondido detrás del panel.

Los botones crecen a 36 px donde se toca con el dedo —lo decide el tipo de
puntero, no el tamaño de la pantalla: un teléfono apaisado mide 844 de ancho y
el dedo sigue midiendo lo mismo—. Con ratón se quedan compactos.

En apaisado y en tablet no cambia nada: ahí los paneles laterales entran bien.

### Mandar el ejército con el dedo

Tocás el escudo de la hueste y queda elegida —abajo aparece de cuál se trata y
qué se espera de vos—; tocás en el mapa a dónde tiene que ir y salen las
órdenes que caben ahí: marchar, cercar la plaza, asaltarla. Tocás el escudo de
nuevo y la soltás.

Todo lo demás del mapa —declararle la guerra al vecino, mirar una comarca,
mudar la corte— sale dejando el dedo apretado medio segundo sobre el sitio. Es
la misma rueda que con ratón abre el clic derecho.

Durante un tiempo nada de esto se podía hacer con el dedo: la rueda solo se
abría con el clic derecho o con la tecla `M`, y encima el clic que el navegador
manda al levantar el dedo caía sobre el fondo de la rueda recién abierta y la
cerraba antes de que se viera. El juego estaba entero y no era jugable en un
teléfono, que es donde se juega.

## Un banco de pruebas para el frente

`conquista.html` es un archivo aparte, y es solo eso: los Pirineos de verdad
—72 comarcas con su contorno y su terreno, sacadas del mapa del juego— partidos
en palmos de tierra de seis kilómetros, y dos bandos empujando. Sin economía,
sin turnos, sin nada más. Se abre a mano igual que el juego.

Sirve para decidir cómo se pelea y cómo se ve antes de meterlo en el juego, que
es donde una cosa así se pierde entre todo lo demás.

**Nadie dibuja el frente.** Cada palmo tiene dueño y cambia de dueño cuando el
de enfrente aprieta más, y solo si el que aprieta ya tiene el palmo de al lado.
De esa única regla salen las tres cosas que hacen que parezca una guerra:

- **La anexión entra por un costado.** El color nace donde están las botas y se
  extiende desde ahí; la capital de la comarca es de lo último que cae, no de
  lo primero.
- **Salientes.** Una hueste solo aprieta el trecho que tiene delante —unos
  cincuenta kilómetros—, así que donde hay ejército se mete una lengua y el
  resto de la línea se queda quieto.
- **Bolsas.** Dos avances que se cruzan por detrás dejan un trozo suelto. No
  hay ninguna regla que diga «si está rodeado, cae»: cae porque se le corta lo
  que lo sostenía, y si nadie va a socorrerlo se rinde de hambre en un par de
  meses. Mientras se apaga, se va poniendo gris.

Dos cosas más que no son adorno y cambian toda la partida: por tierra
conquistada uno se abastece peor que por la propia —de ahí que toda ofensiva se
frene sola cuando se aleja demasiado—, y el enemigo contraataca: sus huestes van
a donde más terreno perdieron y lo recuperan si te fuiste de ahí.

Los mandos: velocidad y pausa, tamaño del palmo, lo irregular del frente,
cuántas huestes de cada bando y de qué tamaño, si el enemigo contraataca o se
queda quieto, y una cámara que sigue a la hueste elegida —de lejos no se ve
nada, esa es media cuestión—.

Lo que ahí se decida es lo que después va al juego. Las reglas están copiadas a
mano en el propio archivo para que se abra solo, sin nada al lado, y
`armar_conquista.py` lo rearma desde la plantilla y los contornos.

## Conquistar se ve en el mapa

Una comarca no cambia de dueño de golpe. El ejército entra por un lado y va
ganando campo, y eso es exactamente lo que el mapa pinta: el color crece desde
donde entró la hueste, recortado contra el contorno de verdad de la comarca,
así que se derrama por el valle y se para en la costa como se pararía una
tropa. Lo que está pintado es lo que está tomado.

En medio queda la plaza, del color de quien todavía la tiene, y ahí es donde
termina el asunto: la comarca puede estar entera en tus manos y el castillo
seguir sin rendirse. Cuando cae, la comarca pasa a ser del reino —con su
contorno real, la mitad de su gente y la lealtad por el suelo, que es como
entra una comarca conquistada—.

Lo que tarda depende de lo que hay que tomar, no de un número fijo: una comarca
grande lleva mucho más que una chica, la montaña mucho más que la llanura, y un
ejército con cañones a rastras avanza al paso de los cañones. Ocupar la Guayana
lleva más de cien días; París, ocho.

Y el cerco solo cuenta mientras la plaza está de verdad rodeada. Sitiar una
ciudad por un lado y dejarle el otro abierto no es sitiarla: es acamparle
enfrente y verla comer. Por eso conviene tomar el campo antes de sentarse
delante del muro. Si el ejército levanta el campamento y se va, lo tomado se
va perdiendo solo: el campo vuelve a su dueño, aunque mucho más despacio de lo
que se ganó.

Con el turno de un año —el que viene puesto— la campaña entera se resuelve
entre dos pantallas y no hay nada que mirar. Poné el turno en un mes o en una
semana, arriba en el consejo, y se ve avanzar.

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

**Si el navegador no deja guardar**, el juego lo dice en la portada y el botón
de arriba pasa a decir «⚠ NO SE GUARDA» en rojo. Pasa abriendo el archivo a
mano en Safari, y en las ventanas de navegador que abren otras aplicaciones
desde un mensaje. Se puede jugar igual: lo que hay que hacer es bajar la
partida a un archivo antes de irse, y traerla la próxima vez. Cuando el
almacén del navegador está bloqueado pero el de la pestaña no, la partida
aguanta mientras esa pestaña siga abierta —sobrevive a recargar, no a cerrar—
y el aviso lo aclara.

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
