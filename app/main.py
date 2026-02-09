from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.core.graph import esentia_graph

app = FastAPI(title="Videomatico")

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

@app.post("/generate-esentia-ad/")
async def generate_ad():
    # Iniciamos el grafo con un estado vacío
    initial_state = {
        "project_data": None,
        "image_paths": [],
        "audio_path": None,
        "final_video_path": None,
        "status": "starting"
    }
    
    # Ejecutamos la orquestación de agentes
    result = await esentia_graph.ainvoke(initial_state)
    
    return {
        "message": "Video de esentia generado con éxito",
        "video_url": result["final_video_path"],
        "status": result["status"]
    }