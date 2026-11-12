## VJEŽBE IZ RASPODJELJNIH SUSTAVA
Ovdje se stavljaju praktični i određeni tekstualni sadržaji za svaku vježbu koja se radi na kolegiju Raspodjeljni sustavi (akademska godina 2026./2027.) 

### VJEŽBA 1
Link na frontend basic Vue aplikacije koja komunicira s backendom
https://vjezba1.onrender.com

### VJEŽBA 2 odnosno 3 (2.5)
Zadaci u mapi "vjezba2ili3asyncPython" 
https://github.com/pajser486sx/RS_REPO/tree/master/vjezba2ili3asyncPython

### VJEŽBA 3
Nadogradnja frontenda i povlačenje podataka iz podaci.json kojeg generira Vjezba3Python/pripremaPodataka.py
- Postojeći javni URL frontenda: https://vjezba1.onrender.com
- odgovori na pitanja iz drugog zadatka: https://github.com/pajser486sx/RS_REPO/blob/master/Vjezba3Python/odgovoriZad1.txt
<br>

Program simulira dohvaćanje triju neovisnih skupina podataka za restoran: *Jelovnik*, *Recenzije*, *Stolovi* <br><br>
Dohvaćanje je simulirano pomoću `asyncio.sleep()`. U datoteci `pripremaPodataka.py` korutine se pokreću konkurentno kroz `asyncio.gather()`, a njihovi se rezultati objedinjuju u rječnik s ključevima `jelovnik`, `recenzije` i `stolovi`. Standardni modul `json` sprema taj rječnik u UTF-8 datoteku `podaci.json` (`ensure_ascii=False`, `indent=4`). Program istu datoteku automatski kopira u `../vjezba1rsFrontend/public/podaci.json` ako ta mapa postoji.<br>
Postojeća Vue 3 aplikacija proširena je tako da putem `fetch()` učitava `/podaci.json` te prikazuje sve podatke kroz kartice za jela, recenzije i stolove. Dodatno računa prosječnu ocjenu i zbroj mjesta. Za prikaz JSON-a backend nije potreban jer ga frontend poslužuje kao statičku datoteku.

