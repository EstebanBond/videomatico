from fastapi import FastAPI, BackgroundTasks, HTTPException  # <--- Agregado HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.core.graph import esentia_graph

app = FastAPI(title="Videomatico")

# Importante: Asegúrate de que la carpeta assets exista al arrancar
if not os.path.exists("assets/outputs"):
    os.makedirs("assets/outputs", exist_ok=True)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def read_index():
    # Verifica que la ruta coincida con tu estructura de carpetas
    return FileResponse('app/static/index.html')

@app.post("/generate-esentia-ad/")
async def generate_ad():
    # Iniciamos el grafo con un estado inicial limpio
    initial_state = {
        "project_data": None,
        "image_paths": [],
        "audio_path": None,
        "video_url": None, # Cambiamos final_video_path por video_url para ser consistentes
        "status": "starting"
    }
    
    try:
        # Ejecutamos la orquestación de agentes
        # Nota: ainvoke puede tardar bastante, Traefik tiene un timeout por defecto
        result = await esentia_graph.ainvoke(initial_state)
        
        video_url = result.get("video_url")
            
        if not video_url:
            raise HTTPException(
                status_code=500, 
                detail="El video no se pudo generar en los nodos de ensamblaje"
            )
                
        return {"url": video_url}
        
    except Exception as e:
        print(f"❌ Error crítico en el endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))