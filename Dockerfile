# ---- Etapa de build ----
# Esta etapa solo existe para instalar dependencias; su contenido final
# NO viaja completo a la imagen de producción, solo lo que copiamos
# explícitamente en la segunda etapa (multi-stage build).
FROM python:3.12-slim AS builder
WORKDIR /app

# Creamos un entorno virtual aislado dentro de la imagen. Esto permite
# copiar SOLO esa carpeta (/opt/venv) a la etapa final, en vez de arrastrar
# también las herramientas de compilación que pip pudo haber usado.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiamos primero solo requirements.txt (no el resto del código) para
# aprovechar la cache de capas de Docker: si el código cambia pero las
# dependencias no, esta capa se reutiliza y el build es mucho más rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Etapa final (runtime) ----
# Imagen limpia desde cero. Aquí es donde termina realmente el tamaño de
# la imagen que se despliega — todo lo de la etapa "builder" que no se
# copie explícitamente abajo, se descarta por completo.
FROM python:3.12-slim
WORKDIR /app

# Copiamos SOLO el entorno virtual ya armado desde la etapa builder —
# no reinstalamos nada aquí, así evitamos duplicar herramientas de compilación.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiamos selectivamente solo lo que la app necesita para correr:
# el código de la API, las migraciones de Alembic, y su archivo de config.
# NO copiamos tests/, las carpetas semanaX/, ni requirements-dev.txt —
# nada de eso es necesario en producción (además .dockerignore refuerza esto).
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .

# Puerto en el que Uvicorn va a escuchar dentro del contenedor.
EXPOSE 8000

# Comando de arranque real del contenedor. El "sh -c" permite encadenar dos
# comandos con &&: primero aplica las migraciones pendientes de Alembic
# (crea/actualiza el esquema en la base de datos real ANTES de aceptar
# tráfico), y solo si eso tiene éxito, levanta el servidor Uvicorn.
# Esto evita el escenario "deploy verde, API muerta porque no existe la tabla".
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]