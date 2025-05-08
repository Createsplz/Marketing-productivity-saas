FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip

COPY requirements.txt .

# Instala dependências e mostra se uvicorn foi instalado corretamente
RUN pip install --no-cache-dir -r requirements.txt && pip show uvicorn

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
