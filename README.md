<p align="center"><img src="social-preview.png" width="100%" alt="Revierblick: kostenlose Jagd-App für Android mit Wetter und Wind, Büchsenlicht, Mond und Solunar, Revierkarte, Ansitzplanung, Jagdbuch und Jagdzeiten aus amtlichen Quellen"></p>

# Revierblick

**Die kostenlose Jagd-App für Android.** Wetter und Wind, Büchsenlicht, Mond und Solunar, Revierkarte mit Ständen, intelligente Ansitzplanung, Jagdbuch und Jagdzeiten aller Bundesländer in einer App. Ohne Werbung, ohne Konto, alle Revierdaten bleiben auf deinem Handy.

| | |
|---|---|
| **Aktuelle Version** | 2.2.0 vom 13.11.2026 |
| **Android** | 7.0 oder neuer |
| **Rechtsdaten** | Fassung 2026-11-10.3, wöchentlich gegen amtliche Quellen geprüft |
| **Handbuch** | 35 Seiten, passend zu Version 2.2.0 |

## Herunterladen

| Datei | Download |
|---|---|
| App, Version 2.2.0 | [Revierblick-2.2.0.apk](https://raw.githubusercontent.com/Tropper71/Revierblick/main/app/Revierblick-2.2.0.apk) |
| Handbuch (PDF) | [Revierblick-Handbuch.pdf](https://raw.githubusercontent.com/Tropper71/Revierblick/main/docs/Revierblick-Handbuch.pdf) |

### Installation
1. Die APK auf dem Handy herunterladen und antippen.
2. Beim ersten Mal die Installation aus dieser Quelle erlauben. Warnt Google Play Protect: *Trotzdem installieren*.
3. In den Android-Einstellungen die Akku-Optimierung für Revierblick auf *Nicht eingeschränkt* stellen, damit Meldungen pünktlich kommen.

**Update:** Neue Versionen einfach über die vorhandene installieren. Alle Daten bleiben erhalten, auch beim Wechsel von Revierkompass, Revierbuch oder Revierwetter. Ausführliche Anleitung im Handbuch, Kapitel 2.

## Neu in Version 2.2.0: Passende Stände auf Knopfdruck

Ein Tipp auf **Passende Stände jetzt finden** (in der Ansitzplanung, als Karte *Wo ansitzen?* auf der Startseite oder als Zielscheibe auf der Karte) prüft alle Stände für das nächste Ansitzfenster:

- **Ansitzfenster automatisch:** Morgen (15 Minuten vor Büchsenlicht bis 2 Stunden nach Sonnenaufgang), Abend (2,5 Stunden vor Sonnenuntergang bis Ende Büchsenlicht) oder frei gewählte Uhrzeit mit 1 bis 4 Stunden
- **Wind Stunde für Stunde** zur Blickrichtung oder zu den eingetragenen passenden Winden, mit Windleiste je Stand
- **Hauptzeit, Winddrehung, schwacher Wind** mit Hinweis auf die Thermik am Morgen und am Abend
- **Anmarsch:** neues Feld *Anmarsch kommt aus*. Die App warnt, wenn die Spurwitterung ins Sichtfeld zieht
- **Ruhe, Beanspruchung und Erfahrung:** letzter Ansitz, Ansitze in 14 Tagen, Anblick und Strecke am Stand
- **Ergebnis in vier Gruppen:** passt, bedingt, ohne Angaben, nicht geeignet, mit Begründung, Vormerken und Ansitz beginnen
- **Auf Karte:** Witterungsfahnen aller Stände zum Beginn des Fensters, Filter nach Revier

## Funktionen

- **Heute:** Büchsenlicht mit Restzeit, Tagesuhr mit Wind, Dämmerung, Solunar und Mond, *Wo ansitzen?*, Jagdzeiten des Tages, Fristen
- **Wetter:** amtliche DWD-Warnungen, Regenradar, 48 Stunden und 14 Tage, Luftdruckverlauf, Windkompass
- **Mond:** Phase, Auf- und Untergang, Mondkalender, Solunar-Perioden
- **Karte:** basemap.de, Luftbild und Flurstücke Brandenburg, OpenStreetMap, OpenTopoMap; Einrichtungen, Witterungsfahnen, Windpfeile, Entfernungsringe 100, 200 und 300 m, Messen, Pirschwege, Offline-Karten
- **Jagdbuch:** Ansitzbuch, Strecke, Nachsuche mit Anschuss und Wartezeit, Abschussplan, Wildschaden
- **Jagdrecht:** Jagdzeiten aller 16 Länder, für Brandenburg mit BbgJagdG, BbgJagdDV und Artenliste; Rechtsdaten per Online-Update mit Vorschau der Änderungen
- **Mehr:** Reviere teilen, Fristen und Nachweise, Drückjagdplanung mit Schussfeldern, Export nach Excel, KML, GeoJSON und GPX, Datensicherung
- Darstellung Dunkel, Hell und Rotlicht, Widget für den Startbildschirm

## Versionen

| Version | Datum | Inhalt |
|---|---|---|
| **2.2.0** | 13.11.2026 | Intelligente Standwahl auf Knopfdruck, Feld *Anmarsch kommt aus*, Handbuch auf 35 Seiten erweitert |
| 2.1.1 | 11.11.2026 | Update-Adresse auf das umbenannte Repository *Revierblick* umgestellt, alte Adresse wird automatisch ersetzt |
| 2.1.0 | 11.11.2026 | Neuer Name **Revierblick** (vorher Revierkompass), Lizenzangaben ergänzt |
| 2.0.8 | 10.11.2026 | basemap.de-Karte wird wieder angezeigt, Hinweis bei nicht erreichbarer Grundkarte |
| 2.0.7 | 10.11.2026 | Neues Icon, Hinweise zu Haftung und Datenschutz beim ersten Start, Seite *Über die App* mit Lizenzen |
| 2.0.5 bis 2.0.6 | 10.11.2026 | Jagdzeiten nur noch aus amtlichen Quellen, Qualitätsstufe je Bundesland, Länderdaten per Online-Update |
| 2.0.4 | 10.11.2026 | Rechtsdaten per Online-Update, Warnung bei geänderten Gesetzen |

## Rechtsdaten

Die App lädt die Rechtsdaten über diese Adresse:

```
https://raw.githubusercontent.com/Tropper71/Revierblick/main/rechtsdaten.json
```

- `wildarten`, `gesetz`, `verordnung`: Brandenburg (BbgJagdG, BbgJagdDV, JagdZeitV)
- `laender`: übrige Bundesländer mit Qualitätsstufe
  - **A** amtlicher Text (amtliches Portal oder Gesetzblatt)
  - **B** Verordnungswortlaut aus nicht amtlicher Rechtsdatenbank
  - **C** Landesrecht nicht ausgewertet, nur Bundesrahmen
- `quellen`, `aenderungen`: Fundstellen und Änderungsprotokoll

Verlagstabellen werden nicht verwendet. Die Datei wird jede Woche gegen die amtlichen Quellen geprüft. Neue Fassungen meldet die App und übernimmt sie erst nach Bestätigung.

## Lizenz

- **Rechtsdaten** (`rechtsdaten.json`): CC0 1.0 Universal, siehe [LICENSE](LICENSE). Die Datei LICENSE gilt nur für die Rechtsdaten.
- **App, Handbuch und Bilder** (`app/`, `docs/Revierblick-Handbuch.pdf`, `icon.png`, `social-preview.png`): © 2026 Tropper71. Kostenlose Nutzung und unveränderte Weitergabe erlaubt, alle übrigen Rechte vorbehalten.
- **Bausteine Dritter in der App:** Leaflet (BSD-2-Clause), Schriften Barlow und Barlow Condensed (SIL Open Font License 1.1). Die Lizenztexte stehen in der App unter *Mehr > Über die App*.

## Haftungsausschluss

Zusammenstellung nach bestem Wissen aus den im Feld `quellen` genannten Fundstellen.
Keine Rechtsberatung, keine Gewähr für Richtigkeit und Aktualität. Maßgeblich sind allein
die amtlich verkündeten Gesetze und Verordnungen sowie Allgemeinverfügungen der Jagdbehörden.
