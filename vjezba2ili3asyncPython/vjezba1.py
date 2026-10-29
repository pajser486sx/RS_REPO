import asyncio, time

async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(param)
    print(f'Dovršio sam s {param}.')
    return f"Rezultat za {param}"


async def main():
    corutine1 = fetch_data(1)
    corutine2 = fetch_data(2)

    task1 = asyncio.create_task(corutine1) # scheduling corutine1 to run in the background
    task2 = asyncio.create_task(corutine2) # scheduling corutine2 to run in the background
    
    result1 = await task1
    print("Fetch 1 uspješno završen.")
    result2 = await task2
    print("Fetch 2 uspješno završen.")
    return [result1, result2]

t1 = time.perf_counter()
results = asyncio.run(main()) # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvršavanja: {t2-t1:0.2f} sekundi.")
