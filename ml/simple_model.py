#!/usr/bin/env python3
"""
Jednostavan Model Manager za IoT Malware Detection System
"""

import asyncio
import logging
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any

# Image processing imports
try:
    import cv2
    from PIL import Image
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

logger = logging.getLogger(__name__)

class SimpleModelManager:
    """Jednostavan upravljač modelima"""
    
    def __init__(self):
        self.is_initialized = False
        
    async def initialize(self):
        """Inicijalizacija"""
        logger.info(" Inicijalizacija SimpleModelManager-a...")
        self.is_initialized = True
        logger.info(" SimpleModelManager uspešno inicijalizovan!")
    
    async def cleanup(self):
        """Cleanup"""
        logger.info("🧹 Čišćenje SimpleModelManager-a...")
    
    async def get_model_info(self) -> dict:
        """Informacije o modelu"""
        return {
            "is_initialized": self.is_initialized,
            "model_type": "Simple",
            "image_processing_available": IMAGE_PROCESSING_AVAILABLE
        }
    
    async def predict(self, features: np.ndarray) -> Tuple[bool, float]:
        """Predikcija"""
        try:
            if not self.is_initialized:
                raise RuntimeError("Model nije inicijalizovan")
            
            # Provera da li je fajl slika
            is_image = (features[26] > 0.5)  # Image file indicator
            
            if is_image:
                logger.info(" Detektovana slika - analiziram...")
                malicious_score = await self._predict_image_malicious(features)
            else:
                logger.info(" Detektovan tekst fajl - analiziram...")
                malicious_score = await self._predict_text_malicious(features)
            
            # Dodaj veću količinu random varijabilnosti
            random_factor = (np.random.random() - 0.5) * 0.1  # Povećano sa 0.05 na 0.1
            malicious_score = max(0.0, min(1.0, malicious_score + random_factor))
            
            # Povećanje pouzdanosti na osnovu jačine signala
            if malicious_score > 0.7:
                confidence = malicious_score + 0.05  # Smanjeno sa 0.1 na 0.05
            elif malicious_score < 0.3:
                confidence = malicious_score - 0.1
            else:
                confidence = malicious_score
            
            # Dodaj dodatnu varijabilnost za confidence
            confidence_variance = (np.random.random() - 0.5) * 0.1
            confidence = max(0.1, min(1.0, confidence + confidence_variance))
            
            return malicious_score > 0.5, confidence
            
        except Exception as e:
            logger.error(f" Greška pri predikciji: {e}")
            return False, 0.1
    
    async def _predict_text_malicious(self, features: np.ndarray) -> float:
        """Predikcija za tekst fajlove - poboljšana logika"""
        malicious_score = 0.0
        
        # Maliciozni string patterni (feature[3]) - najvažniji faktor
        malicious_string_ratio = features[3]
        if malicious_string_ratio > 0.1:  # Ako ima malicioznih patterna
            malicious_score += malicious_string_ratio * 0.6
        elif malicious_string_ratio > 0.05:  # Srednji nivo
            malicious_score += malicious_string_ratio * 0.3
        
        # HTTP/URL reference (features[4], [14-17])
        http_refs = features[4] + features[14] + features[15] + features[16] + features[17]
        if http_refs > 0.2:  # Previše HTTP referenci
            malicious_score += 0.3
        elif http_refs > 0.1:  # Srednji nivo
            malicious_score += 0.15
        
        # EXE/DLL reference (features[5], [6])
        exe_dll_refs = features[5] + features[6]
        if exe_dll_refs > 0.1:  # Previše EXE/DLL referenci
            malicious_score += 0.4
        elif exe_dll_refs > 0.05:  # Srednji nivo
            malicious_score += 0.2
        
        # Sistem pozivi (features[18-21])
        system_calls = features[18] + features[19] + features[20] + features[21]
        if system_calls > 0.2:  # Previše sistemskih poziva
            malicious_score += 0.3
        elif system_calls > 0.1:  # Srednji nivo
            malicious_score += 0.15
        
        # File type (features[26-28])
        if features[26] > 0.5:  # Executable files
            malicious_score += 0.4
        elif features[27] > 0.5:  # System files
            malicious_score += 0.2
        elif features[28] > 0.5:  # Script files
            malicious_score += 0.1
        
        # Entropy (feature[8]) - visoka entropija može biti sumnjiva
        if features[8] > 0.9:  # Very high entropy
            malicious_score += 0.3
        elif features[8] > 0.7:  # High entropy
            malicious_score += 0.15
        elif features[8] < 0.1:  # Very low entropy (možda obfuscated)
            malicious_score += 0.1
        
        # Dodatni patterni (features[22-25])
        additional_patterns = features[22] + features[23] + features[24] + features[25]
        if additional_patterns > 0.2:  # Previše dodatnih patterna
            malicious_score += 0.2
        elif additional_patterns > 0.1:  # Srednji nivo
            malicious_score += 0.1
        
        # File size faktor (feature[0])
        file_size_mb = features[0]
        if file_size_mb > 10.0:  # Vrlo veliki fajlovi
            malicious_score += 0.2
        elif file_size_mb > 5.0:  # Veliki fajlovi
            malicious_score += 0.1
        elif file_size_mb < 0.001:  # Vrlo mali fajlovi (možda obfuscated)
            malicious_score += 0.05
        
        # Content length faktor (feature[1])
        content_length = features[1]
        if content_length > 1.0:  # Vrlo dugačak sadržaj
            malicious_score += 0.15
        elif content_length > 0.5:  # Dugačak sadržaj
            malicious_score += 0.05
        elif content_length < 0.01:  # Vrlo kratak sadržaj (možda obfuscated)
            malicious_score += 0.05
        
        # Dodaj veću količinu random varijabilnosti za tekst fajlove
        random_factor = (np.random.random() - 0.5) * 0.15  # Povećano sa 0.05 na 0.15
        malicious_score = max(0.0, min(1.0, malicious_score + random_factor))
        
        # Dodatna varijabilnost na osnovu sadržaja - primeni pre nego što ograniči na 1.0
        if malicious_score > 0.8:  # Ako je već visok skor
            # Dodaj varijabilnost od 0.1 do 0.2
            additional_variance = (np.random.random() - 0.5) * 0.2
            malicious_score = malicious_score + additional_variance
        
        # Ograniči na 0.0-1.0 na kraju
        malicious_score = max(0.0, min(1.0, malicious_score))
        
        return malicious_score
    
    async def _predict_image_malicious(self, features: np.ndarray) -> float:
        """Predikcija za slike - pametna logika"""
        malicious_score = 0.0
        
        # Analiza file size vs image size ratio
        file_size_mb = features[0]
        image_pixels = features[1] * 1000000  # Vraćeno u piksele
        
        if image_pixels > 0:
            expected_size = image_pixels * 3 / (1024 * 1024)  # RGB bytes to MB
            size_ratio = file_size_mb / expected_size if expected_size > 0 else 0
            
            # Ako je fajl značajno veći od očekivanog, možda sadrži skrivene podatke
            if size_ratio > 2.0:  # 2x veći od očekivanog
                malicious_score += 0.4
            elif size_ratio > 1.5:  # 1.5x veći
                malicious_score += 0.2
        
        # Analiza color variance
        color_variance = features[7] + features[8] + features[9]
        if color_variance > 0.5:  # Previše varijabilnosti
            malicious_score += 0.2
        elif color_variance < 0.01:  # Previše uniformno
            malicious_score += 0.1
        
        # Analiza edge density
        edge_density = features[10]
        if edge_density > 0.3:  # Previše ivica
            malicious_score += 0.2
        elif edge_density < 0.01:  # Premalo ivica
            malicious_score += 0.1
        
        # Analiza texture
        texture_std = features[12]
        if texture_std < 0.1:  # Previše uniformno
            malicious_score += 0.2
        elif texture_std > 0.8:  # Previše haotično
            malicious_score += 0.1
        
        # Analiza histograma
        hist_std = features[14]
        hist_peak = features[15]
        
        if hist_std < 0.1:  # Previše koncentrisano
            malicious_score += 0.2
        if hist_peak > 0.5:  # Previše pikova
            malicious_score += 0.1
        
        # Analiza Fourier spektra
        fourier_mean = features[16]
        fourier_std = features[17]
        
        if fourier_std < 0.1:  # Previše koncentrisano
            malicious_score += 0.2
        if fourier_mean > 0.8:  # Previše energije u centralnim frekvencijama
            malicious_score += 0.1
        
        # Dodaj malu količinu random varijabilnosti
        random_factor = (np.random.random() - 0.5) * 0.05
        malicious_score = max(0.0, min(1.0, malicious_score + random_factor))
        
        return malicious_score
    
    async def extract_features(self, file_path: Path) -> np.ndarray:
        """Ekstrakcija feature-a iz fajla"""
        file_ext = file_path.suffix.lower()
        is_image = file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        
        if is_image:
            return await self._extract_image_features(file_path)
        else:
            return await self._extract_text_features(file_path)
    
    async def _extract_text_features(self, file_path: Path) -> np.ndarray:
        """Ekstrakcija feature-a iz tekst fajla"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            features = np.zeros(30)
            
            # File size (MB)
            features[0] = file_path.stat().st_size / (1024 * 1024)
            
            # Content length ratio
            features[1] = len(content) / 10000  # Normalizovano
            
            # Malicious string patterns
            malicious_patterns = [
                'exec', 'eval', 'system', 'shell_exec', 'passthru',
                'base64_decode', 'gzinflate', 'str_rot13',
                'create_function', 'call_user_func', 'preg_replace'
            ]
            
            malicious_count = sum(content.lower().count(pattern) for pattern in malicious_patterns)
            features[3] = min(malicious_count / 10, 1.0)
            
            # HTTP/URL references
            features[4] = content.count('http') / 10
            features[14] = content.count('url') / 10
            features[15] = content.count('download') / 10
            features[16] = content.count('curl') / 10
            features[17] = content.count('wget') / 10
            
            # EXE/DLL references
            features[5] = content.count('.exe') / 10
            features[6] = content.count('.dll') / 10
            
            # Entropy
            features[8] = self._calculate_entropy(content)
            
            # System calls
            features[18] = content.count('system') / 10
            features[19] = content.count('exec') / 10
            features[20] = content.count('eval') / 10
            features[21] = content.count('shell') / 10
            
            # File type indicators
            file_ext = file_path.suffix.lower()
            features[26] = 1.0 if file_ext in ['.exe', '.bat', '.cmd'] else 0.0
            features[27] = 1.0 if file_ext in ['.dll', '.sys'] else 0.0
            features[28] = 1.0 if file_ext in ['.php', '.asp', '.jsp'] else 0.0
            
            # Additional patterns
            features[22] = content.count('<?php') / 10
            features[23] = content.count('javascript:') / 10
            features[24] = content.count('onclick') / 10
            features[25] = content.count('onload') / 10
            
            return features
            
        except Exception as e:
            logger.error(f"❌ Greška pri ekstrakciji text feature-a: {e}")
            return np.zeros(30)
    
    async def _extract_image_features(self, file_path: Path) -> np.ndarray:
        """Ekstrakcija feature-a iz slike"""
        try:
            if not IMAGE_PROCESSING_AVAILABLE:
                logger.warning("⚠️ Image processing nije dostupan")
                return np.zeros(30)
            
            # Učitaj sliku
            image = cv2.imread(str(file_path))
            if image is None:
                return np.zeros(30)
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            features = np.zeros(30)
            
            # File size (MB)
            features[0] = file_path.stat().st_size / (1024 * 1024)
            
            # Image dimensions
            height, width = gray.shape
            features[1] = height * width / 1000000  # Normalizovano
            
            # Color analysis
            features[4] = np.mean(image[:, :, 0]) / 255.0  # Red channel
            features[5] = np.mean(image[:, :, 1]) / 255.0  # Green channel
            features[6] = np.mean(image[:, :, 2]) / 255.0  # Blue channel
            
            # Color variance
            features[7] = np.var(image[:, :, 0]) / 10000
            features[8] = np.var(image[:, :, 1]) / 10000
            features[9] = np.var(image[:, :, 2]) / 10000
            
            # Edge density
            edges = cv2.Canny(gray, 50, 150)
            features[10] = np.sum(edges > 0) / (height * width)
            
            # Texture analysis
            features[11] = np.mean(gray) / 255.0
            features[12] = np.std(gray) / 255.0
            features[13] = np.var(gray) / 10000
            
            # Histogram analysis
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            features[14] = np.std(hist) / 1000
            features[15] = np.max(hist) / 1000
            
            # Fourier analysis
            f_transform = np.fft.fft2(gray)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.log(np.abs(f_shift) + 1)
            features[16] = np.mean(magnitude_spectrum) / 10
            features[17] = np.std(magnitude_spectrum) / 10
            
            # System calls (za slike su 0)
            features[18] = 0.0
            features[19] = 0.0
            features[20] = 0.0
            features[21] = 0.0
            
            # Image type indicators
            features[26] = 1.0  # Image file
            features[27] = 0.0  # Not system file
            features[28] = 0.0  # Not script file
            
            # Additional image features
            features[22] = 0.0  # No PHP
            features[23] = 0.0  # No JavaScript
            features[24] = 0.0  # No onclick
            features[25] = 0.0  # No onload
            
            return features
            
        except Exception as e:
            logger.error(f"❌ Greška pri ekstrakciji image feature-a: {e}")
            return np.zeros(30)
    
    def _calculate_entropy(self, text: str) -> float:
        """Kalkulacija entropije teksta"""
        if not text:
            return 0.0
        
        # Broj karaktera
        char_count = {}
        for char in text:
            char_count[char] = char_count.get(char, 0) + 1
        
        # Entropija
        entropy = 0.0
        text_len = len(text)
        for count in char_count.values():
            p = count / text_len
            if p > 0:
                entropy -= p * np.log2(p)
        
        return min(entropy / 8.0, 1.0)  # Normalizovano

# Test funkcija
if __name__ == "__main__":
    async def test():
        manager = SimpleModelManager()
        await manager.initialize()
        
        # Test sa dummy features
        features = np.zeros(30)
        features[26] = 1.0  # Image file
        is_malicious, confidence = await manager.predict(features)
        print(f"Image test - Predikcija: {is_malicious}, Pouzdanost: {confidence}")
        
        features[26] = 0.0  # Text file
        is_malicious, confidence = await manager.predict(features)
        print(f"Text test - Predikcija: {is_malicious}, Pouzdanost: {confidence}")
        
        await manager.cleanup()
    
    asyncio.run(test())
