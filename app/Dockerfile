FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    libdlib-dev \
    wget \
    curl \
    git \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Запуск FastAPI-приложения с ожиданием PostgreSQL
CMD ["sh", "-c", "wait-for-it db:5432 -- uvicorn main:app --host 0.0.0.0 --port 8000"]
