import asyncio, time, aiohttp, httpx, asyncio


async def get_fact(session):
    URL = "https://catfact.ninja/fact"
    rezulzat = await session.get(URL)
    data = await rezulzat.json()
    print(f"Dohvatili smo činjenicu o mački: {data['fact']}")
    return data["fact"]

async def main():
    async with aiohttp.ClientSession() as session:
        zadaci = [asyncio.create_task(get_fact(session)) for _ in range(5)]
        rezultati = await asyncio.gather(*zadaci)
        print(f"Dohvatili smo ukupno 5 činjenica o mačkama.")
        print(f"Rezultati: \n{rezultati}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    asyncio.run(main())
    t2 = time.perf_counter()
    print(f"Vrijeme izvršavanja: {t2 - t1:.2f} sekundi.")