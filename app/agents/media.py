import os
import asyncio
import requests
from openai import OpenAI
from app.models.state import GraphState

# Inicializamos el cliente de OpenAI con tu llave del .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_image_task(prompt: str, scene_num: int):
    """Genera imágenes de lujo con DALL-E 3."""
    print(f"🎨 Generando imagen DALL-E 3 para escena {scene_num}...")
    
    try:
        # DALL-E 3 es increíble para prompts de lujo
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Fotografía cinematográfica 4k, estilo lujo minimalista: {prompt}",
            size="1024x1792", # Formato vertical para redes sociales
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        path = f"assets/inputs/scene_{scene_num}.png"
        os.makedirs("assets/inputs", exist_ok=True)

        # Descargamos la imagen al Droplet
        img_data = requests.get(image_url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)
            
        return path
    except Exception as e:
        print(f"❌ Error en DALL-E: {e}")
        return None

async def generate_voiceover_task(text_list: list):
    """Genera locución premium con OpenAI TTS."""
    print("🎙️ Generando locución OpenAI (Modelo: Onyx)...")
    
    full_text = " ".join(text_list)
    path = "assets/audio/voiceover.mp3"
    os.makedirs("assets/audio", exist_ok=True)

    try:
        # 'onyx' es una voz profunda y profesional, ideal para fragancias
        response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer", 
            input=full_text
        )
        
        response.stream_to_file(path)
        return path
    except Exception as e:
        print(f"❌ Error en OpenAI TTS: {e}")
        return None

async def media_node(state: GraphState):
    project = state.get("project_data")
    if not project: return {"status": "failed"}

    scenes = project.scenes
    voice_texts = [s.voiceover_text for s in scenes]
    
    try:
        # Ejecución en paralelo para ahorrar tiempo
        image_tasks = [generate_image_task(s.image_prompt, s.num) for s in scenes]
        audio_task = generate_voiceover_task(voice_texts)
        
        results = await asyncio.gather(*image_tasks, audio_task)
        
        return {
            "image_paths": results[:-1],
            "audio_path": results[-1],
            "status": "media_assets_generated"
        }
    except Exception as e:
        print(f"❌ Error en Agente de Medios: {e}")
        return {"status": "failed"}