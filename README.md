# ⚡ AXIOM — Adaptive eXperimental Intelligence Operating Machine

> A defense-grade, edge-cloud hybrid AI assistant built from scratch by Robair Farag. Deployed on NVIDIA Jetson Orin, orchestrated with Kubernetes, secured with JWT, and monitored with Prometheus and Grafana. Live at https://axiom.bitshadow.dev

---

## 🎯 What is AXIOM?

AXIOM is a production-grade AI assistant system that goes far beyond a simple chatbot. It combines voice interaction, persistent memory, real-time web search, system control, file analysis, a holographic interface with an animated face, multi-agent debate system, morning intelligence briefings, and a 24/7 web watchdog — all running across a hybrid edge-cloud architecture. Built to demonstrate real-world AI engineering skills for roles in tech, aerospace, and defense.

---

## 🌐 Live Demo

https://axiom.bitshadow.dev

---

## 🏗️ Architecture

CLOUD LAYER (DigitalOcean Droplet) — REST API, JWT Auth, Rate Limiting, Prometheus Metrics
ORCHESTRATION LAYER (Kubernetes K3s) — AXIOM Service, Grafana, Prometheus, Auto-healing
DEVELOPMENT LAYER (HP Pavilion i7, Ubuntu 24.04) — Voice Assistant, Wake Word, System Control
EDGE LAYER (NVIDIA Jetson Orin Nano) — On-device AI, Offline Capable, ARM Architecture

---

## ✅ Complete Feature List

AI Brain — Powered by Claude Sonnet with streaming responses, natural conversational personality, and context-aware interactions across all sessions.

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

Holographic UI — Iron Man inspired interface with animated holographic face, real-time system stats, live chat, voice waveform, and full dark theme. Mobile responsive — works perfectly on any phone or tablet browser.

Animated Face — Real-time animated AI face that reacts when AXIOM speaks. Eyes move, mouth syncs to voice, particles and scan lines create a holographic presence.

Multi-Agent Debate System — Three specialized AXIOM agents (Alpha analytical, Beta creative, Gamma critical) debate any question and synthesize a unified answer. Triggered by the DEBATE button.

Proactive System Monitoring — AXIOM watches your system 24/7 and speaks up on his own when CPU spikes, memory is low, disk is critical, or unusual network activity is detected. No asking required.

Morning Intelligence Briefing — AXIOM scans world news, tech news, and weather every morning and delivers a spoken briefing automatically. Trigger manually by saying brief me.

Web Watchdog — Tell AXIOM to monitor any topic, website, or keyword. He checks every 30 minutes and alerts you the moment something new happens.

Conversation Mode — Toggle hands-free conversation mode for natural back-and-forth voice interaction. AXIOM listens, responds, and prompts you for your next message automatically.

Interrupt Control — Stop AXIOM mid-speech anytime with the stop button. Full control over the conversation flow.

Cloudflare SSL — Production HTTPS deployment via Cloudflare tunnel with automatic SSL certificate and DDoS protection.

24/7 Auto-restart — Systemd service on Droplet ensures AXIOM restarts automatically on any crash or server reboot.

---

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
DNS and SSL: Cloudflare
Frontend: HTML, CSS, JavaScript
Memory: JSON and ChromaDB
Web Search: DuckDuckGo
Scheduling: Python Schedule
OS: Ubuntu 22.04 and 24.04 LTS

---

## 📁 Project Structure

-AXIOM/
├── src/
│   ├── brain/
│   │   ├── axiom.py              # Voice assistant laptop
│   │   ├── axiom_headless.py     # Cloud API service
│   │   ├── axiom_edge.py         # Jetson edge deployment
│   │   ├── axiom_agents.py       # Multi-agent debate system
│   │   ├── axiom_monitor.py      # Proactive system monitor
│   │   └── axiom_butler.py       # Morning briefings and watchdog
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
│       ├── index.html            # Holographic interface
│       └── face.html             # Animated AI face
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

---

## 🚀 Quick Start

Clone the repository: git clone https://github.com/Robair26/-AXIOM.git then cd into -AXIOM

Set up environment: python3 -m venv axiom-env then source axiom-env/bin/activate then pip install -r requirements.txt

Configure API keys: cp .env.example .env then add your Anthropic and ElevenLabs API keys

Run voice assistant on laptop: python src/brain/axiom.py

Run as cloud API service: python src/brain/axiom_headless.py

Deploy with Docker: docker build -t axiom . then docker-compose up

Deploy to Kubernetes: kubectl apply -f deploy/kubernetes/

Run on Jetson Edge: python src/brain/axiom_edge.py

---

## 🔌 API Endpoints

GET /health — No auth required — System health check
POST /auth — No auth required — Get JWT token
POST /chat — JWT required — Send message to AXIOM
POST /debate — JWT required — Trigger multi-agent debate
POST /speak — JWT required — Text to speech via ElevenLabs
GET /stats — JWT required — Get live system stats
GET /alerts — No auth required — SSE stream for proactive alerts
POST /watch — JWT required — Add topic to watchlist
GET /watchlist — JWT required — Get current watchlist
POST /briefing — JWT required — Trigger morning briefing now
DELETE /memory/clear — JWT required — Wipe AXIOM memory
GET /metrics — No auth required — Prometheus metrics

---

## 🖥️ Deployment

Local Voice Assistant — Runs on laptop with full voice input and output using wake word activation and ElevenLabs voice.

Cloud API on DigitalOcean — Headless Flask API running as a Docker container on a DigitalOcean Droplet with systemd service management for auto-restart and Cloudflare SSL tunnel.

Kubernetes Cluster — Full K3s deployment with AXIOM, Prometheus, and Grafana pods running with persistent storage and auto-healing on any crash.

Edge Device on NVIDIA Jetson Orin Nano — AXIOM Edge runs directly on ARM hardware using the Tegra Orin GPU for local inference with no cloud required.

---

## 📊 Monitoring

Access Grafana: kubectl port-forward service/grafana-service 3000:3000 then open http://localhost:3000 and login with admin/admin

Access Prometheus: kubectl port-forward service/prometheus-service 9090:9090 then open http://localhost:9090

---

## 🔒 Security

All chat and stats endpoints require a valid JWT token obtained via the /auth endpoint. Rate limiting is enforced at 60 requests per minute per IP address. All API keys are stored in environment variables and never committed to version control. Cloudflare tunnel provides additional security layer with DDoS protection.

---

## 🤖 AXIOM Commands

Say or type these to see AXIOM in action:

brief me — triggers a live morning briefing from real web search
watch AI news — AXIOM starts monitoring AI news 24/7
watch SpaceX — AXIOM monitors SpaceX updates and alerts on changes
what are you watching — lists all active watchlist topics
stop watching AI news — removes topic from watchlist
debate: is AI going to replace humans — triggers multi-agent debate
how is my system doing — live CPU memory and disk report
open firefox — opens application by voice command
create a folder called projects — creates folder on your machine
what is the latest news in AI — autonomous web search
read this file — AXIOM reads and summarizes any document
Hey AXIOM — wake word to activate voice assistant on laptop
exit — shuts down AXIOM
forget — wipes all memory and starts fresh

---

## 👤 Built By

Robair Farag — AI Engineer and Builder
GitHub: https://github.com/Robair26
Project: https://github.com/Robair26/-AXIOM
Live: https://axiom.bitshadow.dev

---

## 📌 Roadmap

Computer vision via Jetson camera for real-time object detection and face recognition
Voice cloning for fully personalized AXIOM voice
Autonomous code writing and execution
Browser automation and control
Gmail and Google Calendar integration
