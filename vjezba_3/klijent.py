
import asyncio
import aiohttp
import time

from getpass import getpass
from collections import Counter



## from requests import session

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


async def test_scenarija(session):

    print("\n--- ZADATAK 2.1 ---")

    for scenarij, pokusaj in [
        ("normalno", 1),
        ("poteskoce", 1),
        ("poteskoce", 2)
    ]:

        async with session.get(
            f"{BAZNI_URL}/kamere/PU-02/ocitanje",
            params={
                "interval": INTERVAL,
                "scenarij": scenarij,
                "pokusaj": pokusaj
            }
        ) as response:

            podaci = await response.text()

            print(f"Scenarij: {scenarij}")
            print(f"Pokušaj: {pokusaj}")
            print(f"HTTP status: {response.status}")
            print(f"Odgovor: {podaci}")
            print("--------------------")

async def dohvati_s_retry(
    session,
    kamera_id,
    scenarij="poteskoce",
    timeout=1,
    backoff=False
):

    for pokusaj in range(1, 4):

        print(f"{kamera_id}: pokušaj {pokusaj}")

        try:

            async with session.get(
                f"{BAZNI_URL}/kamere/{kamera_id}/ocitanje",
                params={
                    "interval": INTERVAL,
                    "scenarij": scenarij,
                    "pokusaj": pokusaj
                },
                timeout=aiohttp.ClientTimeout(
                    total=timeout
                )
            ) as response:

                print(f"HTTP status: {response.status}")

                if response.status == 200:
                    return await response.json()

                if response.status != 503:
                    return None

        except asyncio.TimeoutError:

            print("Istek vremena čekanja!")

        if pokusaj < 3 and backoff:

            cekanje = 0.5 * (2 ** (pokusaj - 1))

            print(f"Čekanje {cekanje} s")

            await asyncio.sleep(cekanje)

    print("Svi pokušaji neuspješni.")

    return None

async def test_160(session):

    print("\n--- ZADATAK 2.4 ---")

    async def jedan_zahtjev():

        try:
            async with session.get(
                f"{BAZNI_URL}/kamere/PU-02/ocitanje",
                params={
                    "interval": INTERVAL,
                    "scenarij": "normalno",
                    "pokusaj": 1
                }
            ) as response:

                status = response.status
                retry_after = response.headers.get("Retry-After")

                await response.read()

                return status, retry_after

        except (aiohttp.ClientError, asyncio.TimeoutError):
            return "GREŠKA", None

    rezultati = await asyncio.gather(
        *(jedan_zahtjev() for _ in range(160))
    )

    statusi = Counter(
        status for status, cekanje in rezultati
    )

    print("Ukupno zahtjeva:", len(rezultati))
    print("Broj odgovora 200:", statusi[200])
    print("Broj odgovora 429:", statusi[429])
    print("Broj mrežnih grešaka:", statusi["GREŠKA"])
    print("Svi rezultati:", dict(statusi))

    retry_after_vrijednosti = {
        cekanje
        for status, cekanje in rezultati
        if status == 429
    }

    print("Retry-After:", retry_after_vrijednosti)

async def test_160_s_retry(session):

    print("\n--- ZADATAK 2.5 ---")

    async def jedan_zahtjev():

        prvi_status = None

        for pokusaj in range(1, 4):

            try:
                async with session.get(
                    f"{BAZNI_URL}/kamere/PU-02/ocitanje",
                    params={
                        "interval": INTERVAL,
                        "scenarij": "normalno",
                        "pokusaj": pokusaj
                    }
                ) as response:

                    status = response.status

                    if prvi_status is None:
                        prvi_status = status

                    await response.read()

                    if status == 200:
                        return prvi_status, 200

                    if status != 429:
                        return prvi_status, status

                    retry_after = response.headers.get(
                        "Retry-After"
                    )

            except (aiohttp.ClientError, asyncio.TimeoutError):

                if prvi_status is None:
                    prvi_status = "GREŠKA"

                return prvi_status, "GREŠKA"

            if pokusaj < 3:

                if retry_after is None:
                    return prvi_status, 429

                try:
                    cekanje = float(retry_after)
                except ValueError:
                    return prvi_status, 429

                await asyncio.sleep(cekanje)

        return prvi_status, 429

    rezultati = await asyncio.gather(
        *(jedan_zahtjev() for _ in range(160))
    )

    prvi_statusi = Counter(
        prvi for prvi, zadnji in rezultati
    )

    zadnji_statusi = Counter(
        zadnji for prvi, zadnji in rezultati
    )

    naknadno_uspjesni = sum(
        prvi == 429 and zadnji == 200
        for prvi, zadnji in rezultati
    )

    print("Ukupno zahtjeva:", len(rezultati))
    print("Prvi pokušaji 200:", prvi_statusi[200])
    print("Prvi pokušaji 429:", prvi_statusi[429])
    print("Prvi pokušaji - greške:", prvi_statusi["GREŠKA"])

    print("Naknadno uspješni:", naknadno_uspjesni)

    print("Konačno uspješni:", zadnji_statusi[200])
    print("Konačno odbijeni:", zadnji_statusi[429])
    print("Konačne mrežne greške:", zadnji_statusi["GREŠKA"])

async def main():

    email = input("UNIPU email: ")
    lozinka = getpass("Lozinka: ")

    ## async with aiohttp.ClientSession() as session:
    async with aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(limit=160)
    ) as session:
        token = await login(session, email, lozinka)
        session.headers.update({
            "Authorization": f"Bearer {token}"
        })
        print("Uspješna prijava!")

        #kamere = await dohvati_kamere(session)

        # Izdvajanje oznaka kamera
        #kamera_ids = [
        #    kamera["kamera_id"] for kamera in kamere
        #]

        # Zadatak 1 - sekvencijalni dohvat
        #await sekvencijalno(session, kamera_ids)

        # Zadatak 1 - konkurentni dohvat, limit 2
        #await konkurentno(session, kamera_ids, 2)

        # Zadatak 1 - konkurentni dohvat, limit 6
        #await konkurentno(session, kamera_ids, 6)

        # Zadatak 2.1 - testiranje scenarija
        ## await test_scenarija(session)

        # Zadatak 2.2
        #rezultat = await dohvati_s_retry(
        #    session, "PU-02"
        #)
        #print(rezultat)

        # Zadatak 2.3
        #rezultat = await dohvati_s_retry(
        #    session, "RO-02", backoff=True
        #)
        #print(rezultat)

        # Zadatak 2.4
        #await test_160(session)

        ## Zadatak 2.5   
        await test_160_s_retry(session)

if __name__ == "__main__":
    asyncio.run(main())
