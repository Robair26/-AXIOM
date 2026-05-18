FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    espeak \
    portaudio19-dev \
    libasound2-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "src/brain/axiom_headless.py"]
