## ZADATAK 1
Sekvencijalno: 2.227 s
Uspješna očitanja: 6
Konkurentno (limit 2): 1.088 s
Uspješna očitanja: 6
Konkurentno (limit 6): 0.380 s
Uspješna očitanja: 6

## ZADATAK 2.1
Scenarij: normalno
Pokušaj: 1
HTTP status: 200
Odgovor: {"kamera_id":"PU-02","grad":"Pula","ulaz":"jug","interval":"jutro","broj_vozila":35}
<hr>
Scenarij: poteskoce
Pokušaj: 1
HTTP status: 503
Odgovor: {"detail":"Kamera je privremeno nedostupna."}
<hr>
Scenarij: poteskoce
Pokušaj: 2
HTTP status: 200
Odgovor: {"kamera_id":"PU-02","grad":"Pula","ulaz":"jug","interval":"jutro","broj_vozila":2}
<hr>

## ZADATAK 2.2
PU-02: pokušaj 1
HTTP status: 503
PU-02: pokušaj 2
HTTP status: 200
{'kamera_id': 'PU-02', 'grad': 'Pula', 'ulaz': 'jug', 'interval': 'jutro', 'broj_vozila': 83}
RO-02: pokušaj 1
Istek vremena čekanja!
Čekanje 0.5 s
RO-02: pokušaj 2
Istek vremena čekanja!
Čekanje 1.0 s
RO-02: pokušaj 3
Istek vremena čekanja!
Svi pokušaji neuspješni.
None

## ZADACI 2.3 i 2.4
Ukupno zahtjeva: 160
Broj odgovora 200: 129
Broj odgovora 429: 22
Broj mrežnih grešaka: 9
Svi rezultati: {200: 129, 429: 22, 'GREŠKA': 9}
Retry-After: {'30'}

## ZADATAK 2.5
Ukupno zahtjeva: 160
Prvi pokušaji 200: 140
Prvi pokušaji 429: 2
Prvi pokušaji - greške: 18
Naknadno uspješni: 2
Konačno uspješni: 142
Konačno odbijeni: 0
Konačne mrežne greške: 18

## ZADATAK 3:
Koliko različitih studenata može istovremeno obrađivati poslužitelj? 5 STUDENATA!