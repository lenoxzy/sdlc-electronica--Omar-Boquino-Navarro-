FROM python:3.12-slim
WORKDIR /app

# Dependencias primero: aprovecha la cache de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto que usará Uvicorn
EXPOSE 8000

# Comando para arrancar el servidor
# Comando para migrar la base de datos y luego arrancar el servidor
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]