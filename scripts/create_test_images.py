"""
Script za kreiranje test slika za IoT Malware Detection System
Kreira maliciozne i čiste test slike za testiranje image detection funkcionalnosti
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import random
import base64

def create_clean_images():
    """Kreiranje čistih test slika"""
    print(" Kreiranje čistih test slika...")
    
    clean_dir = Path("test_cases/images/clean")
    clean_dir.mkdir(parents=True, exist_ok=True)
    
    img1 = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(img1, (100, 100), 50, (0, 255, 0), -1)
    cv2.rectangle(img1, (50, 50), (150, 150), (255, 0, 0), 2)
    cv2.imwrite(str(clean_dir / "clean_geometric.png"), img1)
    
    img2 = np.zeros((200, 200, 3), dtype=np.uint8)
    for i in range(200):
        for j in range(200):
            img2[i, j] = [i, j, (i+j)//2]
    cv2.imwrite(str(clean_dir / "clean_gradient.png"), img2)
    
    img3 = np.ones((200, 400, 3), dtype=np.uint8) * 255
    cv2.putText(img3, "Clean Test Image", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, "System Log File", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
    cv2.imwrite(str(clean_dir / "clean_text.png"), img3)
    
    img4 = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
    for i in range(0, 200, 20):
        cv2.line(img4, (i, 0), (i, 200), (100, 150, 200), 1)
    cv2.imwrite(str(clean_dir / "clean_natural.png"), img4)
    
    img5 = np.ones((150, 300, 3), dtype=np.uint8) * 255
    cv2.rectangle(img5, (20, 20), (280, 130), (0, 100, 200), 3)
    cv2.putText(img5, "IoT Device", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 200), 2)
    cv2.putText(img5, "Status: OK", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 1)
    cv2.imwrite(str(clean_dir / "clean_logo.png"), img5)
    
    print(f" Kreirano {len(list(clean_dir.glob('*.png')))} čistih slika u {clean_dir}")

def create_malicious_images():
    """Kreiranje malicioznih test slika"""
    print(" Kreiranje malicioznih test slika...")
    
    malicious_dir = Path("test_cases/images/malicious")
    malicious_dir.mkdir(parents=True, exist_ok=True)
    
    img1 = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)

    secret_data = "MALWARE_PAYLOAD_HIDDEN_IN_IMAGE"
    secret_bytes = secret_data.encode()
    for i, byte in enumerate(secret_bytes):
        if i * 8 < img1.size:
            for bit in range(8):
                pixel_idx = i * 8 + bit
                if pixel_idx < img1.size:
                    flat_img = img1.flatten()
                    flat_img[pixel_idx] = (flat_img[pixel_idx] & 0xFE) | ((byte >> (7-bit)) & 1)
                    img1 = flat_img.reshape(img1.shape)
    cv2.imwrite(str(malicious_dir / "malicious_steganography.png"), img1)
    
    img2 = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
 
    for i in range(0, 200, 10):
        for j in range(0, 200, 10):
            if (i + j) % 20 == 0:
                img2[i:i+5, j:j+5] = [255, 255, 255]
            else:
                img2[i:i+5, j:j+5] = [0, 0, 0]
    cv2.imwrite(str(malicious_dir / "malicious_encrypted.png"), img2)
    
    img3 = np.zeros((200, 200, 3), dtype=np.uint8)
   
    for i in range(10):
        center = (random.randint(50, 150), random.randint(50, 150))
        radius = random.randint(10, 30)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.circle(img3, center, radius, color, -1)
        
        if i > 0:
            prev_center = (random.randint(50, 150), random.randint(50, 150))
            cv2.line(img3, center, prev_center, color, 2)
    
    cv2.putText(img3, "XOR_KEY_12345", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img3, "ENCRYPTED_DATA", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imwrite(str(malicious_dir / "malicious_obfuscated.png"), img3)
    
    img4 = np.ones((100, 100, 3), dtype=np.uint8) * 128

    for i in range(0, 100, 2):
        for j in range(0, 100, 2):
            img4[i, j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    cv2.imwrite(str(malicious_dir / "malicious_high_compression.png"), img4)
    
    img5 = np.ones((200, 300, 3), dtype=np.uint8) * 255
    cv2.putText(img5, "System Configuration", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img5, "Backdoor: ENABLED", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(img5, "Payload: READY", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(img5, "Command: EXECUTE", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.imwrite(str(malicious_dir / "malicious_metadata.png"), img5)
    
    img6 = np.zeros((200, 200, 3), dtype=np.uint8)

    for i in range(0, 200, 20):
        for j in range(0, 200, 20):
            if (i + j) % 40 == 0:
                cv2.rectangle(img6, (i, j), (i+15, j+15), (255, 255, 255), -1)
            else:
                cv2.rectangle(img6, (i, j), (i+15, j+15), (0, 0, 0), -1)
    
    cv2.putText(img6, "BASE64:", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.imwrite(str(malicious_dir / "malicious_hidden_code.png"), img6)
    
    img7 = np.ones((200, 300, 3), dtype=np.uint8) * 240

    for i in range(5):
        y = 40 + i * 30
        cv2.rectangle(img7, (20, y), (280, y+20), (200, 100, 100), -1)
        cv2.putText(img7, f"Process_{i+1}: RUNNING", (30, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    cv2.putText(img7, "TROJAN ACTIVITY", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.imwrite(str(malicious_dir / "malicious_trojan.png"), img7)
    
    print(f" Kreirano {len(list(malicious_dir.glob('*.png')))} malicioznih slika u {malicious_dir}")

def create_edge_case_images():
    """Kreiranje edge case slika"""
    print(" Kreiranje edge case slika...")
    
    edge_dir = Path("test_cases/images/edge_cases")
    edge_dir.mkdir(parents=True, exist_ok=True)
    
    img1 = np.ones((10, 10, 3), dtype=np.uint8) * 128
    cv2.imwrite(str(edge_dir / "edge_tiny.png"), img1)
    
    img2 = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)
    cv2.imwrite(str(edge_dir / "edge_large.png"), img2)
    
    img3 = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.imwrite(str(edge_dir / "edge_single_color.png"), img3)
    
    img4 = np.zeros((100, 100, 3), dtype=np.uint8)
    img4[::2, ::2] = 255
    cv2.imwrite(str(edge_dir / "edge_high_contrast.png"), img4)
    
    print(f" Kreirano {len(list(edge_dir.glob('*.png')))} edge case slika u {edge_dir}")

def create_readme():
    """Kreiranje README fajla za test slike"""
    readme_content = """# Test Images for IoT Malware Detection System

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
"""
    
    readme_path = Path("test_cases/images/README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f" Kreiran README fajl: {readme_path}")

def main():
    """Glavna funkcija"""
    print("🛡️ IoT Malware Detection - Test Image Generator")
    print("=" * 50)
    
    Path("test_cases/images").mkdir(parents=True, exist_ok=True)
    
    create_clean_images()
    create_malicious_images()
    create_edge_case_images()
    create_readme()
    
    print("\n Svi test fajlovi su uspešno kreirani!")
    print(" Lokacija: test_cases/images/")
    print(" Testiranje: http://localhost:8000")

if __name__ == "__main__":
    main()
