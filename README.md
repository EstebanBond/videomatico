# 🎥 Sikno Video Automator | High-Load Media API

Motor de orquestación para campañas de **Hiper-Personalización** desarrollado para la automatización masiva de activos de video verticales. Este sistema integra procesamiento de medios asíncrono y despliegue escalable.

## 🚀 Stack Tecnológico
* **Core:** Python 3.12 (Asíncrono)
* **API Framework:** FastAPI
* **Media Processing:** MoviePy (FFmpeg backend)
* **Environment Management:** UV (Astral)
* **DevOps:** Docker & Cloud-ready para DigitalOcean

## 🛠️ Arquitectura de "Grandes Ligas"
- **Procesamiento Asíncrono:** Uso de `BackgroundTasks` para evitar el bloqueo del event loop durante el renderizado de video pesado.
- **Aislamiento de Recursos:** Inyección dinámica de assets (fuentes, logos) para garantizar la portabilidad en sistemas de archivos restringidos (Read-only systems).
- **Escalabilidad:** Estructura modular preparada para migrar a una arquitectura de Workers (Redis/Celery).

## 📦 Instalación y Uso
1. Instalar dependencias: `uv sync`
2. Configurar assets: Colocar `template.mp4` en `assets/inputs/`
3. Ejecutar: `uv run uvicorn app.main:app --reload`

## 🐳 Cloud Ops (Docker)
Este proyecto está dockerizado para garantizar la consistencia de los binarios de FFmpeg e ImageMagick:
`docker build -t video-automator .`