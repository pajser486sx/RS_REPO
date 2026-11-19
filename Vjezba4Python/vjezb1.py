import asyncio, time, aiohttp, httpx, asyncio

# simuliramo poslužitelja
async def get_fact(session):
    URL = "https://catfact.ninja/fact"
    rezulzat = await session.get(URL)
    data = await rezulzat.json()
    print(f"Dohvatili smo činjenicu o mački: {data['fact']}")
    return data["fact"]

# simuliramo klijent koji šalje zahtjeve
# aiohttpClientSession želimo pisati tamo di je "klijent"
async def main():
    # otvaram asinkronu sesiju za slanje zahtjeva
    async with aiohttp.ClientSession() as session:
        zadaci = [asyncio.create_task(get_fact(session)) for _ in range(5)]
        rezultati = await asyncio.gather(*zadaci) # uvijek vraća listu, kada dođu svi rezultati
        # gather vraća grešku ako barem jedan od zadataka baci grešku, zato je dobro koristiti try/except blok
        print(f"Dohvatili smo ukupno 5 činjenica o mačkama.")
        print(f"Rezultati: \n{rezultati}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    asyncio.run(main())
    t2 = time.perf_counter()
    print(f"Vrijeme izvršavanja: {t2 - t1:.2f} sekundi.")