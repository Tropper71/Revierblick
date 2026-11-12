# Formulare: Überlassung erlaubnispflichtiger Schusswaffen

Private Vordrucke (keine amtlichen Formulare) für die Überlassung erlaubnispflichtiger Schusswaffen zwischen Privatpersonen.
Rechtsstand: WaffG i. d. F. der Änderung vom 20.03.2026 (BGBl. 2026 I Nr. 95), geprüft am 12.11.2026.

| Datei | Zweck |
|---|---|
| `Ueberlassung_Schusswaffen_Vordruck.pdf` | Blanko-Vordruck zum Ausdrucken |
| `Ueberlassung_Schusswaffen_ausfuellbar.pdf` | Am Bildschirm ausfüllbar (Acrobat Reader / Browser) |
| `Ueberlassung_Schusswaffen_Muster.pdf` | Ausgefülltes Beispiel mit erfundenen Daten (rot) |

Inhalt (je 4 Seiten):
1. Überlassungsprotokoll, Nachweis der Berechtigungsprüfung (§ 34 Abs. 1 WaffG)
2. Anzeige der Überlassung (§§ 37a Satz 1 Nr. 1, 37f, 37g WaffG)
3. Anzeige des Erwerbs (§§ 37a Satz 1 Nr. 2, 37f, 37g WaffG; § 13 Abs. 3 WaffG)
4. Hinweise zur Rechtslage

## Neu erzeugen

Benötigt Python 3 mit `reportlab`.

```bash
cd quelle
python3 build_form.py plain    # Blanko-Vordruck
python3 build_form.py fill     # ausfüllbare Version
python3 build_form.py sample   # Musterversion
```

Hinweis: Ersetzt keine Rechtsberatung. Maßgeblich ist der geltende Gesetzeswortlaut.
