from fastapi import FastAPI, BackgroundTasks
from app.services.video_engine import create_lsm_video
import uuid

app = FastAPI(title="Sikno Video Automator")

@app.post("/generate-video/{word}")
async def generate_video(word: str, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    input_file = "assets/inputs/cuantocuesta.mp4"
    output_file = f"assets/outputs/video_{job_id}.mp4"
    
    # Ejecutamos en segundo plano para no bloquear la API
    background_tasks.add_task(create_lsm_video, word, input_file, output_file)
    
    return {"message": "Procesando video", "job_id": job_id, "word": word}

@app.get("/")
def read_root():
    return {"status": "Online", "engine": "MoviePy + FastAPI"}