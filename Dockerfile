FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    espeak \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    libpulse-dev \
    ffmpeg \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir pyaudio --global-option="build_ext" --global-option="-I/usr/include" || \
    apt-get install -y python3-pyaudio

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/brain/axiom.py"]
