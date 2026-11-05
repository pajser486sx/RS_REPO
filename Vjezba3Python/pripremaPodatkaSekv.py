import asyncio, random, time


nekiSeed = random.seed(42) 
async def dohvati_jelovnik():
    jelovnik = [{"id": 1, "naziv": "Pizza", "cijena": 8.50}, {"id": 2, "naziv": "Ragu", "cijena": 10.00}]
    print("Početak dohvačanja prvih podataka...")
    await asyncio.sleep(2)
    print("Završeno dohvačanje prvih podataka.")
    return jelovnik

async def dohvati_recenzije():
    recenzije = [{"id": 1, "ime": "Ivan", "ocjena": 5, "komentar": "Odlično!"}, {"id": 2, "ime": "Ana", "ocjena": 4, "komentar": "Dobar izbor jela."}]
    print("Početak dohvačanja drugih podataka...")
    await asyncio.sleep(2)
    print("Završeno dohvačanje drugih podataka.")
    return recenzije

async def dohvati_stolove():
    stolovi = [{"oznaka": "43", "broj_mjesta": 4}, {"oznaka": "65", "broj_mjesta": 2}]
    print("Početak dohvačanja trećih podataka...")
    await asyncio.sleep(2)
    print("Završeno dohvačanje trećih podataka.")
    return stolovi


async def main():
    t1 = time.perf_counter()
    rezultat1 = await dohvati_jelovnik()
    rezultat2 = await dohvati_recenzije()
    rezultat3 = await dohvati_stolove()

    for i in [rezultat1, rezultat2, rezultat3]:
        print(i)
    t2 = time.perf_counter()
    print(f"Vrijeme izvršavanja: {t2 - t1:.2f} sekundi")
asyncio.run(main())