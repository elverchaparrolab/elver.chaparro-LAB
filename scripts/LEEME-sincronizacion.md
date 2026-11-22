# Sincronización Obsidian → jardín digital

1. En Obsidian, a la nota que quieras publicar ponle la propiedad `publicar: true`
   (las plantillas ya traen `publicar: false`).
2. Ejecuta `python3 scripts/sincronizar_commonplace.py --simular` para ver qué cambiaría,
   y luego sin `--simular` para copiar las notas a `content/commonplace/`.
3. Haz commit y Push (GitHub Desktop). GitHub Actions publica el jardín en 1-2 minutos.

Nunca se publican: Inbox, plantillas, adjuntos PDF/audio, notas «texto completo»
ni notas de salud, aunque estén marcadas.
