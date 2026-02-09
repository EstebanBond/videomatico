# 1. Usamos una imagen de Python ligera y moderna
FROM python:3.12-slim

# 2. Instalamos dependencias de sistema críticas para video y audio
# FFmpeg: Renderizado de video
# ImageMagick: Escribir Textos
# libmagic1: Detecta tipos de archivos
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Configura politicas de ImageMagick.
RUN sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml

# 4. UV install
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 5. Work Space
WORKDIR /app

# 6. Copia archivos dependencias
COPY pyproject.toml uv.lock ./

# 7. Instala dependencias
RUN uv sync --frozen --no-install-project

# 8. Copia código y assets
COPY . .

# 9. Sinc proyecto final
RUN uv sync --frozen

# 10. Expose FastAPI port
EXPOSE 8000

# 11. Comd 'uv run' -> entorno virtual OK
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]