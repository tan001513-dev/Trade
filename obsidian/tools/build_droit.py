"""Génère la toile Obsidian d'une matière de droit à partir d'un module de données.
Usage : python3 build_droit.py droit_contrats_data Contrats
"""
import importlib, os, re, sys
mod = importlib.import_module(sys.argv[1]); short = sys.argv[2]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Droit", short)
for d in ("Notions", "Arrêts", "Articles", "Cours"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
M, TAG = mod.MATIERE, mod.TAG
def fm(t, extra=""):
    return f"---\ntype: {t}\nmatiere: \"[[{M}]]\"\n{extra}tags:\n  - {TAG}\n  - {t}\n---\n"
def L(x): return f"[[{x}]]"
def write(sub, name, text):
    open(os.path.join(ROOT, sub, name + ".md"), "w").write(text)

arrets_by_cours = {}
for a, v in mod.ARRETS.items():
    for c in v[5]: arrets_by_cours.setdefault(c, []).append(a)

for n, (dfn, pts, arts, arrs, voir, cours) in mod.NOTIONS.items():
    t = fm("notion") + f"# {n}\n\n> [!abstract] Définition\n> {dfn}\n\n## À retenir\n" + "\n".join(f"- {p}" for p in pts)
    if arts: t += "\n\n## Articles\n" + " · ".join(L(a) for a in arts)
    if arrs: t += "\n\n## Arrêts\n" + "\n".join(f"- {L(a)}" for a in arrs)
    if voir: t += "\n\n## Voir aussi\n" + " · ".join(L(v) for v in voir)
    t += "\n\n## Sources\n" + " · ".join(L(c) for c in cours) + "\n"
    write("Notions", n, t)

for a, (ref, faits, sol, portee, notions, cours) in mod.ARRETS.items():
    ess = getattr(mod, "ESSENTIELS", {}).get(a)
    head = fm("arret", f"reference: \"{ref}\"\n" + ("essentiel: true\n" if ess else "")).replace("  - arret\n", "  - arret\n  - essentiel\n" if ess else "  - arret\n")
    t = head + f"# {a}\n\n*{ref}*\n\n" + (f"> [!warning] Arrêt essentiel\n> {ess}\n\n" if ess else "") + "> [!info] Faits\n> {faits}\n\n> [!success] Solution\n> {sol}\n\n**Portée.** {portee}\n\n## Notions\n" + " · ".join(L(n) for n in notions) + "\n\n## Sources\n" + " · ".join(L(c) for c in cours) + "\n"
    write("Arrêts", a, t)

# articles cités partout
text_all = "".join(open(os.path.join(ROOT, d, f)).read() for d in ("Notions", "Arrêts") for f in os.listdir(os.path.join(ROOT, d)))
cited = sorted(set(re.findall(r"\[\[(Art\. [0-9-]+)\]\]", text_all)) | set(a for v in mod.NOTIONS.values() for a in v[2]), key=lambda s: [int(x) for x in re.findall(r"\d+", s)])
for a in cited:
    label = mod.ARTICLES.get(a, "")
    notions = [n for n, v in mod.NOTIONS.items() if a in v[2]]
    t = fm("article") + f"# {a} du Code civil\n\n{label}\n\n## Notions liées\n" + (" · ".join(L(n) for n in notions) or "_Voir les rétroliens._") + "\n\n> [!tip] Texte intégral\n> [Légifrance](https://www.legifrance.gouv.fr/search/code?query=%22article%20" + a.replace("Art. ", "") + "%22%20code%20civil)\n"
    write("Articles", a, t)

for c, (titre, did, notions) in mod.COURS.items():
    t = fm("cours", f"source: \"https://docs.google.com/document/d/{did}/edit\"\n") + f"# {c} : {titre}\n\n[Ouvrir le document sur Google Drive](https://docs.google.com/document/d/{did}/edit)\n\n## Notions vues\n" + "\n".join(f"- {L(n)}" for n in notions)
    if c in arrets_by_cours: t += "\n\n## Arrêts cités\n" + "\n".join(f"- {L(a)}" for a in arrets_by_cours[c])
    write("Cours", c, t + "\n")

# carte de la matière
moc = f"---\ntype: matiere\ntags:\n  - {TAG}\n---\n# {M}\n\nRetour : [[Droit - Accueil]]\n\n## Cours et TD\n" + "\n".join(f"- {L(c)} : {v[0]}" for c, v in mod.COURS.items())
moc += "\n\n## Notions\n" + "\n".join(f"- {L(n)}" for n in mod.NOTIONS)
moc += "\n\n## Arrêts\n" + "\n".join(f"- {L(a)}" for a in mod.ARRETS) + "\n"
open(os.path.join(ROOT, M + ".md"), "w").write(moc)

# liens cassés
names = set(mod.NOTIONS) | set(mod.ARRETS) | set(cited) | set(mod.COURS) | {M, "Droit - Accueil"}
alltext = "".join(open(os.path.join(dp, f)).read() for dp, _, fs in os.walk(ROOT) for f in fs)
broken = sorted(set(re.findall(r"\[\[([^\]|#]+)", alltext)) - names)
print(f"{len(mod.NOTIONS)} notions, {len(mod.ARRETS)} arrêts, {len(cited)} articles, {len(mod.COURS)} cours")
print("liens sans note :", broken)
