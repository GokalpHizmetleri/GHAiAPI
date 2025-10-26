# Ollama tabanlı resmi image'den başla
FROM ollama/ollama:latest

# Python kurulumu (Ollama image Ubuntu tabanlıdır)
RUN apt-get update && apt-get install -y python3 python3-pip

# Uygulama dosyalarını kopyala
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY . /app

# SmolLM modelini indir (Render build aşamasında indirilecek)
RUN ollama pull smollm

# Ollama servisini başlat ve aynı anda FastAPI'yi çalıştır
CMD ollama serve & uvicorn main:app --host 0.0.0.0 --port 10000
