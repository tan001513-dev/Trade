# Dépôt Trade : consignes pour Claude

## Toile Obsidian de droit (LAS2)

Le coffre Obsidian est le dossier `obsidian/` (racine du coffre). La toile de droit est dans `obsidian/Droit/`.

**Source des cours :** dossier Google Drive « LAS2 Droit — Cours 2026-2027 » (id `1x-X174c8CyNlUK-BXlwTL0nC3dw0LfSw`), sous-dossiers :
01 Sources du droit (`16YDBTmpyPCzAA-FrpBecLVoNXixhSAtx`), 02 Obligations/contrats (`1VUVrxQGFFkQDjdSZ9kapkPGZGu7u9FwL`),
03 Droit administratif (`1MaF-dyEVWqDOkXrSh3K8atE0h9c6Wq0W`), 04 Droit commercial (`10BOeY2A8NqP6Pr0OFr9Gm5FYjLZ2AdRO`),
05 Droit public financier (`17ixpi_kJ1mb1TKz8oKMu-8u0vXwUQeIV`). Le sommaire est le doc `1h7WGcnqiihBFbuhSKmMSLfXt2Un8UcWIYg-koNIOrE0`.

**Enrichir la toile :**
1. Lister les documents des sous-dossiers (connecteur Google Drive, `parentId = '<id>'`) et comparer avec `obsidian/tools/drive_traites.txt` : traiter les documents absents ou dont la date de modification a changé.
2. Lire chaque document en entier. Ne rien inventer : chaque notion, arrêt ou article vient du cours ou du TD. Garder les « points corrigés » et « vérifié » des documents.
3. Ajouter ou compléter les données dans `obsidian/tools/droit_<matiere>_data.py` (même structure que `droit_contrats_data.py` : COURS, NOTIONS, ARRETS, ARTICLES). Une nouvelle matière = un nouveau fichier de données et un dossier `obsidian/Droit/<Matiere>/`.
4. Relier : chaque notion pointe vers ses articles, ses arrêts, les notions voisines (y compris d'autres matières quand c'est pertinent) et ses cours.
5. Reconstruire : `cd obsidian/tools && python3 build_droit.py droit_<matiere>_data <Dossier>` ; la commande doit afficher `liens sans note : []`.
6. Mettre à jour `obsidian/Droit/Droit - Accueil.md` (liste des matières), `Journal des mises à jour.md` et `drive_traites.txt`.
7. Committer et pousser sur la branche `claude/confident-albattani-me5rpf`.

**Style :** français, phrases courtes, pas de schéma « ce n'est pas X, c'est Y ». Arrêts nommés « Juridiction, date » ou par leur nom usuel avec la référence entre parenthèses.

## Workflow de développement (pack « Claude Code Pro — économie »)
- Locate relevant files using filenames, symbols, and narrow searches before reading content.
- Read only necessary files and sections; avoid generated artifacts, dependencies, lockfiles, and large logs unless required.
- Prefer the smallest safe change; preserve existing conventions and public behavior.
- Run the smallest relevant verification first; report what was and was not tested.
- Keep final responses concise: changes, verification, caveats.
- For ambiguous or broad tasks, agree on scope before extensive exploration.
- Never expose secrets or weaken security to reduce token use.
