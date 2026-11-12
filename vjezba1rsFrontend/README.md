# Bistro Podaci – Vue 3 frontend (Zadatak 3)

Ovo je nadograđeni frontend iz prve vježbe, a **ne novi Vue projekt**. Prikazuje podatke restorana dobivene konkurentnim Python programom `../Vjezba3Python/pripremaPodataka.py`.

## Pokretanje

```bash
npm install
npm run dev
```

Node.js mora zadovoljavati verzije navedene u `package.json`.

Frontend na početku poziva `fetch('/podaci.json')`, odnosno putanju izvedenu iz `import.meta.env.BASE_URL`, i prikazuje tri skupine podataka:

- **Jelovnik** – naziv i cijena jela
- **Recenzije** – ime, komentar i ocjena
- **Stolovi** – oznaka i broj mjesta

Podatke ne upisuje ručno u Vue komponentu. Oni se čitaju iz `public/podaci.json`, koja je generirana Python programom i dodana u repozitorij. Gumb **Osvježi podatke** ponovno učitava JSON iz statičke datoteke. Ako se izvorni Python podaci promijene, ponovno pokreni `pripremaPodataka.py` i ponovno deployaj frontend za javni prikaz.

Dodatno se izračunavaju broj jela, prosječna ocjena, broj stolova i zbroj mjesta. Prikaz ne izmišlja status dostupnosti niti omogućuje rezervacije jer takvi podaci ne postoje u JSON datoteci.

## Kompatibilnost s prvom vježbom

Zadržana je funkcija provjere `/api/test` iz prve vježbe. Taj je test prikazan na dnu stranice **samo** ako je postavljena varijabla `VITE_API_URL`.

Primjer lokalne `.env` datoteke (po potrebi):

```text
VITE_API_URL=https://ADRESA-BACKENDA
```

Za učitavanje `podaci.json` backend i `.env` **nisu potrebni**.

## Build i Render

```bash
npm run build
```

U Render Static Site servisu postaviti Root Directory na `vjezba1rsFrontend`, Build Command na `npm ci && npm run build`, a Publish Directory na `dist`. Ako servis već postoji iz prve vježbe, ažurirati isti servis.
