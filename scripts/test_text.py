#!/usr/bin/env python3
"""
Test za tekst fajlove
"""

import asyncio
from pathlib import Path
from ml.simple_model import SimpleModelManager

async def test_text_files():
    """Testiranje tekst fajlova"""
    print(" Testiranje Text Detection funkcionalnosti")
    print("=" * 50)
    
    manager = SimpleModelManager()
    await manager.initialize()
    
    clean_files = [
        "test_cases/clean/system_log.txt",
        "test_cases/clean/network_monitor_log.txt",
        "test_cases/clean/iot_sensor_config.txt"
    ]
    
    print("\n🔍 Testiranje CLEAN fajlova:")
    for file_path in clean_files:
        try:
            path = Path(file_path)
            if path.exists():
                features = await manager.extract_features(path)
                is_malicious, confidence = await manager.predict(features)
                status = " MALICIOZAN" if is_malicious else " BEZBEDAN"
                print(f" {path.name}: {status} (confidence: {confidence:.1%})")
            else:
                print(f" Fajl ne postoji: {file_path}")
        except Exception as e:
            print(f" Greška: {e}")
    
    malicious_files = [
        "test_cases/malicious/trojan_simulator.txt",
        "test_cases/malicious/backdoor_script.txt",
        "test_cases/malicious/test_suspicious.txt"
    ]
    
    print("\n🔍 Testiranje MALICIOUS fajlova:")
    for file_path in malicious_files:
        try:
            path = Path(file_path)
            if path.exists():
                features = await manager.extract_features(path)
                is_malicious, confidence = await manager.predict(features)
                status = " MALICIOZAN" if is_malicious else " BEZBEDAN"
                print(f" {path.name}: {status} (confidence: {confidence:.1%})")
            else:
                print(f" Fajl ne postoji: {file_path}")
        except Exception as e:
            print(f" Greška: {e}")
    
    await manager.cleanup()
    print("\n Test završen!")

if __name__ == "__main__":
    asyncio.run(test_text_files())
