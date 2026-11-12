<script setup>
import { computed, onMounted, ref } from 'vue'

const podaci = ref({ jelovnik: [], recenzije: [], stolovi: [] })
const loading = ref(true)
const error = ref('')
const backendMessage = ref('')
const backendLoading = ref(false)
const backendUrl = import.meta.env.VITE_API_URL || ''

const jelovnik = computed(() => podaci.value.jelovnik)
const recenzije = computed(() => podaci.value.recenzije)
const stolovi = computed(() => podaci.value.stolovi)

const ukupnoMjesta = computed(() =>
  stolovi.value.reduce((ukupno, stol) => ukupno + Number(stol.broj_mjesta || 0), 0)
)

const prosjecnaOcjena = computed(() => {
  if (!recenzije.value.length) return '—'

  const zbroj = recenzije.value.reduce(
    (ukupno, recenzija) => ukupno + Number(recenzija.ocjena || 0),
    0
  )

  return (zbroj / recenzije.value.length).toLocaleString('hr-HR', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  })
})

const formatCijene = (cijena) =>
  new Intl.NumberFormat('hr-HR', { style: 'currency', currency: 'EUR' }).format(cijena)

const ikonaJela = (naziv) => {
  const ime = String(naziv).toLowerCase()
  if (ime.includes('pizza')) return '🍕'
  if (ime.includes('ragu')) return '🍝'
  return '🍽️'
}

const ucitajPodatke = async () => {
  loading.value = true
  error.value = ''

  try {
    // Vite poslužuje datoteke iz public/ izravno s korijenske putanje.
    const response = await fetch(`${import.meta.env.BASE_URL}podaci.json`, {
      cache: 'no-store',
    })

    if (!response.ok) throw new Error('Datoteka podaci.json nije dostupna.')

    const rezultat = await response.json()
    if (
      !Array.isArray(rezultat.jelovnik) ||
      !Array.isArray(rezultat.recenzije) ||
      !Array.isArray(rezultat.stolovi)
    ) {
      throw new Error('JSON mora sadržavati polja jelovnik, recenzije i stolovi.')
    }

    podaci.value = rezultat
  } catch (err) {
    error.value = err.message || 'Dogodila se pogreška pri učitavanju podataka.'
  } finally {
    loading.value = false
  }
}

// Zadržana funkcionalnost testiranja backenda iz prve vježbe.
const provjeriBackend = async () => {
  backendLoading.value = true
  backendMessage.value = ''

  try {
    const response = await fetch(`${backendUrl.replace(/\/$/, '')}/api/test`)
    if (!response.ok) throw new Error('Backend nije dostupan.')
    const rezultat = await response.json()
    backendMessage.value = rezultat.message
  } catch {
    backendMessage.value = 'Nije moguće uspostaviti vezu s backendom.'
  } finally {
    backendLoading.value = false
  }
}

onMounted(ucitajPodatke)
</script>

<template>
  <div class="site-shell">
    <header class="site-header page-width">
      <a class="brand" href="#pocetak" aria-label="Bistro Podaci - na početak">
        <span class="brand-mark" aria-hidden="true">✳</span>
        <span class="brand-text">bistro<span>podaci.</span></span>
      </a>

      <nav class="site-nav" aria-label="Glavna navigacija">
        <a href="#jelovnik">Jelovnik</a>
        <a href="#recenzije">Recenzije</a>
        <a href="#stolovi">Stolovi</a>
      </nav>

      <a class="header-link" href="#jelovnik">Istraži ponudu <span aria-hidden="true">↗</span></a>
    </header>

    <main id="pocetak">
      <section class="hero page-width" aria-labelledby="hero-title">
        <div class="hero-copy">
          <span class="eyebrow light"><span class="eyebrow-dot"></span> DEMO RESTORANSKOG SUSTAVA</span>
          <h1 id="hero-title">Dobar ukus.<br /><em>Dobri podaci.</em></h1>
          <p>
            Naša mala digitalna terasa. Istraži jelovnik, pročitaj dojmove gostiju
            i pogledaj stolove — sve iz jedne JSON datoteke.
          </p>
          <a class="hero-button" href="#jelovnik">Pogledaj jelovnik <span aria-hidden="true">↗</span></a>
          <div class="hero-note"><span class="note-line"></span> Python · asyncio · JSON · Vue 3</div>
        </div>

        <div class="hero-art" aria-hidden="true">
          <div class="art-circle circle-one"></div>
          <div class="art-circle circle-two"></div>
          <div class="food-plate"><span>🍕</span></div>
          <div class="art-stamp">BON<br />APPÉTIT <span>✳</span></div>
          <span class="art-spark spark-one">✦</span>
          <span class="art-spark spark-two">✳</span>
        </div>
      </section>

      <div class="page-width content-area">
        <div class="status-row">
          <div class="status-label"><span class="status-dot"></span> Pregled podataka restorana</div>
          <button class="refresh-button" type="button" @click="ucitajPodatke" :disabled="loading">
            <span aria-hidden="true">↻</span> {{ loading ? 'Učitavanje...' : 'Osvježi podatke' }}
          </button>
        </div>

        <div v-if="loading" class="notice" role="status">Učitavamo podatke iz datoteke <strong>podaci.json</strong>...</div>
        <div v-else-if="error" class="notice error-notice" role="alert">
          <strong>Podaci nisu učitani.</strong> {{ error }}
          <span>Provjeri nalazi li se datoteka u mapi <code>public/podaci.json</code>.</span>
        </div>

        <template v-else>
          <section class="stats-grid" aria-label="Statistika restorana">
            <article class="stat-card">
              <span class="stat-symbol" aria-hidden="true">◈</span>
              <span class="stat-value">{{ jelovnik.length.toString().padStart(2, '0') }}</span>
              <span class="stat-title">Jela u ponudi</span>
              <span class="stat-caption">Iz našeg jelovnika</span>
            </article>
            <article class="stat-card">
              <span class="stat-symbol" aria-hidden="true">☆</span>
              <span class="stat-value">{{ prosjecnaOcjena }}<small> / 5</small></span>
              <span class="stat-title">Prosječna ocjena</span>
              <span class="stat-caption">Na temelju {{ recenzije.length }} recenzija</span>
            </article>
            <article class="stat-card">
              <span class="stat-symbol" aria-hidden="true">▦</span>
              <span class="stat-value">{{ stolovi.length.toString().padStart(2, '0') }}</span>
              <span class="stat-title">Stolova</span>
              <span class="stat-caption">U našem prikazu</span>
            </article>
            <article class="stat-card highlight-stat">
              <span class="stat-symbol" aria-hidden="true">✳</span>
              <span class="stat-value">{{ ukupnoMjesta.toString().padStart(2, '0') }}</span>
              <span class="stat-title">Ukupno mjesta</span>
              <span class="stat-caption">Kapacitet svih stolova</span>
            </article>
          </section>

          <section id="jelovnik" class="section-block" aria-labelledby="menu-title">
            <div class="section-heading">
              <div>
                <span class="eyebrow dark">01 / NEŠTO FINO</span>
                <h2 id="menu-title">Naš <em>jelovnik.</em></h2>
                <p>Jednostavna ponuda, pregledno prikazane cijene.</p>
              </div>
              <span class="section-count">{{ jelovnik.length }} jela</span>
            </div>

            <div class="menu-grid">
              <article v-for="(jelo, index) in jelovnik" :key="jelo.id" class="menu-card">
                <div class="dish-image" :class="index % 2 === 0 ? 'dish-peach' : 'dish-sage'">
                  <span class="dish-number">BR. {{ String(index + 1).padStart(2, '0') }}</span>
                  <span class="dish-emoji" aria-hidden="true">{{ ikonaJela(jelo.naziv) }}</span>
                  <span class="dish-decoration" aria-hidden="true">✳</span>
                </div>
                <div class="dish-info">
                  <div>
                    <span class="dish-overline">JELO IZ PONUDE</span>
                    <h3>{{ jelo.naziv }}</h3>
                  </div>
                  <strong class="dish-price">{{ formatCijene(jelo.cijena) }}</strong>
                </div>
              </article>
              <p v-if="!jelovnik.length" class="empty-state">Trenutačno nema jela u JSON datoteci.</p>
            </div>
          </section>

          <section id="recenzije" class="section-block review-section" aria-labelledby="review-title">
            <div class="section-heading">
              <div>
                <span class="eyebrow dark">02 / RIJEČ GOSTIJU</span>
                <h2 id="review-title">Gosti <em>kažu.</em></h2>
                <p>Stvarne vrijednosti iz primjera dohvaćenih recenzija.</p>
              </div>
              <span class="section-count">{{ recenzije.length }} recenzija</span>
            </div>

            <div class="reviews-grid">
              <article v-for="recenzija in recenzije" :key="recenzija.id" class="review-card">
                <div class="rating" :aria-label="`Ocjena ${recenzija.ocjena} od 5`">
                  <span v-for="star in 5" :key="star" :class="{ 'star-muted': star > recenzija.ocjena }">★</span>
                </div>
                <p class="review-quote">“{{ recenzija.komentar }}”</p>
                <div class="review-author">
                  <span class="avatar">{{ String(recenzija.ime).slice(0, 1).toUpperCase() }}</span>
                  <div><strong>{{ recenzija.ime }}</strong><small>Gost restorana</small></div>
                  <span class="review-score">{{ recenzija.ocjena }}/5</span>
                </div>
              </article>
              <p v-if="!recenzije.length" class="empty-state">Trenutačno nema recenzija u JSON datoteci.</p>
            </div>
          </section>

          <section id="stolovi" class="section-block table-section" aria-labelledby="tables-title">
            <div class="section-heading">
              <div>
                <span class="eyebrow dark">03 / MJESTO ZA DRUŠTVO</span>
                <h2 id="tables-title">Naši <em>stolovi.</em></h2>
                <p>Prikaz oznake i kapaciteta svakog stola, bez izmišljanja rezervacija.</p>
              </div>
              <span class="section-count">{{ stolovi.length }} stolova</span>
            </div>

            <div class="tables-grid">
              <article v-for="stol in stolovi" :key="stol.oznaka" class="table-card">
                <div class="table-illustration" aria-hidden="true">
                  <div class="table-top"><span>✳</span></div>
                  <div class="seat-dots">
                    <span v-for="seat in Number(stol.broj_mjesta)" :key="seat" class="seat-dot"></span>
                  </div>
                </div>
                <div class="table-details">
                  <div><span class="dish-overline">RASPORED SJEDENJA</span><h3>Stol {{ stol.oznaka }}</h3></div>
                  <span class="seat-tag">{{ stol.broj_mjesta }} {{ Number(stol.broj_mjesta) === 1 ? 'mjesto' : 'mjesta' }}</span>
                </div>
              </article>
              <p v-if="!stolovi.length" class="empty-state">Trenutačno nema stolova u JSON datoteci.</p>
            </div>
          </section>
        </template>

        <aside class="tech-strip" aria-label="Način rada aplikacije">
          <div class="tech-strip-heading"><span class="eyebrow light">KAKO RADI</span><h2>Od Pythona do tvog ekrana.</h2></div>
          <div class="tech-steps">
            <div><b>01</b><span>Python <code>asyncio.gather()</code><small>Konkurentno prikuplja tri skupine.</small></span></div>
            <div><b>02</b><span><code>json.dump()</code><small>Sprema rezultat u podaci.json.</small></span></div>
            <div><b>03</b><span>Vue 3 <code>fetch()</code><small>Učitava i prikazuje sve podatke.</small></span></div>
          </div>
        </aside>

        <div v-if="backendUrl" class="backend-check">
          <span>Test povezivanja iz prve vježbe:</span>
          <button type="button" @click="provjeriBackend" :disabled="backendLoading">
            {{ backendLoading ? 'Provjeravam...' : 'Provjeri backend ↗' }}
          </button>
          <span v-if="backendMessage" role="status">{{ backendMessage }}</span>
        </div>
      </div>
    </main>

    <footer class="site-footer page-width">
      <a class="brand footer-brand" href="#pocetak"><span class="brand-mark" aria-hidden="true">✳</span><span class="brand-text">bistro<span>podaci.</span></span></a>
      <span>Vježba 3 · Raspodjeljni sustavi · Vue 3 + Python</span>
      <a href="#pocetak">Povratak na vrh ↑</a>
    </footer>
  </div>
</template>
