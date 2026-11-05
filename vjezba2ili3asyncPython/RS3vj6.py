import asyncio, time

async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(2)
    print(f'Dovršio sam s {param}.')
    return f"Rezultat za {param}"

async def main():
    task1 = asyncio.create_task(fetch_data(1)) # schedule
    task2 = asyncio.create_task(fetch_data(2)) #schedule
    result1 = await task1
    print("Fetch 1 uspješno završen.")
    return [result1]


t1 = time.perf_counter()
results = asyncio.run(main()) # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")

## "Dovršio sam s 2" može se ispisati ako natjeramo da se spava 2 sekunde, to jest kolko bi bilo dovoljno da 
## se dovrši task2.. to je zato jer su oba taska već scheduleana u event loopu i ako event loop traje 2 sekunde,
## onda će se izvršiti i task2