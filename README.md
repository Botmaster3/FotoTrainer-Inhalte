# FotoTrainer – Inhalte

Dieses öffentliche Repository enthält **nur die Inhalte-Datenbank** des FotoTrainers, also die Kameramodelle und den Fragenkatalog.
Das Programm selbst liegt in einem anderen, privaten Repository.

Die FotoTrainer-Apps für Mac, Windows und Browser fragen beim Start nach, ob es hier eine neuere Version gibt. Sie lesen dafür diese Adresse:

```
https://raw.githubusercontent.com/Botmaster3/fototrainer-inhalte/main/inhalte/aktuell.json
```

Dabei werden **keine persönlichen Daten** übertragen, weder Profile noch Lernstand.

## Aufbau

| Datei | Wozu |
|---|---|
| `inhalte/aktuell.json` | Die gültige Datenbank. Diese Datei lesen die Apps. |
| `inhalte/archiv/` | Frühere Versionen zum Nachschlagen oder Zurückholen. |
| `pruefen.py` | Prüft die Datenbank genauso wie die App beim Import. |
| `.github/workflows/pruefen.yml` | Startet die Prüfung bei jeder Änderung automatisch. |

## Neue Inhalte veröffentlichen

1. **Bearbeiten:** In `FotoTrainer-Entwickler.html` → Profilmenü → „🛠 Entwicklermodus …“ Fragen und Kameras ändern.
2. **Version erhöhen:** Im Reiter „Datenbank“ die **Version** erhöhen (z. B. von 1 auf 2) und unter „Was ist neu?“ einen kurzen Satz eintragen.
3. **Exportieren:** „⬇︎ Zum Veröffentlichen (aktuell.json)“ klicken.
4. **Hochladen:**
   - Auf GitHub den Ordner `inhalte` öffnen, dann **Add file → Upload files**.
   - Die heruntergeladene `aktuell.json` hineinziehen, unten **Commit changes** klicken.
   - Die alte Datei wird dabei ersetzt.
5. **Prüfung abwarten:**
   - Ein grüner Haken beim Commit heißt: Alles ist in Ordnung, die Apps bieten die neue Version beim nächsten Start an.
   - Ein rotes Kreuz heißt: Fehler. Die Details stehen unter **Actions**.
6. **Optional fürs Archiv:** Dieselbe Datei als `archiv/FotoTrainer-Inhalte-v2.json` hochladen.

## Regeln

- Die **Version muss steigen**, sonst bieten die Apps das Update nicht an.
- `minAppVersion` nennt die älteste App-Version, die mit den Inhalten zurechtkommt. Ältere Apps zeigen dann den Hinweis „neuere App-Version nötig“.
- Ein Eintrag mit `"active": false` bleibt in der Datei, wird in den Apps aber nicht angezeigt.
- Ist doch etwas schiefgegangen: Die Datei aus `archiv/` wieder als `aktuell.json` hochladen und dabei die Version erhöhen.
