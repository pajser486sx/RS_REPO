import asyncio

async def fetch_data():
    data = [i for i in range(1, 11)]
    await asyncio.sleep(3)
    return data


async def main():
    result = await fetch_data()
    print(result)
    print("Podaci dohvaćeni.")

asyncio.run(main())