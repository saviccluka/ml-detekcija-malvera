
"""
Script za pokretanje web aplikacije za IoT Malware Detection
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Proverava da li su sve potrebne biblioteke instalirane"""
    print(" Proveravanje zavisnosti...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'aiofiles',
        'tensorflow',
        'numpy',
        'pandas',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f" {package}")
        except ImportError:
            print(f" {package} - nedostaje")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n Instaliranje nedostajućih paketa: {', '.join(missing_packages)}")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f" {package} uspešno instaliran")
            except subprocess.CalledProcessError as e:
                print(f" Greška pri instaliranju {package}: {e}")
                return False
    
    return True

def create_directories():
    """Kreira potrebne direktorijume"""
    print(" Kreiranje direktorijuma...")
    
    directories = ['uploads', 'logs', 'models', 'temp']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f" {directory}/")

def start_server():
    """Pokreće web server"""
    print("\n Pokretanje web aplikacije...")
    print(" Aplikacija će biti dostupna na: http://localhost:8000")
    print(" Za zaustavljanje pritisnite Ctrl+C")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'api.simple_api:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ])
        
        if result.returncode == 0:
            print("\n Web aplikacija uspešno završena!")
        else:
            print(f"\n Web aplikacija završena sa kodom: {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n Web aplikacija zaustavljena uspešno!")
        print(" Doviđenja!")
    except Exception as e:
        print(f"\n Greška pri pokretanju servera: {e}")
        print(" Proverite da li su svi portovi slobodni")

def main():
    """Glavna funkcija"""
    print(" IoT Malware Detection - Web Aplikacija")
    print("=" * 50)
    
    print(" Korak 1/3: Provera zavisnosti...")
    if not check_dependencies():
        print(" Nije moguće pokrenuti aplikaciju zbog nedostajućih zavisnosti!")
        return
    print(" Svi zahtevi ispunjeni!")
    
    print("\n Korak 2/3: Kreiranje direktorijuma...")
    create_directories()
    print(" Direktorijumi pripremljeni!")
    
    print("\n Korak 3/3: Pokretanje servera...")
    start_server()
    
    print("\n" + "=" * 50)
    print(" IoT Malware Detection sistem je spreman!")
    print(" Implementirane funkcionalnosti:")
    print("   CNN model za detekciju malicioznih fajlova")
    print("   Image detection sa naprednim algoritmima")
    print("   Web API sa FastAPI")
    print("   Interaktivni web interfejs")
    print("=" * 50)

if __name__ == "__main__":
    main()
