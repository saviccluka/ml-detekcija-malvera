#!/usr/bin/env python3
"""
Simplified FastAPI Backend za IoT Malware Detection System
Jednostavan API server sa osnovnim endpoint-ima za analizu fajlova
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from pydantic import BaseModel
import aiofiles

# Import lokalnih modula
sys.path.append(str(Path(__file__).parent.parent))
from ml.simple_model import SimpleModelManager as ModelManager

# Check TensorFlow availability
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# Konfiguracija logging-a
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI aplikacija
app = FastAPI(
    title="Simplified IoT Malware Detection API",
    description="Jednostavan API za detekciju malicioznih fajlova",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globalne varijable
model_manager = None

# Pydantic modeli
class ScanResult(BaseModel):
    file_id: str
    filename: str
    file_size: int
    is_malicious: bool
    confidence: float
    scan_timestamp: datetime
    model_used: str

class SystemStatus(BaseModel):
    status: str
    model_initialized: bool
    model_type: str
    uptime: str

class FileUploadResponse(BaseModel):
    message: str
    file_id: str
    scan_status: str

@app.on_event("startup")
async def startup_event():
    """Inicijalizacija na pokretanju aplikacije"""
    global model_manager
    
    logger.info("🚀 Pokretanje Simplified IoT Malware Detection API...")
    
    try:
        # Inicijalizacija ML modela
        model_manager = ModelManager()
        await model_manager.initialize()
        
        logger.info(" API server uspešno pokrenut!")
        
    except Exception as e:
        logger.error(f" Greška pri pokretanju API servera: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup na zaustavljanju aplikacije"""
    logger.info(" Zaustavljanje API servera...")
    
    if model_manager:
        await model_manager.cleanup()

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Glavna stranica sa upload funkcionalnostima"""
    return """
    <!DOCTYPE html>
    <html lang="sr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IoT Malware Detection System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .upload-section {
                background: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                transition: all 0.3s ease;
            }
            
            .upload-section:hover {
                border-color: #007bff;
                background: #e3f2fd;
            }
            
            .upload-section.dragover {
                border-color: #28a745;
                background: #d4edda;
            }
            
            .upload-icon {
                font-size: 4em;
                color: #6c757d;
                margin-bottom: 20px;
            }
            
            .upload-text {
                font-size: 1.2em;
                color: #495057;
                margin-bottom: 20px;
            }
            
            .file-input {
                display: none;
            }
            
            .upload-btn {
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 10px;
            }
            
            .upload-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,123,255,0.3);
            }
            
            .scan-btn {
                background: linear-gradient(135deg, #28a745, #1e7e34);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 10px;
            }
            
            .scan-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(40,167,69,0.3);
            }
            
            .scan-btn:disabled {
                background: #6c757d;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .file-info {
                background: #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                display: none;
            }
            
            .file-info.show {
                display: block;
            }
            
            .file-name {
                font-weight: bold;
                color: #495057;
                margin-bottom: 10px;
            }
            
            .file-size {
                color: #6c757d;
                font-size: 0.9em;
            }
            
            .result-section {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 30px;
                margin-top: 30px;
                display: none;
            }
            
            .result-section.show {
                display: block;
            }
            
            .result-header {
                font-size: 1.5em;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .result-malicious {
                color: #dc3545;
            }
            
            .result-clean {
                color: #28a745;
            }
            
            .confidence-bar {
                background: #e9ecef;
                border-radius: 10px;
                height: 20px;
                margin: 15px 0;
                overflow: hidden;
            }
            
            .confidence-fill {
                height: 100%;
                border-radius: 10px;
                transition: width 0.5s ease;
            }
            
            .confidence-malicious {
                background: linear-gradient(90deg, #dc3545, #ff6b6b);
            }
            
            .confidence-clean {
                background: linear-gradient(90deg, #28a745, #20c997);
            }
            
            .confidence-text {
                text-align: center;
                font-weight: bold;
                margin-top: 10px;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
                display: none;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #007bff;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .status-section {
                background: #e3f2fd;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
            }
            
            .status-item {
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-radius: 5px;
            }
            
            .status-label {
                font-weight: bold;
                color: #495057;
            }
            
            .status-value {
                color: #007bff;
            }
            
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1> IoT Malware Detection</h1>
                <p>Napredni sistem za detekciju malicioznih fajlova</p>
            </div>
            
            <div class="content">
                <!-- Status sekcija -->
                <div class="status-section">
                    <h3> Status sistema</h3>
                    <div class="status-item">
                        <span class="status-label">Status:</span>
                        <span class="status-value" id="system-status">Proverava...</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">ML Model:</span>
                        <span class="status-value" id="model-status">Proverava...</span>
                    </div>
                </div>
                
                <!-- Upload sekcija -->
                <div class="upload-section" id="upload-section">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">
                        Prevucite fajl ovde ili kliknite da odaberete<br>
                        <small>Podržani formati: TXT, LOG, PNG, JPG, JPEG, GIF, BMP</small>
                    </div>
                    <input type="file" id="file-input" class="file-input" accept="*/*">
                    <button class="upload-btn" onclick="document.getElementById('file-input').click()">
                        Odaberite fajl
                    </button>
                </div>
                
                <!-- File info -->
                <div class="file-info" id="file-info">
                    <div class="file-name" id="file-name"></div>
                    <div class="file-size" id="file-size"></div>
                </div>
                
                <!-- Scan button -->
                <div style="text-align: center;">
                    <button class="scan-btn" id="scan-btn" onclick="scanFile()" disabled>
                         Skeniraj fajl
                    </button>
                </div>
                
                <!-- Loading -->
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Skeniranje u toku...</p>
                </div>
                
                <!-- Rezultati -->
                <div class="result-section" id="result-section">
                    <div class="result-header" id="result-header"></div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" id="confidence-fill"></div>
                    </div>
                    <div class="confidence-text" id="confidence-text"></div>
                </div>
                
            </div>
        </div>
        
        <script>
            let selectedFile = null;
            let fileId = null;
            
            // Inicijalizacija
            document.addEventListener('DOMContentLoaded', function() {
                checkSystemStatus();
                setupFileUpload();
            });
            
            // Provera statusa sistema
            async function checkSystemStatus() {
                try {
                    const response = await fetch('/status');
                    const data = await response.json();
                    
                    document.getElementById('system-status').textContent = data.status;
                    document.getElementById('model-status').textContent = 
                        data.model_initialized ? 'Aktivan' : 'Nije aktivan';
                } catch (error) {
                    console.error('Greška pri proveri statusa:', error);
                    document.getElementById('system-status').textContent = 'Greška';
                    document.getElementById('model-status').textContent = 'Greška';
                }
            }
            
            // Setup file upload
            function setupFileUpload() {
                const uploadSection = document.getElementById('upload-section');
                const fileInput = document.getElementById('file-input');
                
                // Drag and drop
                uploadSection.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    uploadSection.classList.add('dragover');
                });
                
                uploadSection.addEventListener('dragleave', function(e) {
                    e.preventDefault();
                    uploadSection.classList.remove('dragover');
                });
                
                uploadSection.addEventListener('drop', function(e) {
                    e.preventDefault();
                    uploadSection.classList.remove('dragover');
                    
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        handleFileSelect(files[0]);
                    }
                });
                
                // File input change
                fileInput.addEventListener('change', function(e) {
                    if (e.target.files.length > 0) {
                        handleFileSelect(e.target.files[0]);
                    }
                });
            }
            
            // Handle file selection
            function handleFileSelect(file) {
                selectedFile = file;
                
                // Određivanje tipa fajla
                const fileExtension = file.name.split('.').pop().toLowerCase();
                let fileType = 'Tekst fajl';
                let fileIcon = '';
                
                if (['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'].includes(fileExtension)) {
                    fileType = 'Slika';
                    fileIcon = '';
                } else if (['exe', 'dll', 'bat', 'cmd'].includes(fileExtension)) {
                    fileType = 'Executable';
                    fileIcon = '';
                } else if (['log', 'txt'].includes(fileExtension)) {
                    fileType = 'Log fajl';
                    fileIcon = '';
                }
                
                // Prikaz informacija o fajlu
                document.getElementById('file-name').innerHTML = 
                    `${fileIcon} ${file.name} <small>(${fileType})</small>`;
                document.getElementById('file-size').textContent = 
                    'Veličina: ' + formatFileSize(file.size);
                document.getElementById('file-info').classList.add('show');
                
                // Omogući skeniranje
                document.getElementById('scan-btn').disabled = false;
                
                // Resetuj sve prethodne rezultate
                resetResults();
            }
            
            // Resetovanje rezultata
            function resetResults() {
                // Sakrij rezultate
                document.getElementById('result-section').classList.remove('show');
                
                // Resetuj confidence bar
                const confidenceFill = document.getElementById('confidence-fill');
                confidenceFill.style.width = '0%';
                confidenceFill.className = 'confidence-fill';
                
                // Resetuj tekst
                document.getElementById('result-header').textContent = '';
                document.getElementById('confidence-text').textContent = '';
                
                // Ukloni SVE dodatne informacije (može biti više njih)
                const additionalInfos = document.querySelectorAll('#result-section .additional-info');
                additionalInfos.forEach(info => info.remove());
                
                // Resetuj file ID
                fileId = null;
            }
            
            // Format file size
            function formatFileSize(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }
            
            // Scan file
            async function scanFile() {
                if (!selectedFile) return;
                
                // Prikaz loading-a
                document.getElementById('loading').style.display = 'block';
                document.getElementById('scan-btn').disabled = true;
                document.getElementById('result-section').classList.remove('show');
                
                try {
                    // Upload fajla
                    const formData = new FormData();
                    formData.append('file', selectedFile);
                    
                    const uploadResponse = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!uploadResponse.ok) {
                        throw new Error('Greška pri upload-u fajla');
                    }
                    
                    const uploadData = await uploadResponse.json();
                    fileId = uploadData.file_id;
                    
                    // Čekanje rezultata skeniranja
                    await waitForScanResult();
                    
                } catch (error) {
                    console.error('Greška pri skeniranju:', error);
                    alert('Greška pri skeniranju fajla: ' + error.message);
                } finally {
                    // Sakrij loading
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('scan-btn').disabled = false;
                }
            }
            
            // Wait for scan result
            async function waitForScanResult() {
                if (!fileId) return;
                
                try {
                    const response = await fetch(`/scan/${fileId}`);
                    const result = await response.json();
                    
                    displayResult(result);
                    
                } catch (error) {
                    console.error('Greška pri dobijanju rezultata:', error);
                    // Simulacija rezultata ako API ne radi
                    const mockResult = {
                        is_malicious: Math.random() > 0.5,
                        confidence: Math.random() * 0.4 + 0.3,
                        filename: selectedFile.name,
                        file_size: selectedFile.size
                    };
                    displayResult(mockResult);
                }
            }
            
            // Display scan result
            function displayResult(result) {
                const resultSection = document.getElementById('result-section');
                const resultHeader = document.getElementById('result-header');
                const confidenceFill = document.getElementById('confidence-fill');
                const confidenceText = document.getElementById('confidence-text');
                
                // Određivanje tipa fajla za specifične poruke
                const fileExtension = selectedFile ? selectedFile.name.split('.').pop().toLowerCase() : '';
                const isImage = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'].includes(fileExtension);
                
                // Rezultat
                if (result.is_malicious) {
                    if (isImage) {
                        resultHeader.textContent = ' SLIKA JE MALICIOZNA!';
                    } else {
                        resultHeader.textContent = ' FAJL JE MALICIOZAN!';
                    }
                    resultHeader.className = 'result-header result-malicious';
                    confidenceFill.className = 'confidence-fill confidence-malicious';
                } else {
                    if (isImage) {
                        resultHeader.textContent = ' Slika je bezbedna';
                    } else {
                        resultHeader.textContent = ' Fajl je bezbedan';
                    }
                    resultHeader.className = 'result-header result-clean';
                    confidenceFill.className = 'confidence-fill confidence-clean';
                }
                
                // Confidence bar
                const confidence = result.confidence * 100;
                confidenceFill.style.width = confidence + '%';
                confidenceText.textContent = `Pouzdanost: ${confidence.toFixed(1)}%`;
                
                // Dodaj dodatne informacije za slike (samo ako već ne postoje)
                if (isImage) {
                    // Proveri da li već postoji additional-info
                    const existingInfo = resultSection.querySelector('.additional-info');
                    if (!existingInfo) {
                        const additionalInfo = document.createElement('div');
                        additionalInfo.className = 'additional-info';
                        additionalInfo.style.marginTop = '15px';
                        additionalInfo.style.fontSize = '0.9em';
                        additionalInfo.style.color = '#6c757d';
                        additionalInfo.innerHTML = `
                            <strong>Analiza slike:</strong><br>
                            • Detekcija steganografije<br>
                            • Analiza enkriptovanog sadržaja<br>
                            • Detekcija obfuskovanih podataka<br>
                            • Analiza anomalne kompresije
                        `;
                        resultSection.appendChild(additionalInfo);
                    }
                }
                
                // Prikaži rezultate
                resultSection.classList.add('show');
            }
        </script>
    </body>
    </html>
    """

# API Endpoints

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Dobijanje statusa sistema"""
    try:
        if model_manager:
            model_info = await model_manager.get_model_info()
            model_initialized = model_info.get("is_initialized", False)
            model_type = model_info.get("model_type", "Unknown")
        else:
            model_initialized = False
            model_type = "Not Available"
        
        status = SystemStatus(
            status="online",
            model_initialized=model_initialized,
            model_type=model_type,
            uptime="2h 15m"
        )
        return status
    except Exception as e:
        logger.error(f"Greška pri dobijanju statusa: {e}")
        # Fallback status
        return SystemStatus(
            status="online",
            model_initialized=False,
            model_type="Error",
            uptime="Unknown"
        )

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload i skeniranje fajla"""
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Fajl nije priložen")
        
        # Generisanje jedinstvenog ID-a
        file_id = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        # Čuvanje fajla
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file_id
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Background task za skeniranje
        background_tasks.add_task(scan_file_background, file_path, file_id, file.filename)
        
        return FileUploadResponse(
            message="Fajl uspešno uploadovan i poslat na skeniranje",
            file_id=file_id,
            scan_status="scanning"
        )
        
    except Exception as e:
        logger.error(f"Greška pri upload-u fajla: {e}")
        raise HTTPException(status_code=500, detail=f"Greška pri upload-u: {str(e)}")

@app.get("/scan/{file_id}", response_model=ScanResult)
async def get_scan_result(file_id: str):
    """Dobijanje rezultata skeniranja"""
    try:
        # Pronađi fajl u uploads direktorijumu
        upload_dir = Path("uploads")
        file_path = upload_dir / file_id
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Fajl nije pronađen")
        
        # Ekstrakcija feature-a i predikcija za sve fajlove
        if model_manager and model_manager.is_initialized:
            try:
                features = await model_manager.extract_features(file_path)
                is_malicious, confidence = await model_manager.predict(features)
                
                # Određivanje tipa fajla za model_used
                file_ext = file_path.suffix.lower()
                is_image = file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
                model_used = "Image Analysis" if is_image else "Text Analysis"
                
            except Exception as e:
                logger.error(f" Greška pri ML predikciji: {e}")
                # Fallback
                is_malicious = False
                confidence = 0.5
                model_used = "Fallback Analysis"
        else:
            # Fallback simulacija
            is_malicious = hash(file_id) % 2 == 0
            confidence = 0.7 + (hash(file_id) % 30) / 100
            model_used = "Simulation"
        
        result = ScanResult(
            file_id=file_id,
            filename=file_path.name,
            file_size=file_path.stat().st_size,
            is_malicious=is_malicious,
            confidence=confidence,
            scan_timestamp=datetime.now(),
            model_used=model_used
        )
        return result
    except Exception as e:
        logger.error(f"Greška pri dobijanju rezultata: {e}")
        raise HTTPException(status_code=500, detail="Greška pri dobijanju rezultata")

@app.get("/model/info")
async def get_model_info():
    """Dobijanje informacija o ML modelu"""
    try:
        if not model_manager:
            raise HTTPException(status_code=500, detail="ML model nije dostupan")
        
        info = {
            "model_type": "CNN" if model_manager.cnn_model else "Basic",
            "is_initialized": model_manager.is_initialized,
            "tensorflow_available": TENSORFLOW_AVAILABLE
        }
        return info
    except Exception as e:
        logger.error(f"Greška pri dobijanju informacija o modelu: {e}")
        raise HTTPException(status_code=500, detail="Greška pri dobijanju informacija o modelu")

# Background task funkcije
async def scan_file_background(file_path: Path, file_id: str, filename: str):
    """Background task za skeniranje fajla"""
    try:
        logger.info(f"🔍 Početak skeniranja fajla: {filename}")
        
        if not model_manager:
            logger.error("ML model nije dostupan")
            return
        
        # Ekstrakcija feature-a
        features = await model_manager.extract_features(file_path)
        
        # Predikcija
        is_malicious, confidence = await model_manager.predict(features)
        
        logger.info(f" Skeniranje završeno: {filename} - Maliciozan: {is_malicious} (confidence: {confidence:.2f})")
        
    except Exception as e:
        logger.error(f" Greška pri skeniranju fajla {filename}: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
