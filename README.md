Simulacija sistema za detekciju malvera u IoT okruženju

Savremeni IoT ekosistemi uključuju veliki broj povezanih uređaja koji razmenjuju podatke u realnom vremenu, što predstavlja ozbiljan bezbednosni izazov. Zbog ograničenih resursa IoT uređaja, tradicionalni antivirusi nisu dovoljni, pa se u praksi sve više koriste sistemi zasnovani na mašinskom učenju i automatizovanoj analizi fajlova. U ovom projektu prikazana je simulacija kompletne platforme za otkrivanje malvera, razvijena u Python-u, sa web interfejsom i REST API-jem.

Cilj sistema je da omogući analizu različitih tipova fajlova – od tekstualnih logova, konfiguracionih fajlova i skripti, pa sve do binarnih fajlova i slika – i da na osnovu treniranog ML modela proceni potencijalnu malicioznu aktivnost. Sistem je posebno prilagođen scenarijima u kojima IoT uređaji šalju podatke centralnom serveru na analizu, pri čemu je neophodna brza i asinhona obrada.

Tehnološka osnova sistema

Sistem je razvijen u Python-u, uz korišćenje laganog web servera i minimalnog seta zavisnosti radi lakše primene u IoT okruženju. Instalacija se vrši jednostavno:

pip install -r simple_requirements.txt


Pokretanje web aplikacije:

python start_web_app.py


Nakon pokretanja, korisnički interfejs i API dostupni su na adresi:
http://localhost:8000

REST API funkcionalnosti

Platforma obezbeđuje tri ključne endpoint-rute:

POST /analyze – prima fajl i pokreće mašinski model za analizu sadržaja

GET /health – proverava status i dostupnost sistema

GET /model-info – vraća informacije o učitanom modelu, verziji i parametrima

Ovi endpointi omogućavaju integraciju sa IoT uređajima, skriptama ili drugim aplikacijama koje zahtevaju automatsku detekciju pretnji.

Podržani tipovi fajlova

Sistem je fleksibilan i omogućava analizu širokog spektra ekstenzija, među kojima su:

.txt, .log, .config, .php, .js, .py, .png, .jpg, .jpeg, .gif, .bmp, .tiff, .webp

Ovako široka podrška omogućava pokrivanje realnih bezbednosnih scenarija, posebno u okruženjima gde IoT uređaji generišu raznovrsne datoteke – od logova do slika sa senzora.

Ključne funkcionalnosti

Asinhrona obrada – omogućava analizu većeg broja fajlova bez blokiranja sistema

Real-time analiza – sistem odmah vraća rezultat detekcije

Web interfejs – jednostavan prikaz za ručno testiranje i pregled rezultata

REST API – omogućava automatizovano slanje fajlova preko skripti ili IoT uređaja

Detaljno logovanje – prati tok obrade i generiše audit tragove

Podrška za različite tipove fajlova – jednostavna integracija u heterogena okruženja
