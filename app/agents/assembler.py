from app.models.state import GraphState
from app.services.video_engine import build_esentia_engine
import asyncio
import os

async def assembler_node(state: GraphState):
    """
    Nodo final que orquesta el renderizado físico del video.
    """
    print("🎬 Agente de Ensamblaje: Iniciando renderizado final de esentia...")
    
    # Extraemos los datos necesarios del estado
    project_data = state["project_data"]
    image_paths = state["image_paths"]
    audio_path = state["audio_path"]
    
    try:
        # Ejecutamos el renderizado en un hilo separado para no bloquear el loop asíncrono
        # MoviePy/FFmpeg son intensivos en CPU y no son nativamente asíncronos.
        loop = asyncio.get_event_loop()
        output_path = "assets/outputs/esentia_final_ad.mp4"
        
        # Corremos el motor de video que definimos previamente
        final_path = await loop.run_in_executor(
            None, 
            build_esentia_engine, 
            project_data, 
            image_paths, 
            audio_path,
            output_path
        )
        
        return {
                    "video_url": f"/assets/outputs/{os.path.basename(final_path)}",
                    "status": "completed"
        }
        
    except Exception as e:
            # AGREGAR ESTA LÍNEA PARA VER EL ERROR REAL EN DOCKER LOGS
            print(f"❌ ERROR REAL EN EL MOTOR DE VIDEO: {str(e)}")
            return {
                "error_message": f"Error en Agente de Ensamblaje: {str(e)}",
                "status": "failed",
                "video_url": None # Aseguramos que sea None para el check de main.py
            }