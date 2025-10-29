# Base image
FROM python:3.12-slim

# Evitar warnings de buffer
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema para pycups
RUN apt-get update && apt-get install -y \
    libcups2-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Exponer puerto de la API
EXPOSE 8000

RUN chmod +x /app/scripts/docker-entrypoint.sh

# Comando para correr el docker
CMD ["/app/scripts/docker-entrypoint.sh"]
