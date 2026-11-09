"""Prépare un dossier de révision à partir d'un FEC : tous les calculs sont faits ici,
les agents ne font qu'interpréter les fichiers produits.

Usage : python3 fec_extract.py <FEC> <dossier_sortie>
Sorties : synthese.md, balance.csv, tiers.csv, tresorerie.csv, tva.csv, charges_produits.csv, controles.csv
"""
import csv, os, re, statistics, sys
from collections import defaultdict
from datetime import date

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)

raw = open(src, "rb").read()
try:
    text = raw.decode("utf-8-sig")
    enc = "UTF-8"
except UnicodeDecodeError:
    text = raw.decode("cp1252")
    enc = "Windows-1252"
lines = [l for l in text.splitlines() if l.strip()]
sep = "\t" if "\t" in lines[0] else "|" if "|" in lines[0] else ";"
head = [h.strip() for h in lines[0].split(sep)]
EXPECTED = ["JournalCode", "JournalLib", "EcritureNum", "EcritureDate", "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
            "PieceRef", "PieceDate", "EcritureLib", "Debit", "Credit", "EcritureLet", "DateLet", "ValidDate", "Montantdevise", "Idevise"]
col = {h.lower(): i for i, h in enumerate(head)}
controles = []  # (gravité, contrôle, détail)
missing = [h for h in EXPECTED if h.lower() not in col]
controles.append(("bloquant" if missing else "ok", "Colonnes obligatoires", ", ".join(missing) if missing else f"{len(head)} colonnes présentes"))
controles.append(("info", "Encodage et séparateur", f"{enc}, séparateur {'tabulation' if sep == chr(9) else sep}"))


def num(s):
    s = (s or "").strip().replace(" ", "")
    if not s:
        return 0.0
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def dt(s):
    m = re.match(r"(\d{4})(\d{2})(\d{2})", (s or "").strip()) or re.match(r"(\d{4})-(\d{2})-(\d{2})", (s or "").strip())
    return date(int(m[1]), int(m[2]), int(m[3])) if m else None


rows, bad_dates, bad_amounts = [], 0, 0
for n, l in enumerate(lines[1:], start=2):
    r = l.split(sep)
    g = lambda k: (r[col[k.lower()]].strip() if k.lower() in col and col[k.lower()] < len(r) else "")
    d, de, cr = dt(g("EcritureDate")), num(g("Debit")), num(g("Credit"))
    if d is None:
        bad_dates += 1
    if de is None or cr is None:
        bad_amounts += 1
        de, cr = de or 0.0, cr or 0.0
    rows.append(dict(line=n, j=g("JournalCode"), num=g("EcritureNum"), date=d, cpt=g("CompteNum"), clib=g("CompteLib"),
                     aux=g("CompAuxNum"), auxlib=g("CompAuxLib"), piece=g("PieceRef"), lib=g("EcritureLib"),
                     de=round(de, 2), cr=round(cr, 2), let=g("EcritureLet")))
controles.append(("bloquant" if bad_dates else "ok", "Dates d'écriture lisibles", f"{bad_dates} date(s) illisible(s)"))
controles.append(("bloquant" if bad_amounts else "ok", "Montants lisibles", f"{bad_amounts} montant(s) illisible(s)"))
tot_d, tot_c = round(sum(r["de"] for r in rows), 2), round(sum(r["cr"] for r in rows), 2)
controles.append(("ok" if abs(tot_d - tot_c) < .01 else "bloquant", "Équilibre global", f"débit {tot_d:.2f} / crédit {tot_c:.2f}"))
by_num = defaultdict(list)
for r in rows:
    by_num[(r["j"], r["num"])].append(r)
unbal = [k for k, v in by_num.items() if abs(sum(x["de"] for x in v) - sum(x["cr"] for x in v)) >= .01]
controles.append(("bloquant" if unbal else "ok", "Équilibre de chaque écriture", f"{len(unbal)} écriture(s) déséquilibrée(s)" + (f" : {unbal[:5]}" if unbal else "")))
dates = [r["date"] for r in rows if r["date"]]
d0, d1 = min(dates), max(dates)
close = date(d1.year, 12, 31)
controles.append(("info", "Période couverte", f"{d0.isoformat()} au {d1.isoformat()} ; clôture retenue {close.isoformat()}"))

def w(name, header, data):
    with open(os.path.join(out, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(header)
        wr.writerows(data)

# balance
bal = defaultdict(lambda: [ "", 0.0, 0.0])
for r in rows:
    b = bal[r["cpt"]]; b[0] = b[0] or r["clib"]; b[1] += r["de"]; b[2] += r["cr"]
bal_rows = sorted([[c, v[0], round(v[1], 2), round(v[2], 2), round(v[1] - v[2], 2)] for c, v in bal.items()])
w("balance.csv", ["compte", "libelle", "debit", "credit", "solde_debiteur_moins_crediteur"], bal_rows)
sens = []
for c, lib, de, cr, s in bal_rows:
    if c.startswith("512") and s < -0.01: sens.append(f"Banque {c} créditrice ({s:.2f}) : découvert à vérifier")
    if c.startswith("47") and abs(s) >= .01: sens.append(f"Compte d'attente {c} non soldé ({s:.2f})")
    if c[:1] == "6" and s < -0.01: sens.append(f"Charge {c} {lib} créditrice ({s:.2f})")
    if c[:1] == "7" and s > 0.01: sens.append(f"Produit {c} {lib} débiteur ({s:.2f})")

# tiers
tiers = defaultdict(lambda: dict(nom="", cpt="", de=0.0, cr=0.0, ouvert=0, plus_ancien=None))
for r in rows:
    if re.match(r"^4[01]", r["cpt"]):
        t = tiers[r["aux"] or r["cpt"]]; t["nom"] = t["nom"] or r["auxlib"]; t["cpt"] = r["cpt"]; t["de"] += r["de"]; t["cr"] += r["cr"]
        if not r["let"]:
            t["ouvert"] += 1
            if r["date"] and (t["plus_ancien"] is None or r["date"] < t["plus_ancien"]): t["plus_ancien"] = r["date"]
tiers_rows = []
for k, t in sorted(tiers.items()):
    s = round(t["de"] - t["cr"], 2)
    nature = "fournisseur" if t["cpt"].startswith("40") else "client"
    anomalie = "solde anormal (fournisseur débiteur)" if nature == "fournisseur" and s > .01 else "solde anormal (client créditeur)" if nature == "client" and s < -.01 else ""
    age = (close - t["plus_ancien"]).days if t["plus_ancien"] else ""
    tiers_rows.append([k, t["nom"], nature, round(t["de"], 2), round(t["cr"], 2), s, t["ouvert"], t["plus_ancien"].isoformat() if t["plus_ancien"] else "", age, anomalie])
w("tiers.csv", ["code", "nom", "nature", "debit", "credit", "solde", "lignes_non_lettrees", "plus_ancienne_non_lettree", "age_jours", "anomalie"], tiers_rows)

# trésorerie : contreparties des écritures de banque
treso = []
for (j, n), ls in by_num.items():
    bank = [x for x in ls if x["cpt"].startswith("512")]
    if not bank: continue
    for x in ls:
        if x["cpt"].startswith("512"): continue
        kind = ("compte d'attente" if x["cpt"].startswith("47") else "charge directe sans facture" if re.match(r"^6[0-2]", x["cpt"]) and not x["cpt"].startswith("627")
                else "frais bancaires" if x["cpt"].startswith("627") else "tiers" if re.match(r"^4[01]", x["cpt"]) else "autre")
        if kind == "tiers":
            t = tiers.get(x["aux"] or x["cpt"])
            has_invoice = any(r for r in rows if (r["aux"] or r["cpt"]) == (x["aux"] or x["cpt"]) and r["j"] != j)
            if not has_invoice: kind = "tiers sans aucune facture enregistrée"
            elif x["let"]: continue
            else: kind = "règlement de tiers non lettré"
        treso.append([x["date"].isoformat() if x["date"] else "", j, n, x["cpt"], x["auxlib"] or x["clib"], x["lib"], round(x["de"] or x["cr"], 2), "sortie" if bank[0]["cr"] else "entrée", kind])
treso.sort()
w("tresorerie.csv", ["date", "journal", "ecriture", "compte_contrepartie", "tiers_ou_compte", "libelle", "montant", "sens", "nature"], treso)

# TVA par mois
m = defaultdict(lambda: dict(ca=0.0, tvac=0.0, ach=0.0, tvad=0.0))
for r in rows:
    if not r["date"]: continue
    k = r["date"].strftime("%Y-%m")
    if r["cpt"].startswith("70"): m[k]["ca"] += r["cr"] - r["de"]
    if r["cpt"].startswith("4457"): m[k]["tvac"] += r["cr"] - r["de"]
    if re.match(r"^6[0-2]", r["cpt"]) and r["j"] in ("AC", "HA"): m[k]["ach"] += r["de"] - r["cr"]
    if r["cpt"].startswith("4456"): m[k]["tvad"] += r["de"] - r["cr"]
tva_rows = [[k, round(v["ca"], 2), round(v["tvac"], 2), round(100 * v["tvac"] / v["ca"], 2) if v["ca"] else "", round(v["ach"], 2), round(v["tvad"], 2), round(100 * v["tvad"] / v["ach"], 2) if v["ach"] else ""] for k, v in sorted(m.items())]
w("tva.csv", ["mois", "ca_ht_70", "tva_collectee_4457", "taux_apparent_collecte_pct", "achats_ht_60_62_journal_achats", "tva_deductible_4456", "taux_apparent_deductible_pct"], tva_rows)

# charges et produits par compte et par mois, avec mois atypiques
cp = defaultdict(lambda: defaultdict(float)); libs = {}
for r in rows:
    if r["cpt"][:1] in "67" and r["date"]:
        cp[r["cpt"]][r["date"].strftime("%Y-%m")] += (r["de"] - r["cr"]) if r["cpt"][0] == "6" else (r["cr"] - r["de"]); libs[r["cpt"]] = libs.get(r["cpt"]) or r["clib"]
cp_rows = []
for c, months in sorted(cp.items()):
    vals = list(months.values()); tot = sum(vals); moy = statistics.mean(vals); sd = statistics.pstdev(vals) if len(vals) > 1 else 0
    atyp = [f"{k} ({v:.2f})" for k, v in sorted(months.items()) if sd and abs(v - moy) > 2 * sd]
    cp_rows.append([c, libs[c], round(tot, 2), len(vals), round(moy, 2), round(sd, 2), ", ".join(atyp)])
w("charges_produits.csv", ["compte", "libelle", "total", "nb_mois", "moyenne_mensuelle", "ecart_type", "mois_atypiques"], cp_rows)
w("controles.csv", ["gravite", "controle", "detail"], controles)

# synthèse lisible
ca = sum(v["ca"] for v in m.values()); tvac = sum(v["tvac"] for v in m.values()); tvad = sum(v["tvad"] for v in m.values())
with open(os.path.join(out, "synthese.md"), "w", encoding="utf-8") as f:
    f.write(f"# Synthèse chiffrée du FEC\n\nFichier : `{os.path.basename(src)}` · {len(rows)} lignes · {len(by_num)} écritures · {d0.isoformat()} → {d1.isoformat()}\n\n")
    f.write("## Contrôles de structure\n" + "\n".join(f"- [{g}] {c} : {d}" for g, c, d in controles) + "\n\n")
    f.write(f"## Chiffres clés\n- Chiffre d'affaires HT (70) : {ca:.2f}\n- TVA collectée (4457) : {tvac:.2f}\n- TVA déductible (4456) : {tvad:.2f}\n- TVA nette de l'exercice : {tvac - tvad:.2f} ({"dette de TVA" if tvac - tvad >= 0 else "crédit de TVA"})\n\n")
    f.write("## Soldes de sens anormal\n" + ("\n".join(f"- {s}" for s in sens) or "- aucun") + "\n\n")
    f.write("## Fichiers détaillés\nbalance.csv, tiers.csv, tresorerie.csv, tva.csv, charges_produits.csv, controles.csv (séparateur point-virgule)\n")
print(f"OK : {len(rows)} lignes, {len(by_num)} écritures, sortie dans {out}")
