# -*- coding: utf-8 -*-
"""Frei erfundene Musterdaten für die Musterversion des Vordrucks."""

MAX = dict(name="Mustermann", vorname="Max", dr="", gebname="Mustermann", frname="-",
           geschl="männlich", gebdat="03.05.1971", gebort="Musterstadt", staat="deutsch",
           str="Musterweg 5", plz="12345", ort="Musterstadt")
ERIKA = dict(name="Mustermann", vorname="Erika", dr="Dr.", gebname="Gabler", frname="Gabler",
             geschl="weiblich", gebdat="12.08.1964", gebort="Berlin", staat="deutsch",
             str="Heidestraße 17", plz="51147", ort="Köln")

BEH_MAX = "Landkreis Musterkreis, Waffenbehörde"
BEH_ERIKA = "Stadt Köln, Waffenbehörde"
WBK_MAX = "MK-2008-00417"
WBK_ERIKA = "K-2012-03311"

WAFFE = ["Repetierbüchse", "J. P. Sauer & Sohn", "100 Classic", ".308 Win.",
         "S100-123456", "2019", "entfällt", "C"]
BEHOERDE_ADR_MAX = "Landkreis Musterkreis, Waffenbehörde, Amtsplatz 1, 12345 Musterstadt"
BEHOERDE_ADR_ERIKA = "Stadt Köln, Waffenbehörde, Musterallee 2, 51103 Köln"


def person(prefix, p, short=False):
    keys = ["name", "vorname", "gebdat", "gebort", "str"] if short else list(p)
    d = {f"{prefix}_{k}": p[k] for k in keys}
    if short:
        d[f"{prefix}_ort"] = f"{p['plz']} {p['ort']}"
    return d


def waffe(prefix):
    return {f"{prefix}_w1_{j + 1}": v for j, v in enumerate(WAFFE)}


SAMPLE = {}

# Seite 1: Überlassungsprotokoll
SAMPLE.update(person("S1u", MAX))
SAMPLE.update({"S1u_wbk": WBK_MAX, "S1u_beh": BEH_MAX, "S1u_nwr": "E-000000000 (Beispiel)"})
SAMPLE.update(person("S1e", ERIKA, short=True))
SAMPLE.update({
    "S1e_ausweis": "Personalausweis L01X00T47", "S1e_ausweisbeh": "Stadt Köln",
    "S1e_erl_art": "WBK (grün) + Jahresjagdschein", "S1e_erl_nr": f"{WBK_ERIKA} / JS-0456",
    "S1e_erl_beh": BEH_ERIKA, "S1e_erl_gueltig": "31.03.2027 (JS)",
    "S1_cb_wbk": True, "S1_cb_js": True,
})
SAMPLE.update(waffe("S1"))
SAMPLE.update({
    "S1_mun": ".308 Win., 40 Stück", "S1_zub": "Zielfernrohr 2,5-15x56, 1 Magazin (5 Patronen)",
    "S1_datum": "07.11.2026", "S1_zeit": "15:30", "S1_ort": "Musterweg 5, 12345 Musterstadt",
    "S1_preis": "1.200,00 EUR", "S1_art0": True,
    "S1_erk1": True, "S1_erk2": True, "S1_erk3": True, "S1_erk4": True,
    "S1_ortdatum_0": "Musterstadt, 07.11.2026", "S1_ortdatum_1": "Musterstadt, 07.11.2026",
    "S1_sig_0": "Max Mustermann", "S1_sig_1": "Erika Mustermann",
})

# Seite 2: Anzeige der Überlassung (Max)
SAMPLE.update(person("S2u", MAX))
SAMPLE.update({
    "S2_behoerde": BEHOERDE_ADR_MAX, "S2u_kontakt": "0123 456789 / max@beispiel.de",
    "S2u_erl_art": "Waffenbesitzkarte (grün)", "S2u_erl_gueltig": "unbefristet",
    "S2u_erl_nr": WBK_MAX, "S2u_erl_beh": BEH_MAX,
    "S2_datum": "07.11.2026", "S2_wbk": WBK_MAX, "S2_lfdnr": "3",
})
SAMPLE.update(waffe("S2"))
SAMPLE.update(person("S2e", ERIKA, short=True))
SAMPLE.update({
    "S2e_wbk": WBK_ERIKA, "S2e_beh": BEH_ERIKA, "S2e_sonst": "Jahresjagdschein JS-0456, Stadt Köln",
    "S2_anl1": True, "S2_anl2": True,
    "S2_ortdatum_0": "Musterstadt, 09.11.2026", "S2_sig_0": "Max Mustermann",
})

# Seite 3: Anzeige des Erwerbs (Erika)
SAMPLE.update(person("S3e", ERIKA))
SAMPLE.update({
    "S3_behoerde": BEHOERDE_ADR_ERIKA, "S3e_kontakt": "0221 987654 / erika@beispiel.de",
    "S3e_erl_art": "Waffenbesitzkarte (grün)", "S3e_erl_gueltig": "unbefristet",
    "S3e_erl_nr": WBK_ERIKA, "S3e_erl_beh": BEH_ERIKA,
    "S3e_js_nr": "JS-0456", "S3e_js_beh": BEH_ERIKA, "S3e_js_gueltig": "31.03.2027",
    "S3_datum": "07.11.2026", "S3_wbk": WBK_ERIKA, "S3_vor": "Langwaffe nach § 13 Abs. 3 WaffG (Jahresjagdschein)",
})
SAMPLE.update(waffe("S3"))
SAMPLE.update(person("S3u", MAX))
SAMPLE.update({"S3_anl1": True, "S3_ortdatum_0": "Köln, 10.11.2026", "S3_sig_0": "Erika Mustermann"})
