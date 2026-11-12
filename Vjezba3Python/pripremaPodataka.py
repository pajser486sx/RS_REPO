import asyncio
import json
import shutil
import time
from pathlib import Path


async def dohvati_jelovnik():
    jelovnik = [
        {"id": 1, "naziv": "Pizza", "cijena": 8.50},
        {"id": 2, "naziv": "Ragu", "cijena": 10.00},
        {"id": 3, "naziv": "Lasagne", "cijena": 12.00},
        {"id": 4, "naziv": "Rižoto", "cijena": 9.50}
    ]
    print("Početak dohvaćanja jelovnika...")
    await asyncio.sleep(1)
    print("Završeno dohvaćanje jelovnika.")
    return jelovnik


async def dohvati_recenzije():
    recenzije = [
        {"id": 1, "ime": "Ivan", "ocjena": 5, "komentar": "Odlično!"},
        {"id": 2, "ime": "Ana", "ocjena": 4, "komentar": "Dobar izbor jela."},
    ]
    print("Početak dohvaćanja recenzija...")
    await asyncio.sleep(3)
    print("Završeno dohvaćanje recenzija.")
    return recenzije


async def dohvati_stolove():
    stolovi = [
        {"oznaka": "43", "broj_mjesta": 4},
        {"oznaka": "65", "broj_mjesta": 2},
    ]
    print("Početak dohvaćanja stolova...")
    await asyncio.sleep(4)
    print("Završeno dohvaćanje stolova.")
    return stolovi


async def main():
    pocetak = time.perf_counter()

    jelovnik, recenzije, stolovi = await asyncio.gather(
        dohvati_jelovnik(),
        dohvati_recenzije(),
        dohvati_stolove(),
    )

    objedinjeni_podaci = {
        "jelovnik": jelovnik,
        "recenzije": recenzije,
        "stolovi": stolovi,
    }

    datoteka = Path(__file__).resolve().parent / "podaci.json"
    with datoteka.open("w", encoding="utf-8") as f:
        json.dump(objedinjeni_podaci, f, ensure_ascii=False, indent=4)

    frontend_public = Path(__file__).resolve().parent.parent / "vjezba1rsFrontend" / "public"
    if frontend_public.is_dir():
        odrediste = frontend_public / "podaci.json"
        shutil.copyfile(datoteka, odrediste)
        print(f"JSON kopiran u: {odrediste}")
    else:
        print("Mapa frontend/public nije pronađena; podaci.json kopiraj ručno u nju.")

    trajanje = time.perf_counter() - pocetak
    print("Objedinjeni podaci:")
    print(json.dumps(objedinjeni_podaci, ensure_ascii=False, indent=2))
    print(f"Vrijeme konkurentnog izvođenja: {trajanje:.2f} sekundi")
    print(f"JSON spremljen u: {datoteka}")


if __name__ == "__main__":
    asyncio.run(main())
