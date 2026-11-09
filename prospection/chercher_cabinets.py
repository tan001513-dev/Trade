"""Liste les cabinets comptables (code NAF 69.20Z) autour d'un point, via l'API publique
recherche-entreprises.api.gouv.fr. Usage : python3 chercher_cabinets.py LAT LON RAYON_KM sortie.json
"""
import json, math, sys, time, urllib.request, urllib.parse

lat, lon, radius, out = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
base = "https://recherche-entreprises.api.gouv.fr/near_point"
rows, page = [], 1
while True:
    q = urllib.parse.urlencode({"lat": lat, "long": lon, "radius": radius, "activite_principale": "69.20Z",
                                "per_page": 25, "page": page, "limite_matching_etablissements": 3})
    req = urllib.request.Request(f"{base}?{q}", headers={"User-Agent": "prospection-trappes/1.0"})
    for attempt in range(4):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=30)); break
        except Exception as e:
            time.sleep(2 * (attempt + 1)); err = e
    else:
        raise err
    rows += data.get("results", [])
    print("page", page, "/", data.get("total_pages"), "total", data.get("total_results"), file=sys.stderr)
    if page >= data.get("total_pages", 1): break
    page += 1; time.sleep(0.25)
json.dump(rows, open(out, "w"), ensure_ascii=False)
