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

La vara con la que se miden las dos fuerzas estuvo mucho tiempo mal puesta, y
mal puesta de una manera que no se veía: una comarca cualquiera proyectaba
sobre cada palmo de su campo la defensa entera de su plaza —muros, ciudad y
toda la gente que puede subirse a ellos—, que es el número de un asedio y no el
de una batalla en campo abierto. Contra eso hacían falta sesenta unidades para
mover un solo palmo, y un reino de 1200 puede poner siete. No existía el
ejército medieval capaz de invadir a su vecino, que es media historia de
Europa.

Ahora la vara dice otra cosa: **lo que para a un ejército es otro ejército.**
Una comarca sola resiste, cuesta y hace lenta la conquista, pero no la impide.
Ocho unidades —lo que ese siglo levanta de verdad— arañan el frente sin ganarlo;
veinte toman una comarca vacía en unos meses y se estrellan si hay tropa
encima; y hace falta más del doble para pasar por arriba de las dos cosas.

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

### La otra manera de saber

Mirar tiene un límite físico: se ve hasta donde llega la vista de alguien que
está ahí. Por eso todos los estados pagaron siempre por el otro camino. Una
**red de espías** no es un ejército invisible: es gente que vive allá
—mercaderes, frailes, secretarios mal pagados— y que cuenta cosas tarde,
incompletas y a veces falsas.

Se monta contra un vecino desde la ficha del ejército, cuesta al montarla y
cuesta todos los años. Y es exactamente lo contrario de un explorador: **poco
detalle sobre mucho territorio.** Un jinete encima de un ejército enemigo te
dice cuántos son; una red te dice que pasaron por ahí y te da un número redondo
y equivocado —dice veinte donde hay treinta— pero te lo dice de todo el país a
la vez, incluso donde no tenés una sola tropa. Las dos cosas se suman en vez de
sustituirse.

Tarda años en servir: empieza en diez y sube unos puntos por año hasta el techo
que su siglo permite, que en 1200 son cuatro frailes y en 1950 un servicio con
presupuesto. Si se deja de pagar, en cinco años no queda nadie. Y se puede
descubrir —más cuanto mejor sea, y el doble en guerra, porque en guerra la
buscan de verdad—: cuando pasa, la red se deshace y lo pagás en las
cancillerías.

### Y hacerles creer

Una red que solo escucha está a medio usar. La otra mitad —la que ganó más
batallas— es meter en la cabeza del otro algo que no es cierto. Hay dos
engaños, porque son los dos únicos que cambian lo que el otro hace:

- **El señuelo**: hacerles ver un ejército donde no hay ninguno. Se pone con el
  clic derecho en el sitio del mapa donde tienen que creer que hay algo. Si
  cuaja, van para allá y se pasan la campaña mirando un campo vacío.
- **El velo**: que no vean el que sí está. Se pone sobre una hueste desde su
  ficha. Si cuaja, para ellos esa hueste no existe y pasan de largo.

Los dos se pagan en oro y sobre todo **quemando la red**: un contacto que se
usa para mentir es un contacto que ya no sirve para escuchar, así que engañar
cuesta saber. Y los dos **pueden no cuajar** —con una red muy buena funcionan
unas cinco de cada seis; con una apenas suficiente, dos de cada tres—.

Lo importante es que **desde casa no se puede saber cuál cuajó.** La ficha
lista los engaños en pie y cuántos días les quedan, y nada más; si picaron o no
se sabrá por lo que hagan ellos, que es exactamente como fue siempre. Un rumor
dura lo que dura: pasada la fecha alguien va a mirar, no hay nada, y se acabó.

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

## De la mina al cañón

Hasta ahora los pertrechos salían de la nada: el ejército gastaba munición y el
reino la cubría con población y caminos, igual que el pan. Para el pan está
bien —lo hace el campo, y el campo está en todas partes—. Para todo lo demás
está mal: una lanza no la hace un labrador, la hacen una mina, una fundición y
un taller, en ese orden, y si falta cualquiera de los tres no hay lanza por
mucha gente que haya.

**La cadena produce lo que deja pasar su eslabón más angosto**, y no el
promedio. De esa única regla sale todo lo demás, incluido lo más importante:
ensanchar el eslabón que no aprieta no produce ni un pertrecho más. La ficha
del ejército dice cuál es el que aprieta, porque es lo único que sirve
arreglar.

- **La mina.** Un yacimiento no es producción: es la posibilidad de producción.
  Hace falta gente que pique y camino para sacarlo, la mena se agota, y de una
  mina ocupada por el enemigo no sale casi nada. Es el eslabón que más crece
  con el siglo: entre picar con azada y volar un frente con dinamita y sacarlo
  en vagonetas hay dos órdenes de magnitud.
- **La fundición.** Antes de la hulla se fundía con carbón vegetal, así que el
  techo de la siderurgia europea durante mil años no fue el mineral sino la
  leña: las ferrerías se comían el bosque y se mudaban. Con carbón de piedra
  ese techo desaparece de golpe, porque la hulla viaja y el bosque no.
- **La maestranza.** Una barra de acero no dispara. Los talleres viven en las
  ciudades, y lo que multiplica un arsenal no es el acero sino cómo se organiza
  el taller: piezas intercambiables, fábrica, cadena de montaje. Ahí está la
  diferencia entre mil fusiles al año y mil por día, y no en el metal, que es
  el mismo.

Entre 1200 y 2000 la cadena de un mismo país se multiplica por veinticinco, y
el escalón más grande está entre 1870 y 1940: ahí se armaron los ejércitos de
masas.

**El pan y los pertrechos se cuentan aparte**, porque salen de sitios distintos
y se acaban en momentos distintos. Setenta unidades en la Castilla de 1200
comen el cien por cien y se arman el doce: un reino medieval podía alimentar
perfectamente un ejército que no podía equipar, y ahora el juego lo sabe decir
—la hueste dice «sin pertrechos: la cadena no da para tanto» y no solo un
porcentaje—. La hueste que ese siglo sostiene de verdad, unas once unidades, va
entera.

**Y hay depósitos.** En paz se llenan solos hasta dos años de producción; en
guerra se vacían, y cuando se acaban se pelea con lo que sale de la fábrica ese
día y nada más. Eso es lo que separa una guerra corta de una larga, y es la
razón por la que todo el mundo planeó guerras cortas.

## Por qué se pelea

Hasta ahora una guerra se declaraba y después se veía: no se declaraba **por**
nada. Se empezaba, se tomaba lo que el frente diera, y terminaba cuando uno de
los dos no podía más. Así no funcionó casi ninguna guerra de la historia, y
sobre todo así no se entiende ninguna: lo que decide cuándo y cómo termina una
guerra no es cuánta gente queda, es para qué se empezó.

Ahora hay que decirlo al declararla: **un escarmiento, que paguen tributo,
quedarse una comarca, arrancar concesiones, o someterlo entero.** En el mapa,
el clic derecho sobre tierra ajena declara la guerra por esa comarca —el motivo
más viejo que hay—; los demás se eligen en la ficha del ejército, donde hay
sitio para explicarlos.

Ese objetivo hace tres cosas a la vez:

- **Dice cuándo se ganó.** Un escarmiento se consigue con vencerlos en el
  campo; una guerra por Landes termina cuando Landes es tuya, y arrasar el país
  sin tomarla no la gana. Eso es lo que permite que exista una guerra corta.
- **Limita lo que se puede exigir en la mesa.** Se puede pedir más de lo que se
  anunció —nadie lo impide— pero sale marcado como «fuera de lo pactado» antes
  de firmarlo, y cuesta prestigio, diplomacia y humor del pueblo. Pedir menos
  nunca es una traición, y la paz blanca siempre está.
- **Le pone precio al escándalo, y ese precio cambia con el siglo.** Borrar a
  un vecino del mapa en 1200 es una hazaña; en 1900 es un problema con todas
  las cortes de Europa. El mismo acto, tres veces más caro.

**Nadie pelea hasta el último hombre.** Cada bando tiene ganas de seguir, y se
acaban antes que los hombres: se pelea hasta que sale más caro seguir que
ceder. Cuando al vecino se le acaban, manda emisarios. Si te está ocupando
comarcas a vos, aguanta más, porque tiene con qué negociar.

Y **ganar y no parar es la forma más común de perder**. Conseguido lo que se
fue a buscar, al reino se le van las ganas de golpe —«ya ganamos, ¿qué hacemos
acá?»— y cada turno de más cuesta estabilidad y humor. El parte de guerra dice
las dos cosas: para qué se pelea y cuántas ganas le quedan a cada lado.

## Cómo se pelea

El ejército tenía piezas —come, se adiestra, se organiza, se entera, se arma— y
ninguna manera de decir para qué las usa. Todos los reinos peleaban igual y
solo se distinguían por cuánto tenían de cada cosa.

Una **doctrina** no es un bono: es una forma de pelear, y una forma de pelear
es siempre un intercambio. Hay seis, y cada una toca las piezas que ya existen
—el campo, el sitio, la marcha, el pan, los pertrechos, el bulto, el mando, la
vista, la sangre y el empuje del frente— y ninguna nueva:

- **La guerra de plazas.** Se toman los castillos y se arrasa el campo; para
  ella un muro vale la mitad que para cualquier otra. Y por eso a campo abierto
  pelea peor que nadie.
- **La batalla decisiva.** Se busca al otro ejército y se lo deshace: la mejor
  en campo abierto, la peor delante de una plaza, y el día que sale mal deja el
  doble de gente en el suelo.
- **La guerra de posiciones.** No se arriesga nada: come un cuarto menos, pierde
  la mitad de gente y avanza despacísimo.
- **La nación en armas.** Marcha el doble, come un tercio menos porque vive del
  país que cruza, y lo paga en sangre: hay más hombres detrás porque hacen falta.
- **La guerra de material.** Gasta el doble de pertrechos por cabeza y es
  literalmente su método; a cambio rompe muros y líneas, y avanza más despacio
  que nadie.
- **La guerra de movimiento.** Concentra dos cuerpos más de los que su época
  permite, ve más lejos y marcha un cincuenta por ciento más rápido — y todo
  depende de que el abasto siga el paso, que casi nunca lo sigue.

Ninguna es mejor: cada una es mejor **contra** algo. Se ganan con el siglo y no
por decreto —decretar guerra de movimiento en 1200 no hace nada—, la ficha
enseña los pesos de cada una antes de elegir, y **cambiar cuesta**: la tropa
tiene que volver a aprender su oficio y la instrucción cae un treinta por
ciento, así que no se cambia todos los años.

## Las bajas que no son muertos

Hasta acá una hueste derrotada perdía gente y esa gente desaparecía del mundo.
Es la simplificación más cara que quedaba, porque en casi todas las batallas de
la historia los muertos fueron una minoría de las bajas: la mayoría **se
rindió**, y lo que pasó después con esos hombres es media historia de la
guerra.

Ahora una parte de las bajas del vencido son **prisioneros**. Cuántos lo decide
sobre todo lo desparejo que quedó el final —en una derrota aplastante se
entrega la mitad larga de los que caen, y en una batalla pareja casi nadie,
porque mientras la línea aguanta no hay a quién rendirse—. Y la veteranía
cuenta acá al revés que en todo lo demás: **el que sabe se escapa**. Los que se
entregan en masa son las levas nuevas.

Donde salen a montones es en las **bolsas**. Una hueste cortada, sin pan y sin
salida, no se muere de hambre entera: se entrega casi completa, porque no hay
retirada que ordenar. Ulm, Sedán, Tannenberg, Stalingrado.

**Y comen todos los días.** Un preso come un tercio largo de lo que come un
soldado en armas, y de la misma despensa. Capturar un ejército es heredar el
problema de alimentarlo: si el pan no alcanza, los presos se mueren, y del otro
lado eso no se distingue de haberlos matado. La mayoría de los prisioneros que
murieron en la historia murieron de hambre y de tifus, no de una orden.

Por eso hay que decidir qué hacer con ellos, y hay cinco cosas —las cinco que
se hicieron siempre—:

- **Pedir rescate.** Lo que más oro deja, y era para lo que se los tomaba.
- **Soltarlos bajo palabra.** No deja un escudo y deja todo lo demás:
  relaciones, prestigio y la fama de tratar bien a los que se rinden.
- **Ponerlos a trabajar.** A las minas y a los caminos. Algo de oro y una
  mancha.
- **Canjearlos por los nuestros.** Hombre por hombre, y **es el único que
  devuelve gente a las filas**. No existe antes de 1650: hace falta que dos
  estados se reconozcan y lleven listas.
- **Pasarlos a cuchillo.** No cuesta oro y cobra en las otras cuatro monedas a
  la vez, incluida la de adentro: es la única de las cinco que remueve la
  estabilidad del propio reino.

Todo eso deja una **fama**, de intachable a infame, y la fama no es una nota de
conducta: **es información que circula**. Al que degüella a los que se rinden
no se le rinde nadie —los que se habrían entregado se mueren peleando— y además
el vecino aguanta mucho más antes de firmar, porque rendirse deja de ser una
salida. Una guerra contra un rey así dura el doble, y eso le costó caro a más
de un conquistador que se había ganado la fama a propósito.

Una fama se olvida, pero en una generación: no porque nadie perdone, sino
porque se muere la gente que se acuerda. Y al firmar la paz se abren las
prisiones de los dos lados —fue la cláusula que tuvo casi todo tratado de la
historia y la que se cumplía primero, porque a esa altura los presos son una
carga para los dos—.

## El teatro que no toma tierra

La tentación con el aire es tratarlo como una rama más y dejar que gane
batallas. No es lo que pasó. Ninguna guerra la ganó una fuerza aérea sola, y
todos los que lo prometieron se equivocaron. **El aire no toma un palmo de
tierra**: la toma el que camina encima. Lo que hace lo hace a través de cosas
que el juego ya tenía montadas — lo que se ve, lo que el ejército come, lo
rápido que se mueve y las ganas que le quedan al otro.

La **aviación** es una sexta rama, la más cara de mantener con diferencia, y la
única que **no marcha con nadie**: no se reparte en huestes, se queda en el
reino y opera sobre el teatro entero. Un reino que solo tenga aviones no pone
nada en el mapa.

**El cuello de botella son las tripulaciones, no los aparatos.** Alemania y
Japón terminaron la guerra con más células que gente que supiera volarlas. Una
tripulación tarda dos años en hacerse y se pierde en una tarde, y el techo lo
pone lo que el reino sabe *más* si tiene la costumbre de adiestrar a su
infantería: las dos cosas salen del mismo estado mayor. Los mismos veinte
aviones valen tres veces más con tripulaciones hechas que con reclutas.

**Primero hay que ganar el cielo, y se le gana a su aviación, no al suelo.**
Hasta que eso está resuelto, lo demás no vuela: mandar a cortar puentes sin
tener el cielo no corta absolutamente nada. Y ganarlo no es alquilar una
ventaja que se paga todos los turnos — es **destruirle la fuerza aérea al
otro**, y lo roto queda roto. Cinco años de cazar y nada más no dejan nada de
su aviación, y recién entonces se puede pasar a otra cosa sin perder el cielo.
Es lo que pasó en 1944: los cazas de escolta deshicieron a la caza alemana
entre enero y abril, y recién después la Novena pudo dedicarse a los puentes.

Hay cuatro cosas que puede hacer, y son cuatro y no todas:

- **Ganar el cielo.** No enseña ningún resultado. Hace posibles a las otras tres.
- **Cortarle el abasto.** Lo que de verdad le hizo el aire a los ejércitos: no
  destruirlos, dejarlos sin nada. Pega en la pérdida por palmo, así que el que
  está pegado a su base casi no la siente y el que está a trescientos
  kilómetros dentro de una bolsa se queda sin comer.
- **Apoyar al ejército.** Necesita **radio** — alguien tiene que decirle al
  piloto dónde tirar, y por eso esto es de 1940 y no de 1917. Y rinde poco:
  los cazabombarderos reclamaron un orden de magnitud más blindados de los que
  destruyeron.
- **Bombardear su país.** Necesita un bombardero de gran radio, y hace lo
  contrario de lo que prometieron: **les baja poco la producción y les sube las
  ganas de pelear**. Eso no es una opinión, es lo que midió el Strategic
  Bombing Survey y lo que ya había enseñado el Blitz. Un país bombardeado no se
  rinde, se enoja. Además es la misión que más aviones cuesta.

Lo que sí hace siempre, gane quien gane las discusiones: **ver mucho más
lejos** y **no dejar moverse de día**. Las divisiones que fueron a Normandía
tardaron semanas en un viaje de días, y casi ninguna vio una bomba.

Contra todo eso está la **antiaérea**, que no es aviación: son cañones. Sale de
la artillería que el reino ya tiene, y vale mucho más con radar que sin él.
Treinta cañones sin un solo avión levantan un cielo perdido del todo a un
cielo caro de cruzar, y le encarecen el trabajo al que viene a cortar
puentes. Lo que no hacen es ganar el cielo: un cañón no persigue a un avión
hasta su campo.

Y una fuerza aérea **se gasta sola**. Hasta en paz se pierden aparatos —
accidentes, fatiga, tiempo—, y el que va perdiendo el cielo se desangra al
triple y pierde tripulaciones más rápido de lo que la escuela las hace. Ahí
está la espiral: se muere el que sabe, entra el que no sabe, y el que no sabe
se muere antes.

## Lo que se gana sin dar una batalla

La historia naval que se cuenta es la de Salamina, Lepanto y Trafalgar. La que
decidió las guerras es la de los años en que no pasó nada: la escuadra del otro
en el puerto sin animarse a salir, el bloqueo apretando un año tras otro, y los
convoyes llegando.

**Lo primero: el agua es agua.** Hasta ahora un ejército cruzaba el Canal
caminando. Ahora se cruza embarcado o no se cruza. Hacen falta barcos —cada uno
lleva cuatro unidades de tropa— y hace falta que el mar no sea del otro: **no se
desembarca donde manda el enemigo**, y Overlord esperó a tenerlo. Un ejército
mandado al otro lado del agua sin con qué cruzarla llega a la orilla, se queda
ahí y lo dice. Por mar se va mucho más rápido que por tierra, y esa es la mitad
de lo que hizo grandes a los imperios marítimos.

**Sin puerto no hay armada** por mucho oro que se ponga, y con dos puertos se
sostiene menos escuadra que con veinte: no es el número de barcos, es el
astillero. Un reino sin costa está fuera de todo esto — incluido, y esto se
olvida siempre, **no poder ser bloqueado**.

**La flota en ser.** Una escuadra que no sale del puerto sigue obligando al otro
a tener la suya enfrente. Por eso cuatro veces más barcos no dan cuatro veces
más mar: la curva es cóncava a propósito, el dominio absoluto casi no existió
nunca, y de ahí sale que Tirpitz consiguiera algo real sin ganar una batalla.

Cuatro cosas puede hacer una armada:

- **Sostener la escuadra.** Estar, que en la mar es casi todo.
- **Bloquear sus puertos.** Lo más decisivo que hizo una armada, y no se parece
  a una batalla: se le cierra el comercio y se espera un año, dos, los que
  hagan falta. Casi no cuesta dominio del mar, y no es generosidad — la
  escuadra que bloquea *es* la escuadra de línea, y tenerla frente a Brest era
  justamente lo que impedía que el otro saliera.
- **Guerra al comercio.** Lo único que funciona **sin** dominar el mar, y por
  eso fue siempre la estrategia del que no podía ganarlo. Se paga cediendo la
  superficie, tiene techo bajo, y no ganó una guerra nunca: Francia lo intentó
  dos siglos contra Inglaterra y Alemania dos veces contra todos.
- **Escoltar lo propio.** No le quita nada al otro y es lo que salvó a más de un
  país. Necesita quien organice la travesía; sin eso no hay convoy, hay barcos
  que salen juntos.

El bloqueo **se siente en la aduana antes que en el frente**: el comercio
exterior se desploma, el cabotaje de las comarcas con puerto se corta, y al otro
lado le cuesta cada vez más poner tropa nueva en el campo. Y aprieta despacio —
es una cuenta que se suma, no un golpe—, mientras su escuadra se va gastando y
lo hundido no vuelve a salir.

**Y acá está el contraste que hace que valga la pena tener los dos sistemas:**
bombardearle las ciudades al otro le **endurece** la voluntad y cerrarle los
puertos se la **rompe**. Las dos cosas se midieron y dieron distinto, y no es
una paradoja: una bomba es un ataque que se puede odiar, y el hambre del tercer
invierno es una cuenta que hace todo el mundo en su casa. El bloqueo aliado
contribuyó al derrumbe alemán de 1918 más que ninguna ofensiva de ese año.

## Decir qué y no cómo

El que juega a esto es un jefe de estado, y hasta ahora le hacía a cada hueste
el trabajo de un capitán: caminá hasta acá, sentate delante de esa plaza,
asaltala. Ningún rey hizo eso nunca. Lo que se hace desde arriba es dar una
intención y dejar que el que está ahí resuelva el cómo, porque el que está ahí
ve el terreno y uno no.

Se le encarga a un general una de cinco cosas — **limpiar la comarca**, **tomar
la plaza**, **sostener la línea**, **hostigar sin comprometerse** (necesita
oficiales que sepan retirarse a tiempo) o **desembarcar allá** (necesita costa)
— y a partir de ahí él da las órdenes. Ninguna de las cinco dice por dónde ir
ni qué hacer al llegar: eso es exactamente lo que se delega.

**Una directiva llega hasta donde llega el correo de su siglo.** Un rey de 1200
manda a unos ciento y pico de kilómetros; con un cuerpo de oficiales, algo más;
con una plana mayor, seiscientos; y con el telégrafo, un continente. Más allá
de ese alcance el hombre no desobedece — cumple lo que entendió, que es otra
cosa. Al lado de la corte se obedece un noventa por ciento; a mil kilómetros en
1500, menos de la mitad; a la misma distancia con un cable, otra vez casi todo.
No hizo mejores generales, hizo generales más vigilados.

**Y ahí los rasgos de los generales dejan de ser un adorno.** Cada uno marcha a
su paso, sangra lo suyo, rinde lo suyo delante de un muro y se sale de lo
pedido lo suyo:

- Un **audaz** marcha casi el doble que un cauteloso, pierde el doble de gente
  ganando lo mismo, y a la primera ocasión hace bastante más de lo que se le
  encargó.
- Un **metódico** no pierde hombres de más y no se sale nunca de la raya.
- El **ingenioso en el sitio** toma plazas que los otros rodean.
- Un **cauteloso** llega tarde a todo, no gana nada y no lo destruyen jamás.

Encargale la misma comarca a dos de ellos y salen dos campañas distintas. Y a
un cauteloso al que le pedís sostener una línea, la sostiene; al audaz se le va
a buscar al que viene, que no se le pidió y es lo que iba a hacer igual.

**La contrapartida es que delegar es dejar de ver.** Lo que vuelve no es el
mapa en vivo: es un parte, y tiene la fecha de tu siglo. En 1200 lo que la
corte lee de su propia campaña tiene doce días; con telégrafo se sabe lo que
pasa mientras pasa. Y el parte dice con qué cuenta el hombre, no dónde está
cada hueste — porque eso es un parte y no un mapa.

La operación se cae sola cuando se cumple, y se cae también si el general se
muere: sin él, las huestes se quedan donde están esperando órdenes.

## Convertir el país

Una guerra larga no se paga con el tesoro. Se paga convirtiendo el país, y
todos los estados que pelearon una lo descubrieron tarde y del mismo modo: las
fábricas dejan de hacer arados y hacen espoletas, la gente que hacía una cosa
hace otra, y el estado se mete a decidir qué se produce, cosa que en tiempos
normales no hace nadie.

Hay cinco escalones y cada uno pide su siglo:

- **Economía de paz.** El país hace lo que hacía. En una guerra larga eso rinde
  exactamente nada.
- **Impuesto de guerra.** Lo único que se podía hacer en 1200, y por eso se
  hizo siempre. Es el único escalón que deja **más** plata de la que quita.
- **Arsenales del rey.** Llegan con el ejército permanente y no antes: sin
  tropa propia todo el año no hay para quién fabricar todo el año.
- **Requisa de la industria.** No se puede requisar una industria que no
  existe: esto es de la era de la fábrica.
- **Economía dirigida.** El estado decide qué se produce, quién lo produce y
  quién lo come. Pide una industria que se pueda planificar.

**Y convertir lleva años.** Es lo único importante de todo el bloque. Hay dos
números: lo que se mandó hacer y lo que de verdad está pasando, y el segundo se
arrastra detrás del primero. El día que se firma la orden no ha cambiado nada.
Llegar desde una economía de paz hasta la dirigida lleva unos nueve años, y una
economía a medio convertir rinde a medias. Por eso **gana las guerras largas y
arruina las cortas**: al año de haberla mandado, la cadena de guerra rinde un
tercio más; a los seis, el triple.

**Cañones o manteca, y no las dos cosas.** Lo que sube la producción de guerra
baja la civil en la misma medida — no hay magia, hay gente y hierro que estaban
haciendo otra cosa. Con la conversión hecha la cadena rinde cuatro veces y el
ingreso del reino cae a poco más de la mitad. Lo que **no** cambia es el cuello
de botella: movilizar no abre minas nuevas, pone a trabajar de noche lo que ya
había. Lo angosto no se ensancha gritando.

**La gente lo aguanta en guerra y no lo aguanta en paz.** La misma requisa que
en tiempo de paz sería un escándalo, en guerra es lo que hay que hacer. Los que
más se quejan no son los que hacen la cola del pan sino los que tenían las
fábricas: a unos les tocan la ración y a otros la propiedad. El único contento
es el ejército, que por primera vez tiene todo lo que pidió.

**Y desmovilizar es su propia crisis.** El año que sigue a una guerra es peor
que el último año de la guerra: hay talleres sin encargos y hombres que hacían
espoletas y no saben hacer otra cosa. Desarmar va al doble de rápido que armar
—cerrar una fábrica es más fácil que abrirla— pero aun así lleva años, con la
producción civil por debajo de lo normal todo ese tiempo. 1919 y 1921 fueron
eso, y nadie los esperaba.

Cómo se paga sigue donde estaba: el tesoro, la deuda con sus banqueros y su
tasa, y envilecer la moneda con su memoria. La economía de guerra no es una
manera de pagar; es una manera de producir.

## El arma que sirve para no usarse

Todo lo demás en este juego es una cantidad: más infantería pelea más, más
barcos cierran más puertos, más aviones cortan más puentes. La bomba no es una
cantidad. Modelarla como un cañón muy grande sería el error más caro que se
puede cometer acá, porque lo que la bomba cambia es **para qué sirve una
guerra**.

**Tenerla es una obra industrial, no un descubrimiento.** La física se sabía en
varios países a la vez desde 1938. Lo que separó a los que la tuvieron de los
que no fue separar isótopos a escala industrial — un problema de electricidad y
de años. El cuello de botella no fue Los Álamos: fueron Oak Ridge y Hanford. En
el juego hay que **ordenar la obra**, y avanza con la industria y con el país
movilizado detrás: a pleno tarda unos tres años, y sin industria ni
movilización tarda más de una guerra entera.

**La primera no sirve para nada.** Hiroshima y Nagasaki fueron dos bombas y no
había una tercera. Una sola cabeza disuade casi cero; veinte, tres cuartos.

**Y lo que disuade no es tenerla: es sobrevivir al primer golpe.** La cuenta
que hace el otro no es cuántas tenés sino cuántas te quedarían después de que
él pegue primero. Con las mismas ocho cabezas sobrevive el 9% en un campo de
aviación y el 46% en el mar — por eso el submarino cambió más las cosas que
ninguna cabeza.

**El momento peligroso no es el que suena razonable.** Hay cuatro casillas:

- Nadie la tiene: no hay nada que temer.
- La tiene uno solo: peligro medio, y es la tentación de usarla mientras dure
  la ventaja — que no dura, porque el secreto ya está contado.
- **La tienen los dos y alguno no aguantaría el primer golpe: la peor casilla
  del tablero.** Hay que pegar primero o perderlo todo. Eso tiene nombre —
  inestabilidad de crisis— y es lo que casi se juega en 1962.
- La tienen los dos y los dos aguantarían: **la más segura de todas.** Ninguno
  lo va a dar, y ahí la guerra deja de ser un instrumento.

**La disuasión no gana guerras: hace que no las haya.** A un vecino que sabe
que podés destruirlo y que no puede impedirlo se le acaban las ganas de pelear
— no porque le falten hombres, porque la guerra dejó de servirle. Pero si él
también la tiene y también sobreviviría, se anulan y la guerra vuelve a
decidirse como siempre. La bomba no toma un palmo de tierra.

**Y el secreto nunca fue cómo, fue que se podía.** El día que se prueba la
primera, el resto del mundo aprende lo único que hacía falta saber. A partir de
ahí es cuestión de años y de empeño, y todos los tienen.

**Usarla cuesta el mundo.** Le rompe al otro la voluntad y el poder de golpe —
es lo único que la bomba hace mejor que todo lo demás junto— y a cambio hunde
las relaciones con **todas** las cortes, el prestigio, la estabilidad de casa,
y manda a cero la fama de cómo tratás a los que se rinden: al que hizo esto no
se le vuelve a creer nada sobre cómo trata a nadie. Y se gasta la que se tiró.

## Lo que no se fabrica con empeño

El pan sale de cualquier campo. Los pertrechos salen de una cadena que se puede
ensanchar con años y con dinero. El combustible no sale de ninguna de las dos
cosas: **o está debajo de tu tierra o no está**, y esa asimetría es lo único
que hay que entender de este bloque. Es el primer recurso de la historia
militar que no se resuelve con empeño.

Y reorganizó la estrategia del mundo, no la logística de una campaña: Alemania
fue al Cáucaso por petróleo y se quedó sin él antes de llegar; Japón atacó
Pearl Harbor porque le habían cerrado el grifo; la flota italiana pasó la
guerra en el puerto con los barcos intactos; Rommel paró en El Alamein porque
los petroleros no llegaron.

**No existe hasta que uno se motoriza.** Un ejército de 1200 no pide una gota,
y en 1890 hay motores y casi nada anda a motor. Motorizarse tampoco es solo
saber hacerlo: hay que poder pagarlo, así que lo decide también la economía de
guerra — y nunca llega al total, porque ni el ejército más rico de 1945 lo
estuvo y la Wehrmacht de 1941 iba en su mayor parte a caballo.

**Sale de tres sitios y solo uno es seguro.** De tu propia tierra, si tuviste
suerte con la geología; comprado afuera, que es de lo que vivieron casi todos y
es exactamente lo que corta una escuadra enemiga; o hecho de carbón con un
catalizador sólido, que es química de 1909, el proceso más caro que existe, y
se usó igual porque la alternativa era parar. La ficha dice de cuál de los tres
depende el país, que es lo frágil que es la cosa.

**El intercambio es el más limpio de todo el sistema militar.** Una columna
motorizada con el tanque lleno hace más del doble que una de caballos — y con
el tanque vacío hace **menos** que ella, porque al caballo lo alimenta el pasto
del camino y al camión no lo alimenta nada. Un camión sin gasóleo no es un
camión lento: es un peso muerto que hay que empujar. Eso es Alemania en 1945.

**Y cuando falta no se reparte a prorrata.** Primero vuela el que vuela y
navega el que navega, porque un avión a media ración no vuela a media altura:
no vuela. La Luftwaffe de 1945 tenía más aparatos que nunca. Lo que sobra es lo
que mueve a la tropa.

Una escuadra sin gasóleo, en cambio, **sigue siendo una flota en ser**: amarrada
obliga igual al otro a tener la suya enfrente, y la italiana ató a media
Mediterranean Fleet sin salir del puerto. Lo que el tanque vacío impide no es
existir: es salir.

Y es la única de las tres cosas que un ejército consume que **no perdona la
organización**: saber de logística ahorra pan y pertrechos como ahorró siempre,
y no ahorra ni una gota de combustible. Un motor quema lo que quema.

## Lo que deja una guerra larga

Hasta acá las bajas eran un número que bajaba la población y se olvidaba. Lo
que una guerra larga le hace a un país no termina el día que se firma la paz:
**empieza ahí**, y dura décadas.

**Los que volvieron rotos.** Por cada muerto volvieron dos o tres hombres que
no podían trabajar, y vivieron cuarenta años más. Eso no es una baja: es una
carga permanente. Sus **pensiones** son una partida nueva del presupuesto que
sobrevive al ejército que la generó — un reino puede licenciar hasta el último
soldado y seguir pagándola treinta años. Las pensiones de la guerra civil
norteamericana fueron la mayor partida del presupuesto federal en los años
noventa, tres décadas después de la paz.

**El hueco, y el eco veinte años después.** Una guerra mata varones jóvenes y
eso no se arregla con tiempo. Faltan matrimonios, faltan nacimientos, y **veinte
años más tarde vuelve a faltar gente en edad de servir** — no por la guerra de
entonces sino por el que no nació entonces. Es el bajón más grande de los dos y
llega cuando ya nadie se acuerda de por qué. El déficit de nacimientos de
Francia entre 1915 y 1919 fue mayor que sus muertos en combate, y volvió a
doler en 1939.

**El rencor no lo hace la guerra: lo hace la vuelta.** Mientras se pelea está
contenido — hay a quién echarle la culpa —, y el día que se firma se suelta de
golpe: hay que explicarle a un montón de hombres qué hacen ahora. De ahí
salieron todos los paramilitares de entreguerras. Y no se apaga con el tiempo
sino **con el pan**: un país que sigue exprimiendo a su gente después de la paz
no desactiva a nadie.

**Y la otra cara, sin la cual esto sería una lista de castigos.** Todo estado
que le pidió todo a su pueblo tuvo que darle algo después: el voto, la pensión,
la escuela. La guerra total construyó el estado de bienestar, y no por bondad
de nadie — por la cuenta que hicieron los que volvieron armados. Es lo único de
todo esto que **no se devuelve nunca**.

`MILICIA.md` tiene el mapa completo de lo que falta del sistema militar y en
qué orden conviene hacerlo.

## El mapa suelta el detalle mientras se mueve

Acercarse con el trackpad hacía trabajar al navegador **trece segundos para un
gesto de uno**. Encontrar el motivo costó más que arreglarlo, y las cinco
primeras sondas dieron todas la respuesta equivocada.

**Lo que no era.** No era la geometría: simplificar los trazos a medio píxel
salva el 2%, porque los puntos ya están al límite de lo que el píxel distingue.
No era el margen del lienzo: bajarlo de 0,3 a 0,1 arruina el arrastre y apenas
toca el zoom, así que el valor que ya estaba escrito era el correcto. Y no eran
los asentados: durante el gesto malo había nueve, y nueve mapas no son trece
segundos.

**Por qué no aparecía.** El perfilador de JavaScript decía «(program), 87%», que
es su manera de decir «esto no es tuyo». Contar cuadros tampoco servía: en un
navegador sin pantalla salen lecturas de ciento cincuenta por segundo. El
trabajo estaba donde ninguna de las dos mira: **Chrome rasteriza en hilos
aparte**. Hay que pedirle su propio registro interno, y ahí aparece de una vez:

    12882 ms   2034 veces   RasterizerTaskImpl::RunOnWorkerThread
      421 ms     47 veces   Layout

Dos mil rasterizados para cuarenta tirones: la capa entera, en mosaicos, rehecha
en cada cuadro.

**Lo que era.** El supuesto del código era que estirar la capa dibujada sale
gratis. Sale gratis si el estirón es un **corrimiento** —eso lo hace la tarjeta
gráfica con lo ya pintado, y por eso arrastrar nunca fue el problema—, pero no
si es una **escala**: ahí el navegador vuelve a rasterizar la capa a la
resolución nueva. Y la capa mide 2,56 veces lo que se ve, porque ese margen de
más es justo lo que hace gratis el arrastre.

**Lo que se hizo.** Mientras la escala está cambiando, el mapa se dibuja sin las
capas de detalle: los contornos de provincia, las fronteras, el relieve y los
nombres de las sierras. Son el 55% de los puntos y son exactamente las que nadie
mira mientras el mapa se está moviendo. Vuelven solas al soltar, que es cuando
se las mira.

Con dos cuidados que salieron de medir y no de suponer:

- **Un tirón suelto no pierde nada.** Encender y apagar el modo cuesta dos
  rasterizados, más caros que el detalle que ahorran si el gesto es uno solo. Se
  enciende únicamente cuando llega un tirón mientras el anterior todavía está
  viajando, que es la definición honesta de «el mapa no llega».
- **Las ciudades se quedan.** Estaban en la lista de candidatas y la medición
  dijo que quitarlas empeoraba. Se devolvieron al mapa.

Rasterizado de un acercamiento de trackpad: **16,5 s → 9,5 s**. El arrastre no
cambió, que era lo correcto: nunca había estado mal.

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
