import asyncio, aiohttp, json

async def get_cat_fact(session):
    async with session.get("https://catfact.ninja/fact") as response:
        data = await response.json()
        return data["fact"]

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            # ograničavamo jedan poziv get_cat_fact na 10 sekundi
            return await asyncio.wait_for(get_cat_fact(session), timeout=10)
        except asyncio.TimeoutError:
            print("Isteklo je vrijeme za dohvat činjenice.")
            return None

print(asyncio.run(main()))