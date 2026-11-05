import asyncio

async def autentifikacija(korisnik):
    baza_korisnika = [
  {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
  {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
  {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
  {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]
    if korisnik in [korisnik['korisnicko_ime'] for korisnik in baza_korisnika]:
        print(f"Korisnik {korisnik} je uspješno autentificiran.")
        return True
    else:
        print(f"Korisnik {korisnik} nije pronađen u bazi.")
        return False


async def autorizacija():