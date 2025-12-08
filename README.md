

Sistem za detekciju malvera u IoT okruženju sa podrškom za analizu tekst fajlova i slika.

1. Instaliraj zavisnosti:

   pip install -r simple_requirements.txt


2. Pokreni web aplikaciju:

   python start_web_app.py

3. Otvori browser na `http://localhost:8000`




- `POST /analyze` - Analiza fajla
- `GET /health` - Status sistema
- `GET /model-info` - Informacije o modelu


Sistem podržava:
 .txt, .log, .config, .php, .js, .py
 .png, .jpg, .jpeg, .gif, .bmp, .tiff, .webp

- Asinhrona obrada
- Real-time analiza
- Web interfejs
- REST API
- Detaljno logovanje
- Podrška za različite tipove fajlova
