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

Todo esto ya está en el juego —ver «La guerra se ve en el mapa»—, y el banco de
pruebas se queda para lo que venga: es mucho más rápido probar una idea de
frente acá que dentro de una partida. Las reglas están copiadas a mano en el
propio archivo para que se abra solo, sin nada al lado, y `armar_conquista.py`
lo rearma desde la plantilla y los contornos.

## La guerra se ve en el mapa, palmo a palmo

Cuando hay guerra, el mapa se parte en palmos de tierra de unos siete
kilómetros y cada palmo tiene dueño. Un palmo cambia de dueño cuando el de
enfrente aprieta más, y solo si el que aprieta ya tiene el palmo de al lado o
lo tiene bajo las botas. **Nadie dibuja el frente**: sale de los empujones, y
por eso se comporta como un frente.

- **La anexión entra por un costado.** El color nace donde están las botas —si
  la hueste cruzó la frontera, en la frontera— y la capital de la comarca es de
  lo último que cae, no de lo primero.
- **Salientes.** Una hueste aprieta el trecho que tiene delante, unos cincuenta
  y ocho kilómetros, y no más. Donde hay ejército se mete una lengua; el resto
  de la línea se queda quieto.
- **Bolsas.** Lo que queda cercado y sin nadie que lo socorra se rinde de
  hambre en un par de meses, y mientras se apaga se va poniendo gris. No hay
  ninguna regla que diga «si está rodeado, cae»: cae porque se le corta lo que
  lo sostenía. Si llega una hueste suya a romper el cerco, deja de estar
  perdido y el juego lo sabe.

Debajo hay un campo de fuerza por bando que nace en las huestes y en las plazas
y se propaga de palmo en palmo perdiendo por el camino: poco por tierra propia,
mucho por la del otro, y bastante por la conquistada —la gente no es tuya, los
caminos los cortan, cada convoy necesita escolta—. De ahí sale sola la
**culminación**: toda ofensiva se frena cuando se aleja de su tierra.

Y de ahí sale la vuelta del otro. **La tierra ocupada resiste por su cuenta**,
en todos sus palmos: es la gente de ahí, que no se fue a ninguna parte. Si
levantás el campamento y te vas, lo tomado se pierde solo. Para conservar una
conquista hay que dejarle tropa encima o tomar la plaza y quedársela. Y las
huestes del vecino ya no van a tu capital: van al desgarrón más grande que
tengan a mano, a recuperar lo suyo.

Un cerco solo cuenta mientras la plaza está de verdad rodeada: sitiarla por un
lado y dejarle el otro abierto es acamparle enfrente y verla comer. Los días de
cerco valen lo que valga el cerco, así que una plaza mal sitiada aguanta
muchísimo más.

Al caer la plaza, la comarca pasa a ser del reino con su contorno de verdad, la
mitad de su gente y la lealtad por el suelo, que es como entra una comarca
conquistada.

Con el turno de un año —el que viene puesto— la campaña entera se resuelve
entre dos pantallas. Poné el turno en un mes o en una semana, arriba en el
consejo, y se ve avanzar.

El teatro se arma solo sobre la caja donde se pelea, no sobre el mundo entero
—serían veintidós millones de palmos—, y el palmo se agranda si la caja es
enorme, así que la cuenta no se dispara aunque la guerra sea entre imperios. En
la partida guardada va solo el dueño de cada palmo, comprimido por tramos:
treinta y cinco mil palmos ocupan tres mil letras.

## El ejército come, gasta y se queda sin nada

Ninguna hueste puede pelear indefinidamente. Cada una necesita pan y pertrechos
todos los días: cien jinetes comen tres veces lo que cien de a pie —el caballo
también come— y la artillería casi no come pero gasta a paladas.

Lo que le llega sale del reino y viaja por sus caminos. Cada comarca puede
mandar lo que le permiten su calzada, su terreno, su costa y su gente; el
grueso parte de la corte, que es el depósito, y se va perdiendo con la
distancia: poco por tierra propia, bastante por la recién conquistada —la gente
no es tuya, los caminos los cortan— y casi nada por la del otro, salvo las
pocas leguas que el tren de suministro sigue a la tropa.

De ahí salen tres cosas que se sienten al jugar:

- **Cruzar la frontera es gratis; meterse hondo, no.** Una hueste pegada a su
  raya recibe todo. A media Francia ya no le llega nada, y una campaña metida
  en el fondo se deshace sin que nadie la ataque: pierde gente, pierde moral y
  pelea a un tercio de lo que pesa.
- **Un ejército más grande que el país no se puede alimentar.** No arruina el
  granero: se muere de hambre encima de él.
- **Del granero sale lo que la cosecha no cubre.** Un ejército que el país
  puede mantener no vacía la despensa; la vacía el que lo sobrepasa, y eso se
  siente en el pan de todos.

En la sección de campaña, cada hueste dice cómo está —«abastecida» o «abasto
41% · el camino no da para tanto»— y en el mapa lleva un aro roto alrededor
cuando le falta. Las bajas por hambre se cuentan en la crónica con su motivo.

Y el cerco mide lo que tiene que medir: no cuánto de la comarca tenés, sino
cuánto del campo alrededor de la plaza. Para bloquear una ciudad hay que
cortarle los caminos, no ocupar el departamento entero.

## Lo que le enseñaron a la tropa y lo que vivió

Son dos cosas distintas y el juego las lleva por separado, porque la diferencia
entre ellas es la mitad de la historia militar del mundo.

La **instrucción** es lo que el reino le puso encima a su tropa antes de que
sonara un tiro: formar, cargar, marchar de noche, obedecer a un sargento al que
no se conoce. Se compra, y se compra en la paz. En la ficha del ejército se
elige el plan —ninguno, revista de armas, escuela de cuadros, maniobras de
campaña—, cada uno con su precio al año por unidad y su techo. Sube unos pocos
puntos por año: un plan puesto el día que se declara la guerra no llega a
tiempo a nada. Y baja si se deja de pagar, o cada vez que entra una leva nueva:
duplicar el ejército de golpe hunde la instrucción media, que es exactamente lo
que le pasa a todo el que moviliza en vísperas.

Los planes de arriba piden que haya quien los dé. Sin cuadro de oficiales no
hay escuela de cuadros, y decretar maniobras de estado mayor en el siglo XIII
no hace absolutamente nada.

La **veteranía** no se compra en ningún lado. Se gana afuera: en batalla —lo
que más enseña—, en un asalto, sentado delante de una plaza, y simplemente
marchando, porque montar y levantar el campamento todos los días sin perder a
nadie por el camino es la mitad del oficio. La primera batalla enseña más que
la décima.

Una hueste veterana vale por tres, y no por un solo motivo:

- pesa bastante más en el campo, y a igualdad de hombres le gana dos de cada
  tres veces a una leva;
- pierde una fracción de la gente cuando pelea, y cuando la derrotan se retira
  en orden en vez de dejarse media hueste por el camino;
- no se le rompe la moral;
- y no se deshace cuando se acaba el pan. Cuatro meses sin abasto disuelven a
  una leva y dejan casi entera a la que se conoce: no los mata el hambre, se
  van.

**Y se pierde.** Mientras las bajas sean las de una campaña, la hueste se
curte. Cuando pasan de uno de cada seis empieza a faltar el que sabía, porque
los veteranos van delante, y eso no vuelve con reemplazos. Un asalto que entra
perdiendo a cinco de cada diez deja la plaza tomada y el ejército que la tomó
ya no existe. Una batalla pareja desgasta aunque se gane: un ejército que gana
todo el tiempo también se gasta.

Lo único que un reino se queda de una guerra es lo que aprendieron los que
vuelven. Licenciar a casa una hueste curtida sube la instrucción de todo el
ejército: los veteranos se reparten por los cuarteles y enseñan.

En el mapa cada escudo lleva sus galones —una, dos o tres barras— y en la
sección de campaña cada hueste dice lo que es con una palabra: bisoños,
instruidos, hechos, curtidos, la vieja guardia.

## Lo que se sabe no es lo que hay

Antes la guerra se veía desde arriba y desde afuera: la hueste enemiga estaba
en el mapa con su nombre y su número exacto desde el primer día. Eso no es un
juego de guerra, es ajedrez con terreno. Ahora hay niebla.

Lo que **no** se esconde es el mundo. La geografía no es un secreto —los mapas
existían, y un rey de Castilla sabía perfectamente dónde queda Burdeos—. Lo que
es secreto es lo de hoy: dónde está el ejército del otro, cuánto trae, y hasta
dónde llegó el frente esta semana.

**Ver y enterarse son dos cosas distintas**, y el juego las lleva aparte porque
la historia las llevó aparte:

- **Ver** es hasta dónde alcanza la vista de una tropa. Lo que la estira no es
  el número de soldados sino la caballería ligera —para eso servía—, y después
  el catalejo, el globo, el aeroplano y el radar. Una hueste ve lo que ve su
  mejor ojo, no su peor pie: alcanza con mandar los jinetes por delante. Y una
  tropa bisoña explora peor, porque reconocer es lo más difícil que se le puede
  pedir a alguien que acaba de llegar.
- **Enterarse** es cuánto tarda lo que alguien vio en llegar a quien manda. En
  1200 una noticia camina a caballo: lo que pasa a quinientos kilómetros se
  sabe en la corte nueve días después. Con el telégrafo, en el acto. Esa
  diferencia es media guerra.

De ahí salen cuatro cosas que se sienten al jugar:

- **Del enemigo hay partes, no huestes.** El escudo que ves en el mapa está
  donde se lo vio por última vez, con el número que alguien dijo. Un parte
  fresco es exacto; uno de lejos redondea a lo grueso y se equivoca. Mientras
  tanto el ejército de verdad sigue andando: el mapa enseña un fantasma. El
  escudo se desvanece y se dibuja a trazos según lo viejo que sea, y pasado un
  año se olvida.
- **Se ve lo que se pisa y lo que se alcanza a mirar desde donde se pisa.** El
  suelo propio se conoce entero —ahí vive gente que avisa— y un poco más allá
  de la raya. El resto es lo que alcancen tus tropas, y se desdibuja en una
  estación si no vuelve nadie a mirar.
- **Una comarca puede caer sin que te enteres.** El mapa pinta lo que el reino
  cree. Una conquista tuya a quinientos kilómetros que el vecino recupera sigue
  saliendo tuya, con el color cada vez más apagado, hasta que mandás a alguien
  a ver. El parte de guerra dice cuánto del teatro se conoce y cuánto no.
- **Asaltar es apostar.** De una plaza ajena no se sabe lo que aguanta: se
  estima, y de lejos se estima mal. Los rótulos lo dicen —«aguantará unos 75
  días», «al parecer 76 de cada 100»— y dejan de decirlo cuando llevás tiempo
  sentado enfrente, porque un cerco es también un reconocimiento largo.

Y vale para los dos lados: un ejército enemigo no sale derecho a buscar una
hueste tuya que está a cuatrocientos kilómetros y de la que nadie le dijo nada.

## Cuánto puede llevar un solo hombre

Lo que cambió en dos mil años de guerra no es cuántos hombres podía levantar un
país. Es cuántos podía mover a la vez sin que se le deshicieran por el camino.
Un rey medieval con cuarenta mil hombres tenía cuarenta mil hombres y un
problema; Napoleón con cuarenta mil tenía cuatro divisiones.

La ficha del ejército dice en qué escalón está el reino —la mesnada, la
ordenanza, el regimiento, la división, el cuerpo de ejército, el grupo de
ejércitos— y cada uno da dos números:

- **Bulto**: cuántas unidades aguanta una hueste antes de estorbarse a sí
  misma. Pasado eso marcha la mitad, come casi el doble por cabeza —el forraje
  del camino se lo comieron los de adelante— y no llega a poner en el campo
  todo lo que trae. De las tres, la del combate es la más leve: los ejércitos
  demasiado grandes se murieron más de hambre y de camino que de tiros.
- **Mando**: cuántas huestes puede un general llevar al mismo campo el mismo
  día. Ese número es literal: en 1200 es una, y por eso dos huestes tuyas que
  estén al lado pelean una después de la otra y las deshacen por separado. Con
  disciplina de formación son dos, y con estado mayor, seis.

Ninguno viene por el año que es: cada escalón hay que saberlo.

**Poner en pie de guerra reparte.** Si lo que tenés libre no entra en una
hueste, salen varias, cada una con de todo —media hueste de solo cañones no es
media hueste— y con su jefe. También se puede partir una a mano en cualquier
momento.

**El general es la estructura.** Cada hueste lleva el suyo, y se reparten
solos: nadie quiere administrar esto turno a turno. Una hueste sin jefe se
conduce sola y se nota; una con un jefe de oficio pesa más en el campo; un
general muerto no sigue mandando desde la tumba. Y un general estirado —con más
huestes de las que su época le deja— deja de servir de mucho, aunque nunca es
peor que no tener ninguno.

Lo que se compra con todo esto es **concentrar**. Dos huestes con el mismo jefe
que llegan al mismo campo pelean juntas, y eso suele ser la diferencia entre
perder y ganar la misma batalla. Por eso partir el ejército conviene cuando hay
quien mande las partes, y no antes: en 1200 sesenta unidades son tres mesnadas
de las que al campo llega una sola, y por eso los reyes medievales iban en un
solo bulto.

Y de paso se corrigió algo que estaba al revés desde siempre: **a un ejército no
se lo destruye en la batalla, se lo destruye en la persecución**. Antes una
batalla pareja costaba más bajas al vencido que una aplastante, que es lo
contrario de lo que pasó siempre. Cannae y Austerlitz fueron aniquilaciones
porque fueron desparejas; Borodino y Malplaquet dejaron dos ejércitos rotos en
el campo porque estuvieron parejas.

`MILICIA.md` tiene el mapa completo de lo que falta del sistema militar y en
qué orden conviene hacerlo.

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
