#!/usr/bin/env python3
"""Sincroniza el Commonplace Book de Obsidian con el jardín digital (Quartz).

Publica SOLO las notas que tienen `publicar: true` en sus propiedades.
Cada ejecución regenera `content/commonplace/` desde cero, así que una nota
que deja de estar marcada desaparece del jardín.

Bloqueos que se aplican aunque la nota esté marcada:
  - carpetas 00 Inbox, 50 Plantillas y 60 Adjuntos (notas);
  - notas «texto completo» (obras de otros autores);
  - notas del tema Salud y bienestar o con términos médicos en el título;
  - archivos PDF, audio y video (solo se copian imágenes).

Transformaciones:
  - bloques de Dataview y comentarios de Obsidian se quitan;
  - enlaces a notas no publicadas quedan como texto plano;
  - correos electrónicos se reemplazan por «[correo omitido]».

Uso:
  python3 scripts/sincronizar_commonplace.py            # sincroniza y muestra el informe
  python3 scripts/sincronizar_commonplace.py --simular  # solo muestra qué haría
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys

BOVEDA = os.path.expanduser("~/Obsidian/Obsidian-index/commonplacebook")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(REPO, "content", "commonplace")
ESTADO = os.path.join(REPO, "scripts", ".estado_commonplace.json")

CARPETAS_BLOQUEADAS = ("00 Inbox", "50 Plantillas", "60 Adjuntos", ".obsidian", ".trash")
TEMAS_BLOQUEADOS = ("Salud y bienestar", "Salud mental")
TERMINOS_PRIVADOS = re.compile(
    r"bipolar|quetiapina|lamotrigina|antipsic|pregabalina|psicosis|man[ií]a\b|hipoman|"
    r"estabilizador del [aá]nimo|medicaci[oó]n|trastornos? del estado|dopamina|neurotransmisor|tdah|"
    r"cetogenia|dbsa",
    re.IGNORECASE,
)
IMAGENES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg")
CORREO = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ENLACE = re.compile(r"(!?)\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]*))?\]\]")
DATAVIEW = re.compile(r"```dataview(js)?\n.*?```\n?", re.DOTALL)
COMENTARIO = re.compile(r"%%.*?%%", re.DOTALL)
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def propiedades(texto):
    m = FRONTMATTER.match(texto)
    props = {}
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea and not linea.startswith((" ", "-")):
                k, v = linea.split(":", 1)
                props[k.strip().lower()] = v.strip().strip('"').strip("'")
    return props


def marcada(props):
    return props.get("publicar", props.get("publish", "")).lower() in ("true", "sí", "si", "yes")


def motivo_bloqueo(ruta_rel, nombre, props):
    partes = ruta_rel.split(os.sep)
    if partes[0] in CARPETAS_BLOQUEADAS:
        return f"carpeta {partes[0]}"
    if "texto completo" in nombre.lower():
        return "texto completo (derechos de autor)"
    tema = props.get("índice", "") + props.get("indice", "")
    if any(t in tema for t in TEMAS_BLOQUEADOS):
        return "tema de salud (privado)"
    if TERMINOS_PRIVADOS.search(nombre):
        return "título con información médica (privado)"
    return None


def indexar_boveda():
    notas, archivos = {}, {}
    for raiz, dirs, ficheros in os.walk(BOVEDA):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in ficheros:
            ruta = os.path.join(raiz, f)
            if f.endswith(".md"):
                notas[f[:-3]] = ruta
            else:
                archivos.setdefault(f, ruta)
    return notas, archivos


def seleccionar(notas):
    publicadas, bloqueadas = {}, []
    for nombre, ruta in notas.items():
        texto = open(ruta, encoding="utf-8", errors="replace").read()
        props = propiedades(texto)
        if not marcada(props):
            continue
        rel = os.path.relpath(ruta, BOVEDA)
        motivo = motivo_bloqueo(rel, nombre, props)
        if motivo:
            bloqueadas.append((rel, motivo))
        else:
            publicadas[nombre] = (ruta, rel, texto)
    return publicadas, bloqueadas


def transformar(texto, publicadas, archivos, imagenes_usadas):
    texto = DATAVIEW.sub("", texto)
    texto = COMENTARIO.sub("", texto)
    texto = CORREO.sub("[correo omitido]", texto)

    def reemplazo(m):
        incrustado, destino, ancla, alias = m.group(1), m.group(2).strip(), m.group(3) or "", m.group(4)
        base = os.path.basename(destino)
        if incrustado:
            if base.lower().endswith(IMAGENES) and base in archivos:
                imagenes_usadas.add(base)
                return f"![[{base}{'|' + alias if alias else ''}]]"
            if base.lower().endswith((".pdf", ".m4a", ".mp3", ".mp4", ".mov", ".canvas", ".base")):
                return ""
            if base in publicadas:
                return m.group(0)
            return ""
        if base in publicadas:
            return m.group(0)
        if base.lower().endswith((".pdf", ".m4a", ".mp3", ".mp4", ".canvas", ".base")):
            return alias or ""
        return alias or base
    return ENLACE.sub(reemplazo, texto)


TITULOS_AREA = {
    "Arte, imagen y cultura visual": "Cultura visual y estudios de la imagen",
    "Zettelkasten y gestión del conocimiento": "Zettelkasten y gestión del conocimiento",
}


def area_de(rel, props):
    tema = props.get("índice", "")
    for clave, titulo in TITULOS_AREA.items():
        if clave in tema or clave in rel:
            return titulo
    if rel.startswith("40 Proyectos"):
        return "Educación artística y problemas contemporáneos"
    return "Otras notas"


def portada(publicadas):
    grupos = {}
    for nombre, (ruta, rel, texto) in publicadas.items():
        grupos.setdefault(area_de(rel, propiedades(texto)), []).append(nombre)
    lineas = [
        "---",
        "title: Commonplace Book",
        "---",
        "",
        "Notas de lectura, ideas y materiales de curso que vienen de mi Commonplace Book en Obsidian, "
        "un Zettelkasten al estilo de Luhmann. Se actualizan a medida que la bóveda crece.",
        "",
    ]
    orden = list(TITULOS_AREA.values()) + ["Educación artística y problemas contemporáneos", "Otras notas"]
    for area in sorted(grupos, key=lambda a: orden.index(a) if a in orden else 99):
        lineas.append(f"## {area}\n")
        for n in sorted(grupos[area], key=lambda s: re.sub(r"^\d{12} - ", "", s).lower()):
            titulo = re.sub(r"^\d{12} - ", "", n)
            lineas.append(f"- [[{n}|{titulo}]]")
        lineas.append("")
    lineas.append(f"*Última actualización: {dt.date.today():%Y-%m-%d}.*")
    return "\n".join(lineas) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--simular", action="store_true", help="no escribe nada; solo muestra el informe")
    args = ap.parse_args()

    if not os.path.isdir(BOVEDA):
        sys.exit(f"No encuentro la bóveda en {BOVEDA}")
    notas, archivos = indexar_boveda()
    publicadas, bloqueadas = seleccionar(notas)

    anterior = {}
    if os.path.exists(ESTADO):
        anterior = json.load(open(ESTADO, encoding="utf-8"))
    actual, salida, imagenes = {}, {}, set()
    for nombre, (ruta, rel, texto) in publicadas.items():
        nuevo = transformar(texto, publicadas, archivos, imagenes)
        destino_rel = re.sub(r"^\d\d ", "", rel)
        salida[destino_rel] = nuevo
        actual[destino_rel] = hashlib.sha1(nuevo.encode()).hexdigest()

    nuevas = sorted(set(actual) - set(anterior))
    retiradas = sorted(set(anterior) - set(actual))
    cambiadas = sorted(k for k in set(actual) & set(anterior) if actual[k] != anterior[k])

    print(f"Bóveda: {BOVEDA}")
    print(f"Notas marcadas para publicar: {len(publicadas)} · imágenes: {len(imagenes)}")
    print(f"Nuevas: {len(nuevas)} · cambiadas: {len(cambiadas)} · retiradas: {len(retiradas)}")
    for etiqueta, lista in (("+", nuevas), ("~", cambiadas), ("-", retiradas)):
        for k in lista:
            print(f"  {etiqueta} {k}")
    if bloqueadas:
        print(f"\nBloqueadas aunque estén marcadas ({len(bloqueadas)}):")
        for rel, motivo in sorted(bloqueadas):
            print(f"  ✗ {rel} — {motivo}")
    if args.simular:
        print("\nSimulación: no se escribió nada.")
        return

    if os.path.isdir(DESTINO):
        shutil.rmtree(DESTINO)
    for rel, texto in salida.items():
        ruta = os.path.join(DESTINO, rel)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
    carpeta_img = os.path.join(DESTINO, "adjuntos")
    for img in imagenes:
        os.makedirs(carpeta_img, exist_ok=True)
        shutil.copy2(archivos[img], os.path.join(carpeta_img, img))
    with open(os.path.join(DESTINO, "index.md"), "w", encoding="utf-8") as f:
        f.write(portada(publicadas))
    json.dump(actual, open(ESTADO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nListo: {len(salida)} notas en content/commonplace/.")


if __name__ == "__main__":
    main()
