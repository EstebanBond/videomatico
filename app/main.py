from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Importamos el grafo de agentes
from app.core.graph import esentia_graph

app = FastAPI(title="Videomatico - Esentia Engine")

# --- 1. CONFIGURACIÓN DE CORS ---
# Permite que tu frontend hable con la API sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. GESTIÓN DE DIRECTORIOS ---
# Aseguramos que existan las carpetas necesarias para evitar errores de escritura
folders = ["assets/outputs", "assets/inputs", "assets/audio"]
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# --- 3. SERVIDO DE ARCHIVOS ---
# Montamos la carpeta assets para que los videos y el grano sean accesibles vía URL
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Servimos los archivos del frontend (HTML y Assets de diseño)
# Asumiendo que index.html y Background_Grain.jpg están en app/static/
@app.get("/")
async def read_index():
    index_path = os.path.join('app', 'static', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html no encontrado en app/static/"}

# --- 4. ENDPOINT DE GENERACIÓN ---
@app.post("/generate-esentia-ad/")
async def generate_ad():
    # Estado inicial para el flujo de agentes (LangGraph)
    initial_state = {
        "project_data": None,
        "image_paths": [],
        "audio_path": None,
        "video_url": None,
        "status": "starting"
    }
    
    try:
        print("🧠 Iniciando orquestación de agentes para Esentia...")
        
        # Ejecutamos el grafo. Nota: Esta llamada es síncrona para el cliente (espera la respuesta)
        result = await esentia_graph.ainvoke(initial_state)
        
        video_url = result.get("video_url")
            
        if not video_url:
            raise HTTPException(
                status_code=500, 
                detail="El proceso terminó pero no se obtuvo una URL de video."
            )
        
        print(f"✅ Video generado exitosamente: {video_url}")
        return {"url": video_url, "status": "completed"}
        
    except Exception as e:
        print(f"❌ Error crítico en el motor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))