
import asyncio
import aiohttp
import time

from getpass import getpass
from collections import Counter

BAZNI_URL = "http://10.111.1.161:8000"
INTERVAL = "jutro"


async def login(session, email, lozinka):

    podaci = {
        "unipu_email": email,
        "lozinka": lozinka
    }

    async with session.post(
        f"{BAZNI_URL}/auth/login",
        json=podaci
    ) as response:

        response.raise_for_status()

        rezultat = await response.json()

        return rezultat["access_token"]


async def dohvati_kamere(session):

    async with session.get(
        f"{BAZNI_URL}/kamere"
    ) as response:

        response.raise_for_status()

        kamere = await response.json()

        print("Dostupne kamere:")
        print(kamere)

        return kamere


async def dohvati_ocitanje(session, kamera_id):

    async with session.get(
        f"{BAZNI_URL}/kamere/{kamera_id}/ocitanje",
        params={"interval": INTERVAL}
    ) as response:

        podaci = await response.json()

        return response.status, podaci


async def sekvencijalno(session, kamere):

    pocetak = time.perf_counter()
    rezultati = []

    for kamera_id in kamere:

        rezultat = await dohvati_ocitanje(
            session, kamera_id
        )

        rezultati.append(rezultat)

    trajanje = time.perf_counter() - pocetak

    uspjesni = sum(
        status == 200 for status, podaci in rezultati
    )

    print(f"Sekvencijalno: {trajanje:.3f} s")
    print(f"Uspješna očitanja: {uspjesni}")


async def konkurentno(session, kamere, limit):

    semafor = asyncio.Semaphore(limit)

    async def ograniceni_dohvat(kamera_id):

        async with semafor:

            return await dohvati_ocitanje(
                session, kamera_id
            )

    pocetak = time.perf_counter()

    rezultati = await asyncio.gather(
        *(ograniceni_dohvat(k) for k in kamere)
    )

    trajanje = time.perf_counter() - pocetak

    uspjesni = sum(
        status == 200 for status, podaci in rezultati
    )

    print(f"Konkurentno (limit {limit}): {trajanje:.3f} s")
    print(f"Uspješna očitanja: {uspjesni}")


async def main():

    email = input("UNIPU email: ")
    lozinka = getpass("Lozinka: ")

    async with aiohttp.ClientSession() as session:

        token = await login(session, email, lozinka)

        session.headers.update({
            "Authorization": f"Bearer {token}"
        })

        print("Uspješna prijava!")

        kamere = await dohvati_kamere(session)

        # Izdvajanje oznaka kamera
        kamera_ids = [
            kamera["kamera_id"] for kamera in kamere
        ]

        # Zadatak 1 - sekvencijalni dohvat
        await sekvencijalno(session, kamera_ids)

        # Zadatak 1 - konkurentni dohvat, limit 2
        await konkurentno(session, kamera_ids, 2)

        # Zadatak 1 - konkurentni dohvat, limit 6
        await konkurentno(session, kamera_ids, 6)


if __name__ == "__main__":
    asyncio.run(main())
