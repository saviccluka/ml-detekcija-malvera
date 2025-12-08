
"""
Test script za image detection funkcionalnost sa analizom karakteristika
"""

import asyncio
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import requests
import time

sys.path.append(str(Path(__file__).parent))
from ml.simple_model import SimpleModelManager as ModelManager

async def test_image_detection():
    """Testiranje image detection funkcionalnosti"""
    print(" Testiranje Image Detection funkcionalnosti")
    print("=" * 50)
    
    model_manager = ModelManager()
    await model_manager.initialize()
    
    test_images = [
        ("test_cases/images/clean/clean_geometric.png", "clean", "Geometrijska slika"),
        ("test_cases/images/clean/clean_gradient.png", "clean", "Gradient slika"),
        ("test_cases/images/clean/clean_text.png", "clean", "Tekst slika"),
        ("test_cases/images/malicious/malicious_steganography.png", "malicious", "Steganografija"),
        ("test_cases/images/malicious/malicious_encrypted.png", "malicious", "Enkriptovani sadržaj"),
        ("test_cases/images/malicious/malicious_obfuscated.png", "malicious", "Obfuskovani podaci"),
        ("test_cases/images/malicious/malicious_metadata.png", "malicious", "Sumnjivi metadata"),
        ("test_cases/images/edge_cases/edge_tiny.png", "edge", "Vrlo mala slika"),
        ("test_cases/images/edge_cases/edge_high_contrast.png", "edge", "Visok kontrast"),
    ]
    
    correct_predictions = 0
    total_tests = len(test_images)
    
    for image_path, expected_type, description in test_images:
        print(f"\n Testiranje: {description}")
        print(f" Fajl: {image_path}")
        
        try:
            if not Path(image_path).exists():
                print(f" Fajl ne postoji: {image_path}")
                continue
            
            features = await model_manager.extract_features(Path(image_path))
            is_malicious, confidence = await model_manager.predict(features)
            
            result_text = "MALICIOZAN" if is_malicious else "BEZBEDAN"
            result_icon = "greska" if is_malicious else "uspesno"
            
            print(f" Rezultat: {result_icon} {result_text}")
            print(f" Pouzdanost: {confidence:.1%}")
            
            if expected_type == "malicious" and is_malicious:
                print(" ISPRAVNO - Maliciozna slika je detektovana kao maliciozna")
                correct_predictions += 1
            elif expected_type == "clean" and not is_malicious:
                print(" ISPRAVNO - Čista slika je detektovana kao bezbedna")
                correct_predictions += 1
            elif expected_type == "edge":
                print(" EDGE CASE - Rezultat može varirati")
                correct_predictions += 0.5  
            else:
                print(f" GREŠKA - Očekivano: {expected_type}, Dobijeno: {'malicious' if is_malicious else 'clean'}")
            
            if expected_type in ["malicious", "clean"]:
                print(f" Steganografija: {features[23]:.3f}")
                print(f" Enkriptovani sadržaj: {features[27]:.3f}")
                print(f" Obfuskovani podaci: {features[28]:.3f}")
                print(f" Anomalna kompresija: {features[29]:.3f}")
            
        except Exception as e:
            print(f" Greška pri testiranju {image_path}: {e}")
    
    print(f"\n UKUPNI REZULTATI")
    print("=" * 30)
    print(f" Ispravnih predikcija: {correct_predictions}/{total_tests}")
    print(f" Tačnost: {(correct_predictions/total_tests)*100:.1f}%")
    
    if correct_predictions >= total_tests * 0.7:
        print(" Image detection funkcionalnost radi dobro!")
    else:
        print(" Image detection funkcionalnost treba poboljšanje")

async def test_web_api():
    """Testiranje web API-ja sa slikama"""
    print("\n Testiranje Web API-ja sa slikama")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    test_images = [
        "test_cases/images/clean/clean_geometric.png",
        "test_cases/images/malicious/malicious_steganography.png"
    ]
    
    for image_path in test_images:
        if not Path(image_path).exists():
            print(f" Fajl ne postoji: {image_path}")
            continue
            
        print(f"\n Testiranje: {Path(image_path).name}")
        
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{base_url}/upload", files=files)
                
            if response.status_code == 200:
                data = response.json()
                file_id = data['file_id']
                print(f" Upload uspešan: {file_id}")
                
                time.sleep(2)
                
                result_response = requests.get(f"{base_url}/scan/{file_id}")
                if result_response.status_code == 200:
                    result = result_response.json()
                    result_text = "MALICIOZAN" if result['is_malicious'] else "BEZBEDAN"
                    result_icon = "Greska" if result['is_malicious'] else "Uspesan"
                    
                    print(f" Rezultat: {result_icon} {result_text}")
                    print(f" Pouzdanost: {result['confidence']:.1%}")
                    print(f" Model: {result['model_used']}")
                else:
                    print(f" Greška pri dobijanju rezultata: {result_response.status_code}")
            else:
                print(f" Greška pri upload-u: {response.status_code}")
                
        except Exception as e:
            print(f" Greška: {e}")

async def main():
    """Glavna funkcija"""
    print(" IoT Malware Detection - Image Detection Test")
    print("=" * 60)
    
    await test_image_detection()
    
    try:
        await test_web_api()
    except Exception as e:
        print(f" Web API test preskočen: {e}")
        print(" Pokrenite 'python start_web_app.py' u drugom terminalu za testiranje web API-ja")

if __name__ == "__main__":
    asyncio.run(main())
