import os
import asyncio
from google.cloud import aiplatform
from google.cloud import texttospeech
from vertexai.preview.vision_models import ImageGenerationModel
from app.models.state import GraphState

# Inicialización de servicios de Google Cloud
# Nota: Asegúrate de tener configuradas tus credenciales de Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tu-archivo-de-credenciales.json"

async def generate_image_task(prompt: str, scene_num: int):
    """Tarea asíncrona para generar una imagen con Imagen 3 en Vertex AI."""
    print(f"🎨 Generando imagen para escena {scene_num}...")
    
    # En un entorno real de Vertex AI:
    # model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    # response = model.generate_images(prompt=prompt)
    # path = f"assets/inputs/scene_{scene_num}.png"
    # response[0].save(location=path, include_generation_parameters=False)
    
    # Simulación para desarrollo local (Placeholders elegantes)
    await asyncio.sleep(2) # Simula latencia de red
    path = f"assets/inputs/scene_{scene_num}.png"
    return path

async def generate_voiceover_task(text_list: list):
    """Genera un solo archivo de audio uniendo todos los guiones de las escenas."""
    print("🎙️ Generando locución premium con Google TTS...")
    
    client = texttospeech.TextToSpeechClient()
    full_text = " ".join(text_list)
    
    synthesis_input = texttospeech.SynthesisInput(text=full_text)
    
    # Voz de lujo: Usamos una voz 'Neural' o 'Studio' para máxima calidad
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES",
        name="es-ES-Neural2-F", # Voz femenina neural de alta calidad
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=0.0,
        speaking_rate=0.9 # Un poco más lento para tono de lujo
    )

    # Nota: Esta llamada es síncrona en el SDK de Google, 
    # por eso la envolvemos en el hilo de ejecución asíncrono
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    path = "assets/audio/voiceover.mp3"
    with open(path, "wb") as out:
        out.write(response.audio_content)
    
    return path

async def media_node(state: GraphState):
    project = state["project_data"]
    
    # Extraemos los datos del proyecto generado por Gemini
    scenes = project.scenes
    voice_texts = [s.voiceover_text for s in scenes]
    
    try:
        # 🚀 LANZAMIENTO EN PARALELO (Grandes Ligas)
        # Generamos las 5 imágenes y el audio al mismo tiempo
        image_tasks = [generate_image_task(s.image_prompt, s.num) for s in scenes]
        audio_task = generate_voiceover_task(voice_texts)
        
        # Esperamos a que todas las tareas terminen
        results = await asyncio.gather(*image_tasks, audio_task)
        
        image_paths = results[:-1]
        audio_path = results[-1]
        
        return {
            "image_paths": image_paths,
            "audio_path": audio_path,
            "status": "media_assets_generated"
        }
        
    except Exception as e:
        return {
            "error_message": f"Error en Agente de Medios: {str(e)}",
            "status": "failed"
        }