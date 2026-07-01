# ML Detekcija Malvera — IoT Malware Detection System

A simulation of a malware detection system for IoT environments, developed in Python with a web interface and REST API.

## About

Modern IoT ecosystems include a large number of connected devices exchanging data in real time, which poses a serious security challenge. Because IoT devices have limited resources, traditional antivirus software isn't sufficient, so systems based on machine learning and automated file analysis are increasingly used in practice.

This project presents a simulation of a complete malware detection platform. Its goal is to analyze different types of files — from text logs, configuration files, and scripts, to binary files and images — and to assess potential malicious activity based on a trained ML model. The system is specifically adapted for scenarios where IoT devices send data to a central server for analysis, requiring fast and asynchronous processing.

## Project Structure

```
ml-detekcija-malvera/
├── api/            # REST API implementation
├── docs/           # Documentation
├── ml/             # Machine learning logic
├── models/         # Trained ML models
├── notebooks/      # Jupyter notebooks (analysis, experiments, training)
├── scripts/        # Utility and automation scripts
├── test_cases/     # Test cases
├── simple_requirements.txt
└── start_web_app.py
```

## Tech Stack

- Python
- Jupyter Notebook (model training and analysis)
- Lightweight web server
- REST API
- Machine Learning

## Getting Started

Install dependencies:

```bash
pip install -r simple_requirements.txt
```

Run the web application:

```bash
python start_web_app.py
```

Once started, the interface and API are available at: `http://localhost:8000`

## REST API

The platform provides three key endpoints:

| Method & Route | Description |
|---|---|
| `POST /analyze` | Accepts a file and runs the ML model to analyze its content |
| `GET /health` | Checks system status and availability |
| `GET /model-info` | Returns information about the loaded model, its version, and parameters |

These endpoints allow integration with IoT devices, scripts, or other applications that require automated threat detection.

## Supported File Types

The system supports analysis of a wide range of file extensions, including:

`.txt`, `.log`, `.config`, `.php`, `.js`, `.py`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`

This broad support covers real-world security scenarios, especially in environments where IoT devices generate diverse files — from logs to sensor images.

## Features

- **Asynchronous processing** — analyzes multiple files without blocking the system
- **Real-time analysis** — immediately returns detection results
- **Web interface** — simple UI for manual testing and result review
- **REST API** — enables automated file submission via scripts or IoT devices
- **Detailed logging** — tracks processing flow and generates audit trails
- **Multi-format support** — easy integration into heterogeneous environments

## Author

Luka Savić
