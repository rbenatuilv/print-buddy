FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar pycups
RUN apt-get update && apt-get install -y \
    gcc \
    libcups2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]