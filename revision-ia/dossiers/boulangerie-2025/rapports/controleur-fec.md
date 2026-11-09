## Constats
- Aucun contrôle bloquant. Les 7 contrôles de `controles.csv` donnent 5 « ok » et 2 « info ».
- Colonnes obligatoires : 18 présentes. Dates et montants lisibles : 0 erreur (`controles.csv`, lignes 2 à 5).
- Équilibre global : débit = crédit = 144 754,71. Aucune écriture déséquilibrée (`controles.csv`, lignes 6 et 7).
- Période : 2025-01-01 au 2025-12-31, clôture retenue au 2025-12-31. Cohérent avec un exercice 2025 (`synthese.md` ; `controles.csv`).
- Volume : 322 lignes, 130 écritures.
- Le fichier source `FEC-boulangerie-2025.txt` n'est pas dans le dossier : les contrôles reposent sur la synthèse produite par l'extraction.
- Soldes de sens anormal (`synthese.md`) : compte 471000 (attente) non soldé : 539,90 ; compte 512000 (banque) créditeur : -44 477,03, « découvert à vérifier ».
- Chiffres clés (`synthese.md`) : CA HT (70) 12 658,84 ; TVA collectée (4457) 696,24 ; TVA déductible (4456) 6 314,44 ; TVA nette -5 618,20.

## Hypothèses
- Découvert : facilité de caisse ou emprunt non comptabilisés, sens de solde inversé, ou erreur de rapprochement bancaire.
- TVA déductible très supérieure à la TVA collectée : achats importants, ou TVA mal ventilée. Le CA paraît faible au regard des achats, ce qui peut signaler des ventes non enregistrées.
- Compte 471000 : opérations non imputées, à régulariser avant clôture.

## Questions
- Client : quelle est la nature du solde 512000 (découvert autorisé, prêt, erreur) ? Quel est le relevé bancaire au 31/12/2025 ?
- Cabinet : quelles opérations composent le 471000, et pourquoi n'est-il pas soldé ?
- Cabinet : la TVA nette de -5 618,20 est-elle un crédit reporté ou une demande de remboursement ? (Libellé corrigé depuis dans `synthese.md` : « crédit de TVA ».)
- Cabinet : peut-on obtenir le FEC source pour refaire ces contrôles ?

## Priorité
**Haute.** Le solde créditeur de 44 477,03 sur le compte bancaire principal doit être expliqué avant toute analyse de trésorerie. Aucun contrôle de structure n'est bloquant.
