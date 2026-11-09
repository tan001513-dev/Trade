## Constats
Sources : `tiers.csv` et `balance.csv`.
- Rapprochement : les soldes 401 (-2 058,63) et 411 (-311,50) de `tiers.csv` correspondent à `balance.csv`.
- **401EMBAL Emballages Martin** : fournisseur débiteur, solde 890,10 ; 3 lignes non lettrées, la plus ancienne du 2025-03-18 (288 jours). Anomalie.
- **411CANT Cantine Les Petits Loups** : solde nul (débit = crédit = 1 480,00) mais 3 lignes non lettrées, la plus ancienne du 2025-02-26 (308 jours).
- **411CAFE Café des Arts** : client créditeur, solde -312,00 ; 1 ligne non lettrée, 197 jours. Anomalie.
- **401LAIT Laiterie du Vexin** : solde -691,03 ; 4 lignes non lettrées, la plus ancienne de 263 jours.
- **401MOULIN Moulins de la Beauce** : solde -2 257,70, plus gros solde créditeur ; 3 lignes non lettrées, la plus ancienne de 56 jours.
- **411HOTEL Hôtel du Parc** : reliquat 0,50 ; 4 lignes non lettrées, la plus ancienne de 33 jours.
- **401SCI SCI Gambetta** et **401ENERG Énergie Plus** : soldés, sans ligne non lettrée.
- Total : 18 lignes non lettrées sur 8 tiers.

## Hypothèses
- 411CANT : factures et règlements soldés mais non lettrés, plutôt qu'un impayé réel.
- 401EMBAL : factures non saisies, paiement en double, avoir non imputé ou avance fournisseur.
- 411CAFE : acompte ou avoir client non imputé.

## Questions
- Cabinet : détail des écritures non lettrées de 401EMBAL, 411CANT et 411CAFE.
- Client : nature du solde créditeur de Café des Arts (312,00) : avoir, acompte ou erreur ?
- Client : 401SCI présente 21 600,00 en débit et en crédit, alors que le loyer 613200 vaut 18 000,00. Nature de l'écart ?

## Priorité
- **Haute** : 411CANT (308 jours), 401EMBAL (débiteur anormal, 288 jours), 411CAFE (créditeur anormal, 197 jours).
- **Moyenne** : 401LAIT, 401SCI, 401MOULIN.
- **Basse** : 411HOTEL (0,50), 401ENERG (soldé).
