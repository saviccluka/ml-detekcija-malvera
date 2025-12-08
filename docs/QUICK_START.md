#  Brzo pokretanje - IoT Malware Detection Web App

##  Aplikacija je spremna!

Vaša web aplikacija za detekciju malicioznih fajlova je uspešno kreirana i pokrenuta.

##  Kako pristupiti

1. **Otvorite web browser** (Chrome, Firefox, Edge, itd.)
2. **Idite na adresu**: `http://localhost:8000`
3. **Videćete modernu web stranicu** sa upload funkcionalnostima

##  Kako koristiti

### 1. Proverite status
- Na vrhu stranice videćete status sistema
- Trebalo bi da piše "Status: online" i "ML Model: Aktivan"

### 2. Upload fajla
**Opcija A - Drag & Drop:**
- Otvorite File Explorer
- Pronađite bilo koji fajl
- Prevucite ga u plavu upload zonu

**Opcija B - File Picker:**
- Kliknite "Odaberite fajl" dugme
- Odaberite fajl iz dijaloga

### 3. Skeniranje
- Nakon upload-a, videćete informacije o fajlu
- Kliknite "🔍 Skeniraj fajl"
- Sačekajte da se skeniranje završi

### 4. Rezultati
- ** Zeleno**: Fajl je bezbedan
- ** Crveno**: Fajl je maliciozan
- **Progress bar**: Prikazuje pouzdanost rezultata

##  Test fajlovi

### Bezbedni fajlovi:
- `notepad.exe` (Windows Notepad)
- `calc.exe` (Windows Calculator)
- Bilo koji `.txt` fajl
- Slike (`.jpg`, `.png`)

### Za testiranje "malicioznih" fajlova:
- Fajlovi sa sumnjivim imenima
- Veliki fajlovi
- Fajlovi sa određenim hash vrednostima

##  Napredne opcije

### API dokumentacija
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Direktno testiranje API-ja
```bash

curl http://localhost:8000/status

curl -X POST -F "file=@test.txt" http://localhost:8000/upload
```

##  Zaustavljanje aplikacije

1. **U Command Prompt-u**: Pritisnite `Ctrl+C`
2. **Ili zatvorite prozor** gde je pokrenuta aplikacija

##  Ponovno pokretanje

```cmd
cd C:\Users\lukas\OneDrive\Desktop\MALWARE
python start_web_app.py
```

##  Struktura fajlova

```
MALWARE/
├── api/
│   └── simple_api.py          # FastAPI backend
├── ml/
│   └── model_manager.py       # ML model manager
├── uploads/                   # Upload-ovani fajlovi
├── models/                    # ML modeli
├── start_web_app.py          # Pokretanje aplikacije
├── WEB_APP_README.md         # Detaljna dokumentacija
└── DEMO_INSTRUCTIONS.md      # Demo instrukcije
```

##  Uspešno!

Ako vidite:
- ✅ Status: online
- ✅ ML Model: Aktivan  
- ✅ Upload funkcionalnost radi
- ✅ Skeniranje vraća rezultate
- ✅ Rezultati se prikazuju vizuelno

**Čestitamo! Vaša aplikacija radi savršeno!** 

---

**Napomena**: Ova aplikacija koristi simulaciju za ML predikcije. Za pravu detekciju malicioznih fajlova, potrebno je trenirati model na stvarnim podacima.
