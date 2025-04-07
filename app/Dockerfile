FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wait-for-it

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

CMD ["sh", "-c", "wait-for-it db:5432 -- uvicorn main:app --host 0.0.0.0 --port 8000"]