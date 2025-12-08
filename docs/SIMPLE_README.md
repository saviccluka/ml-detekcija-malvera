# Simplified IoT Malware Detection System

Jednostavan sistem za detekciju malicioznih fajlova koristeći ML modele i IoT tehnologije.

##  Brzo pokretanje

### 1. Instalacija zavisnosti

```bash
pip install -r simple_requirements.txt
```

### 2. Pokretanje sistema

```bash
python start_web_app.py
```

### 3. Pristup API-ju

- **API Dokumentacija**: http://localhost:8000/docs
- **Glavna stranica**: http://localhost:8000
- **Status sistema**: http://localhost:8000/status

##  Dostupni endpoint-i

### GET /status
Dobijanje statusa sistema i ML modela.

### POST /upload
Upload fajla za skeniranje.

**Primer:**
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@suspicious_file.exe"
```

### GET /scan/{file_id}
Dobijanje rezultata skeniranja.

### GET /model/info
Informacije o ML modelu.

##  ML Modeli

Sistem koristi:
- **CNN Model** (TensorFlow) - glavni model za detekciju
- **Basic Model** - fallback rule-based model

##  Struktura fajlova

```
├── start_web_app.py            # Pokretanje web aplikacije
├── api/
│   └── simple_api.py          # FastAPI server
├── ml/
│   └── model_manager.py       # ML model manager
├── test_cases/                # Test fajlovi
│   ├── clean/                 # Bezbedni fajlovi
│   ├── malicious/             # Maliciozni fajlovi
│   └── edge_cases/            # Granični slučajevi
├── test_detection.py          # Test skript
├── run_tests.bat              # Batch skript za testiranje
├── simple_requirements.txt    # Zavisnosti
└── SIMPLE_README.md          # Dokumentacija
```

##  Konfiguracija

Sistem automatski kreira potrebne direktorijume:
- `models/` - ML modeli
- `uploads/` - uploadovani fajlovi
- `logs/` - log fajlovi
- `temp/` - privremeni fajlovi

##  Primer korišćenja

### Upload fajla
```python
import requests

with open('test_file.exe', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )
    result = response.json()
    print(f"File ID: {result['file_id']}")
```

### Provera statusa
```python
import requests

response = requests.get('http://localhost:8000/status')
status = response.json()
print(f"Model initialized: {status['model_initialized']}")
print(f"Model type: {status['model_type']}")
```

## 🛠️ Razvoj

### Pokretanje u development modu
```bash
uvicorn api.simple_api:app --reload --host 0.0.0.0 --port 8000
```

### Testiranje
```bash

python test_detection.py

run_tests.bat

curl -X POST -F "file=@test_cases/clean/test_clean.txt" http://localhost:8000/upload
curl -X POST -F "file=@test_cases/malicious/test_suspicious.txt" http://localhost:8000/upload
```

##  Napomene

- Sistem je pojednostavljen i uklonjeni su složeni delovi
- Zadržana je osnovna ML funkcionalnost
- API je optimizovan za jednostavno korišćenje
- Podržani su osnovni tipovi fajlova (PE, ELF, PDF, slike, arhive)

##  Bezbednost

- Fajlovi se skeniraju u izolovanom okruženju
- Maksimalna veličina fajla: 100MB
- Automatsko brisanje privremenih fajlova
