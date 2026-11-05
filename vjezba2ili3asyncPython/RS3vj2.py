import asyncio, time

async def fetch_data1():
    data1 = [
        {'korisnik': 'Ivan', 'dob': 25},
        {'korisnik': 'Marko', 'dob': 30},
        {'korisnik': 'Ana', 'dob': 28}

    ]
    await asyncio.sleep(3)
    print(data1)

async def fetch_data2():
    data2 = [
        {'proizvod': 'Salama', 'cijena': 1.5},
        {'proizvod': 'Kruh', 'cijena': 0.5},
        {'proizvod': 'Mlijeko', 'cijena': 1}
    ]
    await asyncio.sleep(5)
    print(data2)

async def main():
    t1 = time.perf_counter()
    task1 = asyncio.create_task(fetch_data1())
    task2 = asyncio.create_task(fetch_data2())
    await asyncio.gather(task1, task2)
    t2 = time.perf_counter()
    print(f"Vrijeme izvršavanja: {t2 - t1:.2f} sekundi")

asyncio.run(main())
    