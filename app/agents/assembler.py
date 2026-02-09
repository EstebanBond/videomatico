from app.models.state import GraphState
from app.services.video_engine import build_esentia_engine
import asyncio
import os
import traceback

async def assembler_node(state: GraphState):
    """
    Nodo final que orquesta el renderizado físico del video.
    """
    print("🎬 Agente de Ensamblaje: Iniciando revisión de activos...")

    # 1. Extraemos con seguridad
    image_paths = state.get("image_paths")
    audio_path = state.get("audio_path")
    project_data = state.get("project_data")

    # 🔍 DEBUG: Esto nos dirá qué está llegando realmente
    print(f"DEBUG - image_paths: {image_paths}")
    print(f"DEBUG - audio_path: {audio_path}")
    
    # 2. GUARD RAIL (Paracaídas): Si algo es None, no entramos al motor de video
    if not audio_path or not image_paths or project_data is None:
        error_msg = "❌ ERROR: Faltan activos (audio o imágenes). El nodo de Medios falló."
        print(error_msg)
        return {
            "error_message": error_msg,
            "status": "failed",
            "video_url": None
        }
    
    try:
        # 3. Preparación del renderizado
        loop = asyncio.get_event_loop()
        output_path = "assets/outputs/esentia_final_ad.mp4"
        
        # Aseguramos que la carpeta exista antes de intentar escribir
        os.makedirs("assets/outputs", exist_ok=True)
        
        print("🚀 Lanzando proceso de renderizado en el Executor...")
        
        # Ejecutamos el motor síncrono en un hilo aparte
        final_path = await loop.run_in_executor(
            None, 
            build_esentia_engine, 
            project_data, 
            image_paths, 
            audio_path,
            output_path
        )
        
        print(f"✅ Renderizado completo: {final_path}")
        return {
            "video_url": f"/assets/outputs/{os.path.basename(final_path)}",
            "status": "completed"
        }
        
    except Exception as e:
        print(f"❌ ERROR REAL EN EL MOTOR DE VIDEO: {str(e)}")
        traceback.print_exc() # Esto nos dirá la línea exacta del error startswith
        return {
            "error_message": f"Error en Agente de Ensamblaje: {str(e)}",
            "status": "failed",
            "video_url": None
        }