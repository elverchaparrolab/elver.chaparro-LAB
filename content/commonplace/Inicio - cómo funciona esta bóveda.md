---
publicar: true
tipo: índice
---

# Cómo funciona esta bóveda

Un Zettelkasten para investigación doctoral, pensado para durar años y mantenerse con poco esfuerzo. Se basa en el fichero de Niklas Luhmann, en *How to Take Smart Notes* de Sönke Ahrens, en *A System for Writing* de Bob Doto y en las recomendaciones de zettelkasten.de.

**Para entrar, abre siempre 000 - Índice general.**

## Cinco principios

1. **Una idea por nota, con tus palabras.** Lo que copias o resumes de otros va en la nota de la fuente; lo que piensas tú, en un Zettel.
2. **Los temas se ordenan con enlaces, no con carpetas.** Las carpetas solo dicen qué tipo de nota es. Nunca crees carpetas por tema ni por capítulo de la tesis: un Zettel tiene que servirte también después de la tesis.
3. **Cada nota tiene un número que nunca cambia** (`AAAAMMDDHHmm`, la fecha y hora en que nació). Así nunca se repiten nombres y los enlaces no se rompen.
4. **Texto plano y pocas herramientas.** Todo es Markdown y la bóveda solo depende de 5 complementos. Si Obsidian desaparece, tus notas se siguen leyendo en cualquier editor.
5. **Escribes desde los Zettel, no desde cero.** Un capítulo o un artículo se arma ordenando Zettel que ya escribiste.

## La estructura en tres niveles

1. **000 - Índice general**: el registro. Lista los temas.
2. **Índices de tema** (`30 Índices`): uno por tema, con sus Zettel en orden de lectura, sus fuentes y los subtemas pendientes.
3. **Zettel** (`20 Zettel`): las ideas. Cada uno apunta a otros Zettel y, con su propiedad `índice`, a su tema.

Las fuentes alimentan a los Zettel, y los Zettel alimentan a los proyectos.

## Las carpetas

| Carpeta | Qué va ahí | Cómo se llama cada nota | Plantilla |
|---|---|---|---|
| `00 Inbox` | Ideas sueltas por procesar. Son temporales. | `AAAAMMDDHHmm` | Plantilla - Nota rápida |
| `10 Fuentes` | Una nota por libro, artículo, video o película, con lo que tú sacas de ella. | `@citekey` (desde Zotero) o el título | Plantilla - Fuente Zotero o Plantilla - Nota fuente |
| `20 Zettel` | Tus ideas permanentes. Es el corazón de la bóveda. | `AAAAMMDDHHmm - Afirmación` | Plantilla - Nota permanente |
| `30 Índices` | El Índice general y un índice por tema. | `Índice - Tema` | Plantilla - Índice |
| `40 Proyectos` | Una carpeta por producto: capítulo, artículo, ponencia o curso. | `Proyecto - Nombre` | Plantilla - Proyecto |
| `50 Plantillas` | Las 6 plantillas. No las edites sin necesidad. | — | — |
| `00 Inbox/Por revisar` | Notas viejas sin procesar. No hace falta revisarlas: rescata una cuando te sirva. | — | — |
| `60 Adjuntos` | Imágenes, PDF y audios. Obsidian guarda aquí los nuevos. | — | — |

No crees más carpetas. Si dudas dónde va algo, va a `00 Inbox`.

## Propiedades

Cada nota lleva pocas propiedades y siempre las mismas:

- **Zettel:** `id`, `tipo: zettel`, `creado`, `índice` (el tema) y `fuentes` (de dónde sale la idea).
- **Fuente:** `tipo: fuente`, `citekey`, `autor`, `año`, `título`, `índice` y `estado` (por leer, leyendo o leído).
- **Índice:** `tipo: índice`. **Proyecto:** `tipo: proyecto`, `estado` y `entrega`.

## El trabajo de cada día

### 1. Capturar
Cuando se te ocurra algo, usa el comando **"Crear nueva nota única"** (Cmd+P). Crea una nota en `00 Inbox` con su número y la plantilla. Escribe sin pensar dónde va.

### 2. Leer
1. Lee y subraya el PDF en **Zotero**, y escribe tus comentarios en las anotaciones.
2. En Obsidian, usa el comando **"Zotero Integration: Nota de fuente"** y elige el documento. Se crea `10 Fuentes/@citekey` con la referencia en APA, tus subrayados con enlace a la página exacta y tus comentarios.
3. Debajo, en "Resumen con mis palabras" e "Ideas para Zettel", escribe lo que tú sacas. Si vuelves a importar, Zotero actualiza las anotaciones sin borrar lo que escribiste.
4. Ponle su `índice`. Si es un video, una web o una película, usa Plantilla - Nota fuente.

### 3. Escribir Zettel
Toma una idea del Inbox o de una fuente y escríbela como Zettel:
- **Título:** la idea completa en una frase ("La ideología opera como modelo mental compartido"), no un tema ("Ideología").
- **Cuerpo:** de 3 a 8 frases con tus palabras, que se entiendan sin abrir otra nota.
- **Fuente:** el enlace a la fuente con la página: `@vandijk2011, p. 45`.
- Muévelo a `20 Zettel` (si nació en el Inbox) y aplica la plantilla de nota permanente.

### 4. Conectar
- Enlaza cada Zettel nuevo al menos a otro Zettel y explica en una línea por qué se relacionan.
- Pon su tema en `índice` y agrégalo a la lista de ese índice, en el lugar que le toca en el argumento.
- Si cinco o más Zettel tratan algo que no tiene tema, crea un índice nuevo con Plantilla - Índice y enlázalo en el Índice general.

### 5. Escribir para la tesis
1. Crea una carpeta en `40 Proyectos` y dentro una nota con Plantilla - Proyecto.
2. Arma el esquema con Zettel que ya existen. Si falta una idea, escribe primero el Zettel.
3. Redacta el borrador uniendo esos Zettel. Para citar, escribe `[@citekey]`: el complemento Pandoc Reference List muestra la bibliografía, y al exportar con Pandoc y el `.bib` de Zotero obtienes las referencias en APA.

## Revisión semanal (unos 30 minutos)

El Índice general tiene una sección "Para la revisión semanal" que se llena sola.
- [ ] Vaciar `00 Inbox`: cada nota pasa a ser un Zettel, se agrega a una fuente o se borra.
- [ ] Poner `índice` a los Zettel y fuentes que aparecen como "sin tema".
- [ ] Revisar un índice de tema: ¿el orden de los Zettel todavía cuenta un argumento?
- [ ] Marcar como "leído" las fuentes que terminaste.

Una vez al mes, rescata una o dos notas de `00 Inbox/Por revisar` que te sirvan y reescríbelas como Zettel.

## Nombres y enlaces

- Para enlazar, escribe `[[` y empieza a teclear el título; no hace falta escribir el número.
- Al renombrar o mover una nota desde Obsidian, los enlaces se actualizan solos. No renombres desde Finder.
- Las numeraciones antiguas tipo Luhmann (`1a1`, `3c`) siguen en la propiedad `folgezettel`; no hace falta usarlas en notas nuevas.

## Complementos que usa la bóveda

Solo estos cinco, más los básicos de Obsidian. Los demás están desactivados, no borrados.

| Complemento | Para qué |
|---|---|
| Zotero Integration | Importar fuentes y citas desde Zotero |
| Pandoc Reference List | Ver la bibliografía de lo que citas |
| Dataview | Las listas automáticas del Índice general |
| Omnisearch | Buscar dentro de notas y PDF |
| Excalidraw | Abrir tus dibujos y esquemas |

## Qué no hacer

- No crees carpetas por tema, autor o capítulo.
- No copies texto ajeno en un Zettel: va en la fuente.
- No instales complementos para organizar. Si el sistema necesita más orden, se resuelve con un índice.

Los registros de la reorganización (dónde quedó cada archivo y cómo se llamaba antes) están en los archivos `_registro-*.csv` de `00 Inbox/Por revisar`.
