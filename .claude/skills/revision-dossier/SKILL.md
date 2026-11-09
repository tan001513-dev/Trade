---
name: revision-dossier
description: Révision d'un dossier comptable à partir d'un FEC par l'équipe de 6 agents (contrôleur FEC, réviseurs tiers, trésorerie, TVA, charges et produits, chef de mission). Produit une note de révision priorisée avec les questions au client. Use when the user asks to « réviser un dossier », « analyser un FEC », « lancer l'équipe de révision » or similar.
argument-hint: "[chemin du FEC] [nom du dossier]"
---

# Révision d'un dossier par l'équipe IA

Aide à la révision, pas une révision certifiée : la note finale est à valider par un expert-comptable. Ne jamais utiliser de vraies données clients sans l'accord écrit du cabinet ; préférer un FEC anonymisé.

## Étapes

1. **Calculs.** Lancer l'extraction (tous les chiffres viennent d'ici, les agents ne recalculent rien) :
   `python3 -I revision-ia/tools/fec_extract.py <FEC> revision-ia/dossiers/<nom>`
   Si un contrôle est « bloquant » dans `synthese.md`, le dire à l'utilisateur avant de continuer.
2. **Réviseurs, en parallèle.** Lancer dans un seul message les cinq agents `controleur-fec`, `reviseur-tiers`, `reviseur-tresorerie`, `reviseur-tva`, `reviseur-charges-produits`, chacun avec le chemin du dossier `revision-ia/dossiers/<nom>`.
3. **Enregistrer** chaque réponse telle quelle dans `revision-ia/dossiers/<nom>/rapports/<agent>.md`.
4. **Chef de mission.** Lancer l'agent `chef-de-mission` sur le dossier ; enregistrer sa réponse dans `revision-ia/dossiers/<nom>/note-de-revision.md`.
5. **Restituer** à l'utilisateur : le verdict, les 3 points les plus urgents et le chemin de la note. Ne pas recopier toute la note.

## Règles

- Un seul passage de l'équipe par demande ; ne pas relancer les agents en boucle.
- Ne pas versionner un dossier contenant de vraies données clients (ajouter le dossier au `.gitignore`).
