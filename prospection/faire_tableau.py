"""Construit le tableau de prospection Excel à partir de cabinets_filtres.json."""
import json, sys, urllib.parse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

src, out = sys.argv[1], sys.argv[2]
rows = json.load(open(src))
EXCL = ("COMPAGNIE REGIONALE", "CTRE DEVELOPPEMENT", "CENTRE AGRICOLE", "CENTRE DE GESTION", "ASSOCIATION")
rows = [r for r in rows if not any(x in r["nom"].upper() for x in EXCL)]

FOUND = {  # infos publiques : annuaires en ligne (téléphones, à vérifier) et sites des cabinets (emails)
    "CT EXPERT": ("01 34 62 02 42", "", ""),
    "LB CONSULTING": ("01 76 78 36 80", "", ""),
    "SOCIETE AUXILIAIRE FIDUCIAIRE (SAF)": ("01 34 82 88 89", "", ""),
    "AUDIT EXPERTISE COMPTABLE ET FISCALITE (AECF)": ("01 30 62 55 60", "cabinet-aecf.fr", "azi@cabinet-aecf.fr"),
    "CGID": ("01 81 88 98 00", "cgid.fr", "cgid@cgid.fr"),
    "AUDIS ASSOCIES": ("01 61 37 27 52", "", ""),
    "SAGES-CONSEILS EXPERTISE COMPTABLE": ("", "sages-conseils.com", "sages.conseils@yahoo.fr"),
    "LC2C": ("01 34 59 41 13", "", ""),
    "FARJOTS GOUSSEAU ET ASSOCIES": ("01 30 57 46 50", "", ""),
}

BROWN, SOFT, INK = "7A5236", "F4ECE5", "2E241D"
wb = Workbook()
ws = wb.active; ws.title = "Cabinets"
head = ["Priorité", "Km", "Cabinet", "Commune", "Adresse", "Salariés", "Dirigeant(s)", "Téléphone", "Site web",
        "Email de contact", "Rechercher", "SIREN", "Mail 1 envoyé le", "Relance 1 le", "Relance 2 le", "Réponse", "Notes"]
ws.append(head)
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=BROWN)
    c.alignment = Alignment(vertical="center", wrap_text=True)
ws.row_dimensions[1].height = 30
for i, r in enumerate(rows):
    tel, site, mail = FOUND.get(r["nom"], ("", "", ""))
    q = urllib.parse.quote_plus(f'{r["nom"]} expert comptable {r["commune"]} contact')
    ws.append(["A" if i < 30 else ("B" if i < 80 else "C"), r["km"], r["nom"], r["commune"].title(), r["adresse"],
               r["salaries"], r["dirigeants"], tel, site, mail, "Google ↗", r["siren"], None, None, None, "", ""])
    row = ws.max_row
    ws.cell(row, 11).hyperlink = f"https://www.google.com/search?q={q}"
    ws.cell(row, 11).font = Font(color=BROWN, underline="single")
    if site:
        ws.cell(row, 9).hyperlink = "https://" + site; ws.cell(row, 9).font = Font(color=BROWN, underline="single")
    for col in (13, 14, 15): ws.cell(row, col).number_format = "DD/MM/YYYY"
    if i % 2: 
        for col in range(1, len(head) + 1): ws.cell(row, col).fill = PatternFill("solid", fgColor="FBF8F5")
widths = [9, 6, 38, 22, 42, 10, 40, 16, 20, 30, 11, 12, 14, 13, 13, 18, 30]
for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
ws.freeze_panes = "D2"; ws.auto_filter.ref = ws.dimensions
dv = DataValidation(type="list", formula1='"Pas de réponse,Intéressé,Fichier reçu,Pas intéressé,Ne plus contacter"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"P2:P{ws.max_row}")
n = ws.max_row
ws.conditional_formatting.add(f"A2:Q{n}", FormulaRule(formula=['$P2="Fichier reçu"'], fill=PatternFill("solid", fgColor="E4F1E2")))
ws.conditional_formatting.add(f"A2:Q{n}", FormulaRule(formula=['OR($P2="Pas intéressé",$P2="Ne plus contacter")'], font=Font(color="A8A09A", strike=True)))

g = wb.create_sheet("Mode d'emploi")
lines = [
    ("Tableau de prospection : cabinets comptables à 20 km de Trappes", True),
    (f"{len(rows)} cabinets actifs de 3 à 49 salariés, code NAF 69.20Z (activités comptables).", False),
    ("Source : base officielle des entreprises (recherche-entreprises.api.gouv.fr), novembre 2026.", False),
    ("Exclus : entreprises qui ont refusé la prospection commerciale (opposition INSEE), grands réseaux, organismes publics.", False),
    ("", False),
    ("Comment l'utiliser", True),
    ("1. Commence par la priorité A (les 30 plus proches).", False),
    ("2. Clique « Google ↗ » : trouve le site du cabinet, puis sa page Contact. Copie l'email dans « Email de contact ».", False),
    ("   Pas d'email ? Utilise le formulaire du site, ou passe au suivant.", False),
    ("3. Envoie le mail 1, note la date. Relance 1 à J+4, relance 2 à J+10. Jamais plus de 3 messages.", False),
    ("4. Remplis « Réponse » avec la liste déroulante. « Ne plus contacter » = on ne réécrit jamais.", False),
    ("", False),
    ("À savoir", True),
    ("Téléphones : trouvés dans des annuaires en ligne, à vérifier. Emails : relevés sur le site du cabinet lui-même.", False),
    ("Écris uniquement à l'adresse professionnelle publiée par le cabinet. Chaque mail propose de refuser d'être recontacté.", False),
]
for t, b in lines:
    g.append([t]); g.cell(g.max_row, 1).font = Font(bold=b, size=13 if b else 11, color=BROWN if b else INK)
g.column_dimensions["A"].width = 120
wb.save(out)
print(len(rows), "cabinets ->", out)
