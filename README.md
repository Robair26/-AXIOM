# ⚡ AXIOM — Adaptive eXperimental Intelligence Operating Machine

> An edge-cloud hybrid AI assistant built by Robair Farag. Runs on a laptop, a cloud server, and an NVIDIA Jetson Orin Nano. Orchestrated with Kubernetes (K3s), secured with JWT, and monitored with Prometheus and Grafana. Live at https://axiom.bitshadow.dev

---

## 🎯 What is AXIOM?

AXIOM is an AI assistant system that combines voice interaction, persistent memory, real-time web search, system control, file analysis, a holographic web interface with an animated face, a multi-agent debate system, morning briefings, and a web watchdog. It runs across a hybrid edge-cloud architecture and uses the Anthropic API (Claude Sonnet) for reasoning.

---

## 🌐 Live Demo

https://axiom.bitshadow.dev

---

## 🏗️ Architecture

```
CLOUD LAYER (DigitalOcean Droplet) — REST API, JWT Auth, Rate Limiting, Prometheus Metrics
ORCHESTRATION LAYER (Kubernetes K3s) — AXIOM Service, Grafana, Prometheus, Auto-healing
DEVELOPMENT LAYER (HP Pavilion i7, Ubuntu 24.04) — Voice Assistant, Wake Word, System Control
EDGE LAYER (NVIDIA Jetson Orin Nano) — On-device deployment, ARM architecture
```

Note: reasoning uses the Anthropic API, so responses need an internet connection unless a local model is configured.

---

## ✅ Feature List

**AI Brain** — Powered by Claude Sonnet with streaming responses and context-aware conversation across sessions.

**Persistent Memory** — Remembers conversations across sessions using a JSON-based memory store with timestamp tracking. Wipe memory on command.

**Voice System** — Wake word detection ("Hey AXIOM"), voice input via Google Speech Recognition, voice output via ElevenLabs, and hands-free operation.

**Web Search** — Real-time web search via DuckDuckGo. AXIOM decides when to search and synthesizes the results into a natural-language answer.

**System Control** — Live CPU, memory, and disk monitoring. Open applications, create folders, list files, and control volume by voice command.

**File Intelligence** — Read and summarize PDF, Word (.docx), and plain text files on command.

**Security** — JWT authentication on protected endpoints, role-based access control, rate limiting at 60 requests per minute per IP, and environment-based secret management.

**Containerization** — Docker with Docker Compose for local orchestration and a multi-step Dockerfile.

**Kubernetes Orchestration** — K3s cluster with Persistent Volume Claims, auto-healing deployments, and ClusterIP services.

**Monitoring** — Prometheus metrics with Grafana dashboards, custom chat request counters, and response time tracking.

**Edge Deployment** — Runs on an NVIDIA Jetson Orin Nano (ARM) from the same codebase as the cloud deployment.

**Holographic UI** — Iron Man-inspired web interface with an animated face, real-time system stats, live chat, voice waveform, and a dark theme. Mobile responsive.

**Animated Face** — Animated AI face that reacts when AXIOM speaks: eye movement, mouth sync to voice, particles, and scan lines.

**Multi-Agent Debate** — Three AXIOM agents (Alpha analytical, Beta creative, Gamma critical) debate a question and synthesize a single answer. Triggered by the DEBATE button.

**Proactive System Monitoring** — Watches the system and speaks up on CPU spikes, low memory, critical disk usage, or unusual network activity.

**Morning Briefing** — Scans world news, tech news, and weather and delivers a spoken briefing. Trigger manually by saying "brief me."

**Web Watchdog** — Monitor any topic, website, or keyword. Checks every 30 minutes and alerts on new results.

**Conversation Mode** — Hands-free back-and-forth voice interaction.

**Interrupt Control** — Stop AXIOM mid-speech with the stop button.

**Cloudflare SSL** — HTTPS via a Cloudflare tunnel with automatic SSL certificates.

**Auto-restart** — A systemd service on the Droplet restarts AXIOM after a crash or reboot.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Model | Claude Sonnet (Anthropic API) |
| Voice Input | Google Speech Recognition, PyAudio |
| Voice Output | ElevenLabs TTS |
| Backend | Python, Flask |
| Security | JWT, Flask-CORS |
| Monitoring | Prometheus, Grafana |
| Containerization | Docker |
| Orchestration | Kubernetes K3s |
| Edge Device | NVIDIA Jetson Orin Nano |
| Cloud | DigitalOcean Droplet |
| DNS and SSL | Cloudflare |
| Frontend | HTML, CSS, JavaScript |
| Memory | JSON store |
| Web Search | DuckDuckGo |
| Scheduling | Python Schedule |
| OS | Ubuntu 22.04 and 24.04 LTS |

---

## 📁 Project Structure

```
AXIOM/
├── src/
│   ├── brain/
│   │   ├── axiom.py              # Voice assistant (laptop)
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
│   │   └── memory.py             # Persistent memory
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
```

---

## 🚀 Quick Start

Requirements: Python 3.10 or newer. For voice input on Linux, install PortAudio first: `sudo apt install portaudio19-dev`.

```bash
git clone https://github.com/Robair26/AXIOM.git
cd AXIOM
python3 -m venv axiom-env
source axiom-env/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your Anthropic and ElevenLabs API keys and a JWT secret (see `.env.example` for the variable names).

```bash
# Voice assistant on a laptop
python src/brain/axiom.py

# Cloud API service
python src/brain/axiom_headless.py

# Docker
docker build -t axiom .
docker-compose up

# Kubernetes
kubectl apply -f deploy/kubernetes/

# Jetson edge
python src/brain/axiom_edge.py
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /health | None | System health check |
| POST | /auth | None | Get a JWT token |
| POST | /chat | JWT | Send a message to AXIOM |
| POST | /debate | JWT | Trigger a multi-agent debate |
| POST | /speak | JWT | Text to speech via ElevenLabs |
| GET | /stats | JWT | Live system stats |
| GET | /alerts | None | SSE stream for proactive alerts |
| POST | /watch | JWT | Add a topic to the watchlist |
| GET | /watchlist | JWT | Get the current watchlist |
| POST | /briefing | JWT | Trigger the morning briefing |
| DELETE | /memory/clear | JWT | Wipe AXIOM memory |
| GET | /metrics | None | Prometheus metrics |

`/health`, `/alerts`, and `/metrics` are intentionally public.

---

## 🖥️ Deployment

**Local voice assistant** — Runs on a laptop with voice input and output, wake word activation, and ElevenLabs voice.

**Cloud API on DigitalOcean** — Headless Flask API in a Docker container on a Droplet, managed by systemd for auto-restart and exposed through a Cloudflare SSL tunnel.

**Kubernetes cluster** — K3s deployment with AXIOM, Prometheus, and Grafana pods, persistent storage, and auto-healing.

**Edge device (NVIDIA Jetson Orin Nano)** — AXIOM Edge runs directly on ARM hardware from the same codebase. Reasoning uses the Anthropic API unless a local model is configured.

---

## 📊 Monitoring

Access Grafana:

```bash
kubectl port-forward service/grafana-service 3000:3000
```

Open http://localhost:3000. The default login is `admin` / `admin`. **Change the password on first login** and do not expose Grafana publicly with default credentials.

Access Prometheus:

```bash
kubectl port-forward service/prometheus-service 9090:9090
```

Open http://localhost:9090.

---

## 🔒 Security

- Chat, stats, and other protected endpoints require a JWT obtained from `/auth`.
- Rate limiting is enforced at 60 requests per minute per IP.
- API keys and secrets are stored in environment variables and are not committed to the repository.
- A Cloudflare tunnel provides HTTPS and an additional protection layer.

---

## 🤖 AXIOM Commands

Say or type these:

- `brief me` — live morning briefing from web search
- `watch AI news` — start monitoring a topic
- `watch SpaceX` — monitor SpaceX updates and alert on changes
- `what are you watching` — list active watchlist topics
- `stop watching AI news` — remove a topic from the watchlist
- `debate: is AI going to replace humans` — multi-agent debate
- `how is my system doing` — live CPU, memory, and disk report
- `open firefox` — open an application by voice
- `create a folder called projects` — create a folder on your machine
- `what is the latest news in AI` — web search
- `read this file` — read and summarize a document
- `Hey AXIOM` — wake word for the laptop voice assistant
- `exit` — shut down AXIOM
- `forget` — wipe all memory

---

## 👤 Built By

Robair Farag — M.S. Applied Artificial Intelligence, University of San Diego

- GitHub: https://github.com/Robair26
- Project: https://github.com/Robair26/AXIOM
- Live: https://axiom.bitshadow.dev

---

## 📌 Roadmap

- Computer vision via the Jetson camera for object detection and face recognition
- Voice cloning for a custom AXIOM voice
- Local model option for fully offline edge operation
- Browser automation
- Gmail and Google Calendar integration
