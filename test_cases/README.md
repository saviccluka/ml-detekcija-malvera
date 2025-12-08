# 🧪 Test Cases Directory

Ovaj direktorijum sadrži test fajlove za IoT Malware Detection sistem, organizovane po kategorijama.

##  Struktura Direktorijuma

```
test_cases/
├── clean/              # Bezbedni fajlovi
├── malicious/          # Maliciozni fajlovi  
├── edge_cases/         # Granični slučajevi
└── README.md          # Ovaj fajl
```

##  Kategorije Test Fajlova

###  Clean Files (`clean/`)
Bezbedni fajlovi koji ne treba da budu detektovani kao maliciozni:

- **`test_clean.txt`** - IoT konfiguracioni fajl
- **`system_log.txt`** - Normalni sistem log fajl
- **`iot_sensor_config.txt`** - Detaljna IoT senzor konfiguracija
- **`network_monitor_log.txt`** - Mrežni monitor log fajl

###  Malicious Files (`malicious/`)
Maliciozni fajlovi koji treba da budu detektovani kao opasni:

- **`test_suspicious.txt`** - Simulacija malicioznog skripta
- **`trojan_simulator.txt`** - Simulacija trojan konja
- **`backdoor_script.txt`** - Simulacija backdoor skripta

###  Edge Cases (`edge_cases/`)
Granični slučajevi za testiranje preciznosti:

- **`false_positive_test.txt`** - Legitimni kod koji može izazvati lažne pozitive
- **`edge_case_test.txt`** - Mješoviti sadržaj za testiranje graničnih slučajeva

##  Kako da Koristite

### 1. Automatsko Testiranje
```bash
python test_detection.py
```

### 2. Manualno Testiranje
```bash
python start_web_app.py

curl -X POST -F "file=@test_cases/clean/test_clean.txt" http://localhost:8000/upload
curl -X POST -F "file=@test_cases/malicious/test_suspicious.txt" http://localhost:8000/upload
```

### 3. Web Interface
1. Otvorite http://localhost:8000
2. Upload-ujte fajlove iz test_cases direktorijuma
3. Posmatrajte rezultate detekcije

##  Očekivani Rezultati

| Fajl | Kategorija | Očekivani Rezultat | Confidence |
|------|------------|-------------------|------------|
| test_clean.txt | Clean |  BEZBEDAN | 10-30% |
| system_log.txt | Clean |  BEZBEDAN | 5-25% |
| iot_sensor_config.txt | Clean |  BEZBEDAN | 5-20% |
| network_monitor_log.txt | Clean |  BEZBEDAN | 5-25% |
| test_suspicious.txt | Malicious |  MALICIOZAN | 70-95% |
| trojan_simulator.txt | Malicious |  MALICIOZAN | 80-95% |
| backdoor_script.txt | Malicious |  MALICIOZAN | 75-90% |
| false_positive_test.txt | Edge Case |  MALICIOZAN | 60-80% |
| edge_case_test.txt | Edge Case |  BEZBEDAN | 30-50% |

## 🔧 Dodavanje Novih Test Fajlova

### Za Clean Fajlove:
1. Kreirajte fajl u `clean/` direktorijumu
2. Dodajte ga u `test_detection.py` sa `"clean"` kategorijom
3. Testirajte da li je pravilno klasifikovan

### Za Malicious Fajlove:
1. Kreirajte fajl u `malicious/` direktorijumu
2. Dodajte ga u `test_detection.py` sa `"malicious"` kategorijom
3. Testirajte da li je pravilno klasifikovan

### Za Edge Cases:
1. Kreirajte fajl u `edge_cases/` direktorijumu
2. Dodajte ga u `test_detection.py` sa odgovarajućom kategorijom
3. Testirajte granične slučajeve

##  VAŽNO

- Ovi test fajlovi su namenjeni SAMO za testiranje sistema
- Ne pokretajte ih na produkcijskim sistemima
- Malicious fajlovi sadrže simulacije, ne stvarni maliciozni kod
- Uvek testirajte u izolovanom okruženju

##  Performance Metrije

- **Accuracy**: Cilj > 90%
- **False Positive Rate**: Cilj < 5%
- **False Negative Rate**: Cilj < 10%
- **Processing Time**: < 2 sekunde po fajlu

##  Troubleshooting

### Česti Problemi:
1. **Fajl nije pronađen** - Proverite putanju u `test_detection.py`
2. **Svi fajlovi pokazuju 50% confidence** - Restartujte API server
3. **Greška pri upload-u** - Proverite da li je API server pokrenut

### Debug Komande:
```bash
curl http://localhost:8000/status

curl http://localhost:8000/model/info

tail -f iot_malware_detection.log
```
