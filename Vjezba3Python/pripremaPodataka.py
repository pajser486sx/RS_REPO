import asyncio, random, time

nekiSeed = random.seed(42) 

async def dohvati_jelovnik():
    jelovnik = [{"id": 1, "naziv": "Pizza", "cijena": 8.50}, {"id": 2, "naziv": "Ragu", "cijena": 10.00}]
    print("Početak dohvačanja prvih podataka...")
    await asyncio.sleep(1)
    print("Završeno dohvačanje prvih podataka.")
    return jelovnik

async def dohvati_recenzije():
    recenzije = [{"id": 1, "ime": "Ivan", "ocjena": 5, "komentar": "Odlično!"}, {"id": 2, "ime": "Ana", "ocjena": 4, "komentar": "Dobar izbor jela."}]
    print("Početak dohvačanja drugih podataka...")
    await asyncio.sleep(3)
    print("Završeno dohvačanje drugih podataka.")
    return recenzije

async def dohvati_stolove():
    stolovi = [{"oznaka": "43", "broj_mjesta": 4}, {"oznaka": "65", "broj_mjesta": 2}]
    print("Početak dohvačanja trećih podataka...")
    await asyncio.sleep(4)
    print("Završeno dohvačanje trećih podataka.")
    return stolovi


async def main():

    t1 = time.perf_counter()
    rezultati = await asyncio.gather(
        dohvati_stolove(),
        dohvati_jelovnik(),
        dohvati_recenzije()
    )

    for i in rezultati:
        print(i)
    t2 = time.perf_counter()
    print(f"Vrijeme izvršavanja: {t2 - t1:.2f} sekundi")
asyncio.run(main())

## random.randrange(1, 4) - to smo prije koristili