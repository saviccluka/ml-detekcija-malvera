# Test Images for IoT Malware Detection System

Ovaj direktorijum sadrži test slike za testiranje image detection funkcionalnosti sistema.

## Struktura

### Clean Images (`clean/`)
- **clean_geometric.png** - Jednostavna geometrijska slika sa krugom i kvadratom
- **clean_gradient.png** - Gradient slika sa prirodnim prelazima boja
- **clean_text.png** - Slika sa običnim tekstom
- **clean_natural.png** - Slika sa prirodnim pattern-ima
- **clean_logo.png** - Logo slika sa tekstom

### Malicious Images (`malicious/`)
- **malicious_steganography.png** - Slika sa skrivenim podacima (LSB steganography)
- **malicious_encrypted.png** - Slika sa enkriptovanim sadržajem (visoka entropija)
- **malicious_obfuscated.png** - Slika sa obfuskovanim podacima i složenim pattern-ima
- **malicious_high_compression.png** - Slika sa anomalnom kompresijom
- **malicious_metadata.png** - Slika sa sumnjivim tekstom u metadata
- **malicious_hidden_code.png** - Slika sa skrivenim kodom (QR-like pattern)
- **malicious_trojan.png** - Slika sa trojan pattern-ima

### Edge Cases (`edge_cases/`)
- **edge_tiny.png** - Vrlo mala slika (10x10)
- **edge_large.png** - Vrlo velika slika (500x500)
- **edge_single_color.png** - Slika sa samo jednom bojom
- **edge_high_contrast.png** - Slika sa visokim kontrastom

## Kako koristiti

1. Pokrenite `create_test_images.py` da kreirate sve test slike
2. Upload-ujte slike kroz web interfejs na `http://localhost:8000`
3. Posmatrajte kako sistem detektuje različite tipove slika

## Očekivani rezultati

- **Clean slike** treba da budu detektovane kao bezbedne
- **Malicious slike** treba da budu detektovane kao sumnjive/maliciozne
- **Edge case slike** mogu da budu detektovane kao sumnjive zbog svojih karakteristika

## Napomene

Ove slike su kreirane za testiranje i ne sadrže stvarni maliciozni kod.
