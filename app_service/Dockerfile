# Usar la imagen base oficial de Python
FROM python:3.12-slim

# Desactivar la comprobación de versiones de pip y configurar stdout sin buffer
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Instalar las dependencias necesarias para compilar e instalar psycopg2 y otras librerías
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del directorio actual al contenedor
COPY . .

# Exponer el puerto 8000 para la API de FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "app_service.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
