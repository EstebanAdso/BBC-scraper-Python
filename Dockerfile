FROM python:3.9-slim

WORKDIR /app

COPY . .

# Crear el directorio para archivos generados si no existe
RUN mkdir -p ArchivosGenerados

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Por defecto, ejecutar el script principal
CMD ["python", "main.py"]
