"""Génère 4 factures PDF fictives pour la démo (mises en page différentes).

Usage : python3 generer_exemples.py   -> exemples/*.pdf
Toutes les entreprises sont inventées. La facture 4 contient volontairement
deux erreurs (total TTC faux, SIRET invalide) pour montrer les contrôles.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exemples")
W, H = A4


def luhn_ok(digits):
    s = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s % 10 == 0


def siret(base13):
    """SIREN (8 chiffres + clé) puis NIC (4 chiffres + clé), tous deux valides."""
    siren = next(base13[:8] + c for c in "0123456789" if luhn_ok(base13[:8] + c))
    return next(siren + base13[9:13] + c for c in "0123456789" if luhn_ok(siren + base13[9:13] + c))


def tva_intra(siren):
    return "FR%02d%s" % ((12 + 3 * (int(siren) % 97)) % 97, siren)


def eur(x):
    s = "{:,.2f}".format(x).replace(",", " ").replace(".", ",")
    return s + " €"


CLIENT = ["Garage Dupont SARL", "14 rue des Forges", "44100 Nantes"]


def facture_1(c):
    s = siret("8123456780001")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, H - 60, "FOURNITURES PRO ATLANTIQUE")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 75, "ZA de la Lande, 85000 La Roche-sur-Yon")
    c.drawString(50, H - 87, "SIRET : %s   TVA intracom. : %s" % (s, tva_intra(s[:9])))
    c.setFont("Helvetica-Bold", 13)
    c.drawString(380, H - 60, "FACTURE")
    c.setFont("Helvetica", 10)
    c.drawString(380, H - 78, "Facture n° FPA-2026-0412")
    c.drawString(380, H - 92, "Date : 03/11/2026")
    c.drawString(380, H - 106, "Échéance : 03/12/2026")
    y = H - 150
    for line in ["Client :"] + CLIENT:
        c.drawString(50, y, line); y -= 13
    lignes = [("Ramettes papier A4 (carton de 5)", 6, 24.90),
              ("Cartouches toner noir", 2, 68.00),
              ("Classeurs à levier", 20, 3.15)]
    y = H - 240
    c.setFont("Helvetica-Bold", 10)
    for x, t in [(50, "Désignation"), (330, "Qté"), (380, "P.U. HT"), (470, "Total HT")]:
        c.drawString(x, y, t)
    c.setFont("Helvetica", 10)
    ht = 0
    for d, q, pu in lignes:
        y -= 16; t = q * pu; ht += t
        c.drawString(50, y, d); c.drawString(330, y, str(q))
        c.drawString(380, y, eur(pu)); c.drawString(470, y, eur(t))
    tva = round(ht * 0.20, 2)
    y -= 40
    for lab, v in [("Total HT", ht), ("TVA 20 %", tva), ("Total TTC", ht + tva)]:
        c.drawString(380, y, lab); c.drawString(470, y, eur(v)); y -= 15
    c.setFont("Helvetica", 8)
    c.drawString(50, 60, "Pénalités de retard : 3 fois le taux d'intérêt légal. Indemnité forfaitaire de recouvrement : 40 €.")


def facture_2(c):
    s = siret("4987654320001")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, H - 60, "Transports Lemaire & Fils")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 74, "SAS au capital de 50 000 € - 2 quai Ouest, 49100 Angers")
    c.drawString(50, H - 86, "N° SIRET %s - N° TVA %s" % (s, tva_intra(s[:9])))
    c.setFont("Helvetica", 10)
    c.drawString(330, H - 140, "Destinataire")
    y = H - 154
    for line in CLIENT:
        c.drawString(330, y, line); y -= 13
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, H - 210, "FACTURE N° TL/26/1187 du 28/10/2026")
    c.setFont("Helvetica", 10)
    c.drawString(50, H - 228, "Livraison pièces détachées Nantes - Angers - Nantes, 3 tournées")
    ht = 3 * 145.00
    tva = round(ht * 0.20, 2)
    c.drawString(50, H - 260, "Montant hors taxes ....................... " + eur(ht))
    c.drawString(50, H - 275, "TVA (20 %) ............................... " + eur(tva))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, H - 295, "NET À PAYER .............................. " + eur(ht + tva))
    c.setFont("Helvetica", 10)
    c.drawString(50, H - 320, "Règlement par virement à 30 jours, soit avant le 27/11/2026.")


def facture_3(c):
    s = siret("7531598520001")
    c.setFont("Times-Bold", 18)
    c.drawString(50, H - 60, "Imprimerie du Port")
    c.setFont("Times-Roman", 10)
    c.drawString(50, H - 76, "5 place du Bouffay, 44000 Nantes")
    c.drawString(50, H - 90, "Siret %s | TVA %s" % (s, tva_intra(s[:9])))
    c.drawString(50, H - 130, "Facture : IDP-0098")
    c.drawString(50, H - 144, "Émise le 15/10/2026")
    c.drawString(50, H - 158, "À régler avant le 14/11/2026")
    c.drawString(350, H - 130, "Garage Dupont SARL")
    c.drawString(350, H - 144, "14 rue des Forges, 44100 Nantes")
    rows = [("Catalogue pièces 2027 (livre, 300 ex.)", 900.00, 5.5),
            ("Flyers promotion hiver (2 000 ex.)", 240.00, 20.0),
            ("Cartes de visite (500 ex.)", 60.00, 20.0)]
    y = H - 210
    c.setFont("Times-Bold", 10)
    c.drawString(50, y, "Article"); c.drawString(330, y, "Taux TVA"); c.drawString(430, y, "Montant HT")
    c.setFont("Times-Roman", 10)
    ht = 0; tva = 0
    for d, m, t in rows:
        y -= 15; ht += m; tva += round(m * t / 100, 2)
        c.drawString(50, y, d); c.drawString(330, y, ("%s %%" % t).replace(".", ","))
        c.drawString(430, y, eur(m))
    y -= 35
    c.drawString(330, y, "Total HT"); c.drawString(430, y, eur(ht)); y -= 14
    c.drawString(330, y, "TVA 5,5 %"); c.drawString(430, y, eur(49.50)); y -= 14
    c.drawString(330, y, "TVA 20 %"); c.drawString(430, y, eur(60.00)); y -= 14
    c.setFont("Times-Bold", 11)
    c.drawString(330, y, "Total TTC"); c.drawString(430, y, eur(ht + tva))


def facture_4(c):
    s = "41234567800013"  # SIRET volontairement invalide (clé de Luhn fausse)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, H - 60, "NETTOYAGE ÉCLAT SERVICES")
    c.setFont("Helvetica", 9)
    c.drawString(50, H - 74, "8 allée des Tilleuls, 44800 Saint-Herblain - SIRET %s" % s)
    c.setFont("Helvetica", 10)
    c.drawString(50, H - 110, "Facture N° NES-2026-233")
    c.drawString(50, H - 124, "Date de facture : 31/10/2026")
    c.drawString(350, H - 110, "Client : Garage Dupont SARL")
    c.drawString(50, H - 170, "Entretien des locaux - octobre 2026 (forfait mensuel)")
    ht = 520.00; tva = 104.00
    c.drawString(330, H - 220, "Total HT"); c.drawString(450, H - 220, eur(ht))
    c.drawString(330, H - 234, "TVA 20%"); c.drawString(450, H - 234, eur(tva))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, H - 250, "Total TTC"); c.drawString(450, H - 250, eur(634.00))  # erreur volontaire (624)


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, f in enumerate([facture_1, facture_2, facture_3, facture_4], 1):
        p = os.path.join(OUT, "facture-%d.pdf" % i)
        c = canvas.Canvas(p, pagesize=A4)
        c.setTitle("Facture exemple %d" % i)
        f(c); c.showPage(); c.save()
        print(p)


if __name__ == "__main__":
    main()
