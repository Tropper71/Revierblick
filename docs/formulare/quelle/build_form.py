# -*- coding: utf-8 -*-
"""Erzeugt einen ausfüllbaren Blanko-Vordruck zur Überlassung erlaubnispflichtiger
Schusswaffen (Privat an Privat) nach WaffG, Stand 20.03.2026."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

W, H = A4
M = 36                      # Seitenrand
CW = W - 2 * M              # Inhaltsbreite
DARK = colors.HexColor("#1f3a5f")
LIGHT = colors.HexColor("#e8eef5")
GRID = colors.HexColor("#7a8796")

import sys
from sample_data import SAMPLE

# MODE: "plain" (bisherige Version), "fill" (Bildschirmversion), "sample" (Musterdaten rot)
MODE = sys.argv[1] if len(sys.argv) > 1 else "plain"
OUT = {"plain": "Ueberlassung_Schusswaffen_Vordruck.pdf",
       "fill": "Ueberlassung_Schusswaffen_ausfuellbar.pdf",
       "sample": "Ueberlassung_Schusswaffen_Muster.pdf"}[MODE]
RED = colors.HexColor("#c0141c")
FIELD_BG = colors.HexColor("#eaf2ff")

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Überlassung erlaubnispflichtiger Schusswaffen - Vordruck")
c.setAuthor("Privater Vordruck")
c.setSubject("Überlassungsprotokoll und Anzeigen nach §§ 34, 37a, 37f, 37g WaffG")
form = c.acroForm
import os
ROWS = {"S1": 9, "S2": 11, "S3": 9}
if os.environ.get("ROWS"):
    ROWS.update(dict(zip(["S1", "S2", "S3"], map(int, os.environ["ROWS"].split(",")))))
END = {}
page_no = [0]


def tf(name, x, y, w, h, tip="", fs=8.5, multi=False):
    """Textfeld je nach Modus: Formularfeld oder rot gedruckter Musterwert."""
    if MODE == "sample":
        val = SAMPLE.get(name)
        if val:
            size = fs
            while c.stringWidth(val, "Helvetica-Bold", size) > w - 2 and size > 5:
                size -= 0.25
            c.setFillColor(RED)
            c.setFont("Helvetica-Bold", size)
            c.drawString(x + 1, y + (h - size) / 2 + 1, val)
            c.setFillColor(colors.black)
        return
    kw = dict(name=name, x=x, y=y, width=w, height=h, borderWidth=0,
              textColor=colors.black, fontSize=fs, fontName="Helvetica",
              tooltip=tip or name)
    if MODE == "fill":
        kw["fillColor"] = FIELD_BG
        if multi:
            kw["fieldFlags"] = "multiline"
    else:
        kw["fillColor"] = colors.white
    form.textfield(**kw)


def cb(name, x, y, size, tip=""):
    """Ankreuzfeld je nach Modus."""
    if MODE == "sample":
        c.setStrokeColor(GRID)
        c.setLineWidth(0.8)
        c.rect(x, y, size, size, stroke=1, fill=0)
        if SAMPLE.get(name):
            c.setStrokeColor(RED)
            c.setLineWidth(1.4)
            c.line(x + 1.5, y + 1.5, x + size - 1.5, y + size - 1.5)
            c.line(x + 1.5, y + size - 1.5, x + size - 1.5, y + 1.5)
        c.setStrokeColor(GRID)
        return
    form.checkbox(name=name, x=x, y=y, size=size, buttonStyle="cross", borderWidth=0.8,
                  borderColor=GRID, fillColor=FIELD_BG if MODE == "fill" else colors.white,
                  textColor=colors.black, tooltip=tip or name)


def watermark():
    """Diagonales MUSTER-Wasserzeichen auf jeder Seite der Musterversion."""
    if MODE != "sample":
        return
    c.saveState()
    c.setFillColor(colors.Color(0.85, 0.1, 0.1, alpha=0.10))
    c.setFont("Helvetica-Bold", 120)
    c.translate(W / 2, H / 2)
    c.rotate(50)
    c.drawCentredString(0, -40, "MUSTER")
    c.restoreState()
TOTAL_PAGES = 4


def footer():
    """Fußzeile mit Hinweis auf nichtamtlichen Charakter und Rechtsstand."""
    page_no[0] += 1
    watermark()
    if MODE == "sample":
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(RED)
        c.drawString(M, 30, "MUSTER - alle Personen-, Waffen- und Behördendaten sind frei erfunden. Rot = Beispieleintrag.")
    c.setFont("Helvetica", 6.5)
    c.setFillColor(GRID)
    c.drawString(M, 20, "Privater Vordruck, kein amtliches Formular. Rechtsstand: WaffG i. d. F. der Änderung vom 20.03.2026 (BGBl. 2026 I Nr. 95).")
    c.drawRightString(W - M, 20, f"Seite {page_no[0]} von {TOTAL_PAGES}")
    c.setFillColor(colors.black)


def title(text, sub=None, y=H - M):
    """Seitentitel mit optionaler Unterzeile; gibt neue y-Position zurück."""
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y - 14, text)
    y -= 20
    if sub:
        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.black)
        for line in sub:
            c.drawString(M, y - 9, line)
            y -= 11
    c.setStrokeColor(DARK)
    c.setLineWidth(1.2)
    c.line(M, y - 3, W - M, y - 3)
    c.setFillColor(colors.black)
    return y - 10


def section(y, text):
    """Abschnittsbalken."""
    c.setFillColor(DARK)
    c.rect(M, y - 13, CW, 13, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M + 4, y - 9.5, text)
    c.setFillColor(colors.black)
    return y - 13


def row(y, prefix, specs, h=22):
    """Zeile aus beschrifteten Feldern. specs = [(Label, Anteil, Feldname), ...]"""
    total = sum(s[1] for s in specs)
    x = M
    c.setStrokeColor(GRID)
    c.setLineWidth(0.6)
    for label, frac, name in specs:
        w = CW * frac / total
        c.rect(x, y - h, w, h, stroke=1, fill=0)
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.HexColor("#33414f"))
        c.drawString(x + 2.5, y - 7, label)
        c.setFillColor(colors.black)
        tf(f"{prefix}_{name}", x + 2, y - h + 1.5, w - 4, h - 10, tip=label, multi=h > 26)
        x += w
    return y - h


def checkline(y, prefix, name, text, size=8, indent=0, width=None):
    """Ankreuzfeld mit Text (mehrzeilig möglich)."""
    style = ParagraphStyle("cb", fontName="Helvetica", fontSize=7.5, leading=9.2)
    p = Paragraph(text, style)
    tw = (width or CW) - 16 - indent
    _, ph = p.wrap(tw, 200)
    cb(f"{prefix}_{name}", M + indent, y - size - 1, size, tip=re.sub("<[^>]+>", "", text)[:120])
    p.drawOn(c, M + indent + 14, y - ph)
    return y - max(ph, size + 2) - 3


def para(y, text, size=7.5, leading=9.4, width=None, x=None, bold=False):
    style = ParagraphStyle("p", fontName="Helvetica-Bold" if bold else "Helvetica",
                           fontSize=size, leading=leading)
    p = Paragraph(text, style)
    _, ph = p.wrap(width or CW, 1000)
    p.drawOn(c, x or M, y - ph)
    return y - ph


def signatures(y, prefix, labels, h=34):
    """Unterschriftszeilen nebeneinander: Ort/Datum + Unterschrift."""
    n = len(labels)
    gap = 14
    w = (CW - gap * (n - 1)) / n
    for i, lab in enumerate(labels):
        x = M + i * (w + gap)
        tf(f"{prefix}_ortdatum_{i}", x, y - 14, w, 12, tip="Ort, Datum")
        if MODE == "sample" and SAMPLE.get(f"{prefix}_sig_{i}"):
            c.setFillColor(RED)
            c.setFont("Helvetica-BoldOblique", 12)
            c.drawString(x + w * 0.4, y - h + 3, SAMPLE[f"{prefix}_sig_{i}"])
            c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.6)
        c.line(x, y - h, x + w, y - h)
        c.setFont("Helvetica", 6.5)
        c.drawString(x, y - 21, "Ort, Datum")
        c.drawString(x, y - h - 8, lab)
    return y - h - 12


def person_full(y, p):
    """Volldatensatz nach § 37f Abs. 1 Nr. 3 / Abs. 2 Nr. 3 WaffG."""
    y = row(y, p, [("Familienname (a)", 3, "name"), ("Vorname(n) (d)", 3, "vorname"),
                   ("Doktorgrad (e)", 1.3, "dr")])
    y = row(y, p, [("Geburtsname (c)", 2.5, "gebname"), ("Früherer Name (b)", 2.5, "frname"),
                   ("Geschlecht (h)", 1.2, "geschl")])
    y = row(y, p, [("Geburtsdatum (f)", 1.5, "gebdat"), ("Geburtsort, ggf. Staat (g)", 2.5, "gebort"),
                   ("Jede Staatsangehörigkeit (i)", 2.5, "staat")])
    y = row(y, p, [("Straße, Hausnummer (j)", 3, "str"), ("PLZ (j)", 1, "plz"),
                   ("Ort, bei Auslandsanschrift auch Staat (j)", 3, "ort")])
    return y


def person_short(y, p):
    """Erwerberdaten nach § 37f Abs. 2 Nr. 1 WaffG."""
    y = row(y, p, [("Familienname (a)", 3, "name"), ("Vorname(n) (b)", 3, "vorname"),
                   ("Geburtsdatum (c)", 1.5, "gebdat")])
    y = row(y, p, [("Geburtsort (d)", 2.2, "gebort"), ("Straße, Hausnummer (e)", 2.8, "str"),
                   ("PLZ, Ort (e)", 2.5, "ort")])
    return y


def weapon_table(y, p, rows=3):
    """Waffendaten nach § 37f Abs. 1 Nr. 5 WaffG."""
    cols = [("Nr.", 0.35), ("Art der Waffe (h)\nz. B. Repetierbüchse", 1.7), ("Hersteller (a)", 1.4),
            ("Modell (b)", 1.3), ("Kaliber (c)", 1.0), ("Seriennummer (d)", 1.4),
            ("Jahr Fertig-\nstellung (e)", 0.75), ("Verbringen\nin DE (f)", 0.75), ("Kat.\n(g)", 0.5)]
    total = sum(x[1] for x in cols)
    hh, rh = 18, 18
    x = M
    c.setFillColor(LIGHT)
    c.rect(M, y - hh, CW, hh, stroke=0, fill=1)
    c.setFillColor(colors.black)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.6)
    for lab, fr in cols:
        w = CW * fr / total
        c.rect(x, y - hh - rh * rows, w, hh + rh * rows, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 5.8)
        for k, ln in enumerate(lab.split("\n")):
            c.drawString(x + 2, y - 7 - k * 6.5, ln)
        x += w
    for r in range(rows):
        yy = y - hh - rh * (r + 1)
        c.line(M, yy, W - M, yy)
        x = M
        for j, (lab, fr) in enumerate(cols):
            w = CW * fr / total
            if j == 0:
                c.setFont("Helvetica", 7.5)
                c.drawCentredString(x + w / 2, yy + 6, str(r + 1))
            else:
                tf(f"{p}_w{r + 1}_{j}", x + 1.5, yy + 2, w - 3, rh - 4,
                   tip=f"Waffe {r + 1}: " + lab.replace("\n", " "), fs=7.5)
            x += w
    return y - hh - rh * rows


# ---------------------------------------------------------------------------
# SEITE 1: Überlassungsprotokoll (Nachweis der Berechtigungsprüfung, § 34 Abs. 1)
# ---------------------------------------------------------------------------
P = "S1"
y = title("Überlassungsprotokoll für erlaubnispflichtige Schusswaffen",
          ["zwischen Privatpersonen  |  Nachweis der Berechtigungsprüfung nach § 34 Abs. 1 WaffG",
           "Je ein Exemplar für Überlassenden und Erwerber. Waffen dürfen nur an berechtigte Personen überlassen werden;",
           "die Berechtigung muss offensichtlich sein oder nachgewiesen werden."])
y = section(y, "1  Überlassender")
y = person_full(y, P + "u")
y = row(y, P + "u", [("Nr. der eigenen Waffenbesitzkarte", 2, "wbk"), ("Ausstellende Behörde", 3, "beh"),
                     ("NWR-ID der Erlaubnis (E-..., falls bekannt)", 2, "nwr")])
y -= 6
y = section(y, "2  Erwerber")
y = person_short(y, P + "e")
y = row(y, P + "e", [("Identität geprüft anhand (Personalausweis / Reisepass), Dokument-Nr.", 4, "ausweis"),
                     ("Ausstellende Stelle", 2.5, "ausweisbeh")])
y -= 3
c.setFont("Helvetica-Bold", 7.5)
c.drawString(M, y - 8, "Nachweis der Erwerbsberechtigung (im Original eingesehen):")
y -= 11
y = checkline(y, P, "cb_wbk", "<b>Waffenbesitzkarte</b> mit Erwerbsberechtigung (Voreintrag bzw. gelbe WBK, Kategorie passend zur Waffe)")
y = checkline(y, P, "cb_js", "<b>Gültiger Jahresjagdschein</b> (§ 13 Abs. 3 WaffG): nur für Langwaffen; der Erwerber muss binnen zwei Wochen "
                         "die Ausstellung einer WBK beantragen.")
y = checkline(y, P, "cb_sonst", "Sonstige Erlaubnis (z. B. Waffenhandelserlaubnis § 21 WaffG, Europäischer Feuerwaffenpass):")
y = row(y, P + "e", [("Art der Erlaubnis", 2.4, "erl_art"), ("Nummer", 1.6, "erl_nr"),
                     ("Ausstellende Behörde", 2.4, "erl_beh"), ("Gültig bis", 1, "erl_gueltig")])
y -= 6
y = section(y, "3  Überlassene Waffe(n)  (Daten wie in der WBK eingetragen)")
y = weapon_table(y, P, rows=ROWS[P])
y = row(y, P, [("Mitüberlassene Munition: Kaliber / Stückzahl (nur bei Munitionserwerbsberechtigung)", 4, "mun"),
               ("Mitüberlassenes Zubehör (z. B. Zielfernrohr, Magazine)", 3, "zub")], h=20)
y -= 6
y = section(y, "4  Überlassung")
y = row(y, P, [("Datum der Überlassung", 1.4, "datum"), ("Uhrzeit", 0.8, "zeit"), ("Ort der Übergabe", 2.6, "ort"),
               ("Kaufpreis / Gegenleistung (freiwillig)", 1.8, "preis")])
yy = y - 3
c.setFont("Helvetica", 7.5)
c.drawString(M, yy - 8, "Art:")
xx = M + 22
for i, t in enumerate(["Verkauf", "Schenkung", "Leihe (befristet bis: ________)", "Sonstiges: ______________"]):
    cb(f"{P}_art{i}", xx, yy - 10, 8, tip="Art: " + t)
    c.drawString(xx + 11, yy - 8, t)
    xx += [62, 70, 140, 0][i]
y = yy - 16
y = section(y, "5  Erklärungen")
y = checkline(y, P, "erk1", "Der Überlassende hat die Erwerbsberechtigung und die Identität des Erwerbers anhand der Originaldokumente geprüft.")
y = checkline(y, P, "erk2", "Die Waffe(n) wurde(n) entladen übergeben. Der Erwerber hat die Waffe(n) in dem besichtigten Zustand übernommen.")
y = checkline(y, P, "erk3", "Der Überlassende zeigt die Überlassung binnen zwei Wochen der für ihn zuständigen Waffenbehörde an und legt seine "
                          "WBK zur Berichtigung vor (§§ 37a Satz 1 Nr. 1, 37g Abs. 1 WaffG).")
y = checkline(y, P, "erk4", "Der Erwerber zeigt den Erwerb binnen zwei Wochen an und legt seine WBK zur Eintragung vor (§§ 37a Satz 1 Nr. 2, "
                          "37g Abs. 1 WaffG) bzw. beantragt als Jagdscheininhaber binnen zwei Wochen die WBK (§ 13 Abs. 3 WaffG).")
y -= 4
END[P] = signatures(y, P, ["Unterschrift Überlassender", "Unterschrift Erwerber"], h=32)
footer()
c.showPage()

# ---------------------------------------------------------------------------
# SEITE 2: Anzeige der Überlassung (§ 37a Satz 1 Nr. 1 i. V. m. § 37f WaffG)
# ---------------------------------------------------------------------------
P = "S2"
y = title("Anzeige der Überlassung einer erlaubnispflichtigen Schusswaffe",
          ["gemäß § 37a Satz 1 Nr. 1 i. V. m. § 37f WaffG  |  Frist: binnen zwei Wochen, schriftlich oder elektronisch",
           "Bitte gleichzeitig die Waffenbesitzkarte (ggf. auch den Europäischen Feuerwaffenpass) zur Berichtigung vorlegen (§ 37g Abs. 1 WaffG)."])
y = row(y, P, [("An die zuständige Waffenbehörde (Bezeichnung, Anschrift)", 1, "behoerde")], h=34)
y -= 6
y = section(y, "1  Anzeigender / Überlassender  (§ 37f Abs. 1 Nr. 3, Abs. 2 Nr. 3 WaffG)")
y = person_full(y, P + "u")
y = row(y, P + "u", [("Telefon / E-Mail (freiwillig)", 1, "kontakt")], h=20)
y -= 6
y = section(y, "2  Erlaubnis des Anzeigenden  (§ 37f Abs. 1 Nr. 7 bis 9 WaffG)")
y = row(y, P + "u", [("Art der Erlaubnis (z. B. WBK grün / gelb)", 2.2, "erl_art"), ("Gültigkeit", 1.2, "erl_gueltig"),
                     ("Nr. der Erlaubnisurkunde", 1.6, "erl_nr"), ("Ausstellende Behörde", 2.2, "erl_beh")])
y -= 6
y = section(y, "3  Sachverhalt  (§ 37f Abs. 1 Nr. 1 und 2 WaffG)")
y = para(y - 3, "Ich zeige hiermit an, dass ich die nachstehend bezeichnete(n) erlaubnispflichtige(n) Schusswaffe(n) <b>überlassen</b> habe "
                "und beantrage die Austragung aus meiner Waffenbesitzkarte.", size=7.8)
y -= 2
y = row(y, P, [("Datum der Überlassung", 1.5, "datum"), ("Austragung aus WBK-Nr.", 2, "wbk"),
               ("Lfd. Nr. des Eintrags in der WBK", 2, "lfdnr")])
y -= 6
y = section(y, "4  Waffe(n)  (§ 37f Abs. 1 Nr. 5 WaffG)")
y = weapon_table(y, P, rows=ROWS[P])
y -= 6
y = section(y, "5  Erwerber  (§ 37f Abs. 2 Nr. 1 und 2 WaffG)")
y = person_short(y, P + "e")
y = row(y, P + "e", [("Nr. der WBK des Erwerbers (bei Nachweis durch WBK)", 2.4, "wbk"), ("Ausstellende Behörde", 2.6, "beh"),
                     ("Sonst. Nachweis (z. B. Jagdschein-Nr., Behörde)", 2.6, "sonst")])
y -= 6
y = section(y, "6  Anlagen")
y = checkline(y, P, "anl1", "Waffenbesitzkarte im Original zur Berichtigung (§ 37g Abs. 1 WaffG)")
y = checkline(y, P, "anl2", "Kopie des Überlassungsprotokolls")
y = checkline(y, P, "anl3", "Europäischer Feuerwaffenpass (sofern die Waffe dort eingetragen ist)")
y -= 6
y = para(y, "Ich versichere die Richtigkeit und Vollständigkeit meiner Angaben.", size=7.5)
y -= 6
END[P] = signatures(y, P, ["Unterschrift Anzeigender"], h=30)
footer()
c.showPage()

# ---------------------------------------------------------------------------
# SEITE 3: Anzeige des Erwerbs (§ 37a Satz 1 Nr. 2 i. V. m. § 37f WaffG)
# ---------------------------------------------------------------------------
P = "S3"
y = title("Anzeige des Erwerbs einer erlaubnispflichtigen Schusswaffe",
          ["gemäß § 37a Satz 1 Nr. 2 i. V. m. § 37f WaffG  |  Frist: binnen zwei Wochen, schriftlich oder elektronisch",
           "Bitte gleichzeitig die Waffenbesitzkarte zur Eintragung vorlegen (§ 37g Abs. 1 WaffG)."])
y = row(y, P, [("An die zuständige Waffenbehörde (Bezeichnung, Anschrift)", 1, "behoerde")], h=34)
y -= 6
y = section(y, "1  Anzeigender / Erwerber  (§ 37f Abs. 1 Nr. 3 WaffG)")
y = person_full(y, P + "e")
y = row(y, P + "e", [("Telefon / E-Mail (freiwillig)", 1, "kontakt")], h=20)
y -= 6
y = section(y, "2  Erlaubnis des Anzeigenden  (§ 37f Abs. 1 Nr. 7 bis 9 WaffG)")
y = row(y, P + "e", [("Art der Erlaubnis (z. B. WBK grün / gelb)", 2.2, "erl_art"), ("Gültigkeit", 1.2, "erl_gueltig"),
                     ("Nr. der Erlaubnisurkunde", 1.6, "erl_nr"), ("Ausstellende Behörde", 2.2, "erl_beh")])
y = checkline(y - 3, P, "js", "Erwerb einer Langwaffe als Inhaber eines Jahresjagdscheins ohne bestehende WBK: Hiermit beantrage ich "
                              "zugleich die Ausstellung einer Waffenbesitzkarte (§ 13 Abs. 3 Satz 2 WaffG). Jagdschein-Nr. / Behörde:")
y = row(y, P + "e", [("Jagdschein-Nr.", 2, "js_nr"), ("Ausstellende Behörde", 3, "js_beh"), ("Gültig bis", 1.2, "js_gueltig")])
y -= 6
y = section(y, "3  Sachverhalt  (§ 37f Abs. 1 Nr. 1 und 2 WaffG)")
y = para(y - 3, "Ich zeige hiermit an, dass ich die nachstehend bezeichnete(n) erlaubnispflichtige(n) Schusswaffe(n) <b>erworben</b> habe "
                "und beantrage die Eintragung in meine Waffenbesitzkarte.", size=7.8)
y -= 2
y = row(y, P, [("Datum des Erwerbs", 1.5, "datum"), ("Eintragung in WBK-Nr.", 2, "wbk"),
               ("Genutzter Voreintrag / Erwerbsberechtigung", 2.5, "vor")])
y -= 6
y = section(y, "4  Waffe(n)  (§ 37f Abs. 1 Nr. 5 WaffG)")
y = weapon_table(y, P, rows=ROWS[P])
y -= 6
y = section(y, "5  Überlassender  (§ 37f Abs. 2 Nr. 3 WaffG)")
y = person_full(y, P + "u")
y -= 6
y = checkline(y, P, "anl1", "Anlage: Waffenbesitzkarte im Original zur Eintragung (§ 37g Abs. 1 WaffG); Kopie des Überlassungsprotokolls")
y = para(y - 2, "Ich versichere die Richtigkeit und Vollständigkeit meiner Angaben.", size=7.5)
y -= 6
END[P] = signatures(y, P, ["Unterschrift Anzeigender"], h=30)
footer()
c.showPage()

# ---------------------------------------------------------------------------
# SEITE 4: Hinweise
# ---------------------------------------------------------------------------
y = title("Hinweise zum Ausfüllen und zur Rechtslage", ["Stand der Prüfung: 12.11.2026"])
blocks = [
    ("Wer darf erwerben? (§ 34 Abs. 1 WaffG)",
     "Waffen und Munition dürfen nur berechtigten Personen überlassen werden. Die Berechtigung muss offensichtlich sein oder "
     "nachgewiesen werden. Lassen Sie sich die Originaldokumente (WBK mit passender Erwerbsberechtigung bzw. gültigen "
     "Jahresjagdschein) und einen amtlichen Lichtbildausweis zeigen. Das Überlassungsprotokoll (Seite 1) dokumentiert diese Prüfung; "
     "es ist gesetzlich nicht vorgeschrieben, aber dringend zu empfehlen."),
    ("Anzeigepflicht des Überlassenden (§ 37a Satz 1 Nr. 1, § 37g WaffG)",
     "Inhaber einer WBK müssen die Überlassung einer erlaubnispflichtigen Schusswaffe binnen zwei Wochen schriftlich oder elektronisch "
     "der zuständigen Behörde anzeigen und gleichzeitig die WBK zur Berichtigung vorlegen. Zuständig ist die Waffenbehörde am eigenen Wohnsitz."),
    ("Anzeigepflicht des Erwerbers (§ 37a Satz 1 Nr. 2, § 37g WaffG; § 13 Abs. 3 WaffG)",
     "Der Erwerber zeigt den Erwerb ebenfalls binnen zwei Wochen an und legt seine WBK zur Eintragung vor. Inhaber eines "
     "Jahresjagdscheins dürfen Langwaffen ohne vorherige WBK erwerben, müssen aber binnen zwei Wochen nach Erwerb die Ausstellung "
     "einer WBK beantragen."),
    ("Pflichtangaben (§ 37f WaffG)",
     "Die Buchstaben in den Feldbeschriftungen (a), (b) usw. verweisen auf die jeweilige Nummer des § 37f WaffG. Die Kategorie (g) "
     "richtet sich nach Anlage 1 Abschnitt 3 WaffG (z. B. A, B, C). Für die Erwerberdaten verlangt das Gesetz nur Name, Vorname, "
     "Geburtsdatum, Geburtsort, Anschrift sowie bei WBK deren Nummer und ausstellende Behörde (§ 37f Abs. 2 Nr. 1 und 2). "
     "Ist ein Beteiligter nicht vom Anwendungsbereich des WaffG erfasst, genügen Name und Anschrift (§ 37f Abs. 3). Ist ein Magazin "
     "selbst Gegenstand der Anzeige, sind zusätzlich Kapazität, kleinste verwendbare Munition und ggf. Beschriftung anzugeben (§ 37f Abs. 1 Nr. 6)."),
    ("Keine Anzeige erforderlich (§ 37e Abs. 3 WaffG)",
     "In den Fällen des § 12 Abs. 1 WaffG (z. B. vorübergehende Überlassung unter Aufsicht oder zum Schießen auf einer Schießstätte) "
     "sowie bei Überlassung an einen Waffenhändler nach § 21 Abs. 1 Satz 1 WaffG zur Verwahrung, Instandsetzung oder geringfügigen "
     "Änderung oder zum Kommissionsverkauf."),
    ("Erwerber mit Wohnsitz im EU-Ausland (§ 34 Abs. 4 WaffG)",
     "Wer einer Person mit gewöhnlichem Aufenthalt in einem anderen Mitgliedstaat eine Schusswaffe der Kategorien B oder C überlässt, "
     "muss dies zusätzlich unverzüglich schriftlich dem Bundesverwaltungsamt anzeigen. Dieser Vordruck ist dafür nicht ausgelegt."),
    ("Behördenvordrucke und Online-Verfahren",
     "Viele Waffenbehörden stellen eigene Vordrucke oder ein Online-Verfahren bereit, teils mit NWR-ID-Feldern. Erkundigen Sie sich vorab, "
     "ob Ihre Behörde ihren eigenen Vordruck verlangt. Inhaltlich deckt dieser Vordruck die gesetzlichen Pflichtangaben vollständig ab."),
    ("Ordnungswidrigkeit",
     "Eine nicht, nicht richtig, nicht vollständig oder nicht rechtzeitig erstattete Anzeige ist bußgeldbewehrt (§ 53 WaffG) und kann "
     "Zweifel an der waffenrechtlichen Zuverlässigkeit begründen."),
]
for head, txt in blocks:
    y = para(y - 4, head, size=8.5, leading=10.5, bold=True)
    y = para(y - 1, txt, size=7.8, leading=10)
y -= 10
y = para(y, "<i>Dieser Vordruck ist ein privates Hilfsmittel und ersetzt keine Rechtsberatung. Maßgeblich ist der jeweils geltende "
            "Gesetzeswortlaut (www.gesetze-im-internet.de/waffg_2002).</i>", size=7.5)
footer()
c.showPage()
c.save()
print("ok", {k: round(v) for k, v in END.items()})
