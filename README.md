# ⚡ AXIOM — Adaptive eXperimental Intelligence Operating Machine

> A defense-grade, edge-cloud hybrid AI assistant built from scratch by Robair Farag. Deployed on NVIDIA Jetson Orin, orchestrated with Kubernetes, secured with JWT, and monitored with Prometheus and Grafana.

## 🎯 What is AXIOM?

AXIOM is a production-grade AI assistant system that goes far beyond a simple chatbot. It combines voice interaction, persistent memory, real-time web search, system control, file analysis, and a holographic interface — all running across a hybrid edge-cloud architecture. Built to demonstrate real-world AI engineering skills for roles in tech, aerospace, and defense.

## 🏗️ Architecture

CLOUD LAYER (DigitalOcean Droplet) — REST API, JWT Auth, Rate Limiting, Prometheus Metrics
ORCHESTRATION LAYER (Kubernetes K3s) — AXIOM Service, Grafana, Prometheus, Auto-healing
DEVELOPMENT LAYER (HP Pavilion i7, Ubuntu 24.04) — Voice Assistant, Wake Word, System Control
EDGE LAYER (NVIDIA Jetson Orin Nano) — On-device AI, Offline Capable, ARM Architecture

## ✅ Features

AI Brain — Powered by Claude Sonnet (Anthropic) with streaming responses, natural conversational personality, and context-aware interactions across all sessions.

Persistent Memory — Remembers conversations across sessions using JSON-based memory store with timestamp tracking. Wipe memory on command.

Voice System — Wake word detection (say Hey AXIOM to activate), voice input via Google Speech Recognition, natural voice output via ElevenLabs, fully hands-free operation.

Web Search — Autonomous real-time web search via DuckDuckGo. AXIOM decides when to search without being told and synthesizes results into natural language.

System Control — Live CPU, memory, and disk monitoring. Open applications, create folders, list files, and control volume by voice command.

File Intelligence — Read and summarize PDF documents, Word (.docx) files, and plain text files on command.

Security — JWT authentication on all protected endpoints, role-based access control, rate limiting at 60 requests per minute per IP, environment-based secret management.

Containerization — Full Docker containerization with Docker Compose for local orchestration and an optimized multi-step Dockerfile.

Kubernetes Orchestration — K3s lightweight Kubernetes cluster with Persistent Volume Claims, auto-healing deployments, and service mesh with ClusterIP routing.

Monitoring — Prometheus metrics collection with Grafana visualization dashboard, custom chat request counters, and response time tracking.

Edge AI Deployment — Runs natively on NVIDIA Jetson Orin Nano with ARM architecture support, offline capable with the same codebase as cloud deployment.

Holographic UI — Iron Man inspired interface with real-time system stats, live chat, animated voice waveform, and full dark holographic theme.

## 🛠️ Tech Stack

AI Model: Claude Sonnet by Anthropic
Voice Input: Google Speech Recognition and PyAudio
Voice Output: ElevenLabs TTS
Backend: Python and Flask
Security: JWT and Flask-CORS
Monitoring: Prometheus and Grafana
Containerization: Docker
Orchestration: Kubernetes K3s
Edge Device: NVIDIA Jetson Orin Nano
Cloud: DigitalOcean Droplet
Frontend: HTML, CSS, JavaScript
Memory: JSON and ChromaDB
Web Search: DuckDuckGo
OS: Ubuntu 22.04 and 24.04 LTS

## 📁 Project Structure

-AXIOM/
├── src/
│   ├── brain/
│   │   ├── axiom.py              # Voice assistant (laptop)
│   │   ├── axiom_headless.py     # Cloud API service
│   │   └── axiom_edge.py         # Jetson edge deployment
│   ├── voice/
│   │   ├── listener.py           # Microphone input
│   │   ├── speaker.py            # ElevenLabs TTS output
│   │   └── wakeword.py           # Wake word detection
│   ├── memory/
│   │   └── memory.py             # Persistent memory system
│   ├── tools/
│   │   ├── search.py             # Web search
│   │   ├── system.py             # System control
│   │   └── file_reader.py        # Document analysis
│   ├── security/
│   │   └── security.py           # JWT auth and rate limiting
│   └── ui/
│       └── index.html            # Holographic interface
├── deploy/
│   └── kubernetes/
│       ├── axiom-deployment.yaml
│       ├── axiom-service.yaml
│       ├── axiom-pvc.yaml
│       └── monitoring.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## 🚀 Quick Start

Clone the repository: git clone https://github.com/Robair26/-AXIOM.git then cd into -AXIOM

Set up environment: python3 -m venv axiom-env then source axiom-env/bin/activate then pip install -r requirements.txt

Configure API keys: cp .env.example .env then add your Anthropic and ElevenLabs API keys

Run voice assistant: python src/brain/axiom.py

Run as API service: python src/brain/axiom_headless.py

Deploy with Docker: docker build -t axiom . then docker-compose up

Deploy to Kubernetes: kubectl apply -f deploy/kubernetes/

Run on Jetson Edge: python src/brain/axiom_edge.py

## 🔌 API Endpoints

GET /health — No auth required — System health check
POST /auth — No auth required — Get JWT token
POST /chat — JWT required — Send message to AXIOM
GET /stats — JWT required — Get live system stats
DELETE /memory/clear — JWT required — Wipe AXIOM memory
GET /metrics — No auth required — Prometheus metrics

## 🖥️ Deployment

Local Voice Assistant — Runs on laptop with full voice input and output using wake word activation and ElevenLabs voice.

Cloud API on DigitalOcean — Headless Flask API running as a Docker container on a DigitalOcean Droplet with systemd service management for auto-restart.

Kubernetes Cluster — Full K3s deployment with AXIOM, Prometheus, and Grafana pods running with persistent storage and auto-healing on any crash.

Edge Device on NVIDIA Jetson Orin Nano — AXIOM Edge runs directly on ARM hardware using the Tegra Orin GPU for local inference with no cloud required.

## 📊 Monitoring

Access Grafana: kubectl port-forward service/grafana-service 3000:3000 then open http://localhost:3000 and login with admin/admin

Access Prometheus: kubectl port-forward service/prometheus-service 9090:9090 then open http://localhost:9090

## 🔒 Security

All chat and stats endpoints require a valid JWT token obtained via the /auth endpoint. Rate limiting is enforced at 60 requests per minute per IP address. All API keys are stored in environment variables and never committed to version control.

## 👤 Built By

Robair Farag — AI Engineer and Builder
GitHub: https://github.com/Robair26
Project: https://github.com/Robair26/-AXIOM

## 📌 Roadmap

Gmail and Google Calendar integration for email and schedule management
Computer vision via Jetson camera for real-time object detection and face recognition
Multi-agent system with specialized agents working in parallel
Mobile interface for iOS and Android
Voice cloning for fully personalized AXIOM voice
