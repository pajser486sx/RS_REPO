import asyncio
import time

async def dohvati_jelovnik():
    jelovnik = [
        {"id": 1, "naziv": "Pizza", "cijena": 8.50},
        {"id": 2, "naziv": "Ragu", "cijena": 10.00},
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

    jelovnik = await dohvati_jelovnik()
    recenzije = await dohvati_recenzije()
    stolovi = await dohvati_stolove()

    print({"jelovnik": jelovnik, "recenzije": recenzije, "stolovi": stolovi})
    print(f"Vrijeme sekvencijalnog izvođenja: {time.perf_counter() - pocetak:.2f} sekundi")


if __name__ == "__main__":
    asyncio.run(main())
