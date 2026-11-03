#!/usr/bin/env python3
"""Prüft inhalte/aktuell.json genauso wie die FotoTrainer-App beim Import.

Aufruf:  python3 pruefen.py [Datei] [--vorher alte-datei.json]
Ohne Fehler endet das Skript mit „OK“. Läuft automatisch bei jeder Änderung (GitHub Actions).
"""
import json
import sys

CATEGORIES = set(["blende","verschlusszeit","iso","belichtung","messung","weissabgleich","raw","blitz","gestaltung","ausruestung","workflow","genres","modi","kamera"])
args = sys.argv[1:]
old = None
if "--vorher" in args:
    i = args.index("--vorher")
    old = args[i + 1]
    del args[i:i + 2]
path = args[0] if args else "inhalte/aktuell.json"
errors = []


def version_tuple(v):
    return tuple(int(p) if p.isdigit() else 0 for p in str(v).replace("-", ".").split("."))


try:
    c = json.load(open(path, encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    sys.exit(f"FEHLER: {path} ist kein gültiges JSON: {e}")

if c.get("format") != "fototrainer-inhalte":
    errors.append('Feld "format" muss "fototrainer-inhalte" sein')
for key in ("version", "cameras", "questions"):
    if key not in c:
        errors.append(f'Feld "{key}" fehlt')
cams = c.get("cameras") or []
qs = c.get("questions") or []
cam_ids = set()
for cam in cams:
    cid = cam.get("id", "?")
    if not cam.get("id") or not cam.get("brand") or not cam.get("model") or cam.get("kind") not in ("dslr", "mirrorless"):
        errors.append(f"Kamera {cid}: Pflichtangaben fehlen (id, brand, model, kind)")
    if not (cam.get("layout") or {}).get("elements"):
        errors.append(f"Kamera {cid}: Zeichnung (layout.elements) fehlt")
    if cid in cam_ids:
        errors.append(f"Kamera {cid}: doppelte ID")
    cam_ids.add(cid)
q_ids = set()
for q in qs:
    qid = q.get("id", "?")
    opts = q.get("options")
    if not q.get("id") or not q.get("text") or not isinstance(opts, list) or len(opts) < 2:
        errors.append(f"Frage {qid}: Text oder Antworten fehlen")
    elif not (isinstance(q.get("correctIndex"), int) and 0 <= q["correctIndex"] < len(opts)):
        errors.append(f"Frage {qid}: richtige Antwort (correctIndex) fehlt")
    if q.get("category") not in CATEGORIES:
        errors.append(f"Frage {qid}: unbekanntes Thema {q.get('category')!r}")
    if qid in q_ids:
        errors.append(f"Frage {qid}: doppelte ID")
    q_ids.add(qid)
    for ref in q.get("cameras") or []:
        if ref not in cam_ids:
            errors.append(f"Frage {qid}: unbekannte Kamera {ref}")
if not any(x.get("active", True) is not False for x in cams):
    errors.append("Mindestens eine Kamera muss aktiv sein")
if not any(x.get("active", True) is not False for x in qs):
    errors.append("Mindestens eine Frage muss aktiv sein")

if old:
    try:
        prev = json.load(open(old, encoding="utf-8"))
        if version_tuple(c.get("version")) <= version_tuple(prev.get("version")):
            errors.append(f"Version {c.get('version')} ist nicht höher als die bisherige ({prev.get('version')}) – die Apps würden das Update nicht anbieten")
    except FileNotFoundError:
        pass

if errors:
    print("FEHLER in", path)
    for e in errors[:50]:
        print("  •", e)
    sys.exit(1)
print(f"OK – Version {c['version']}: {sum(x.get('active', True) is not False for x in cams)}/{len(cams)} Kameras, "
      f"{sum(x.get('active', True) is not False for x in qs)}/{len(qs)} Fragen aktiv")
