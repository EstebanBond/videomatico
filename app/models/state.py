from typing import List, TypedDict, Optional
from pydantic import BaseModel, Field

# 1. Esquema de una Escena (Lo que Gemini debe inventar)
class SceneSchema(BaseModel):
    num: int = Field(description="Número de la escena")
    image_prompt: str = Field(description="Prompt visual para generar la imagen de lujo")
    voiceover_text: str = Field(description="Texto que dirá la voz en off")
    overlay_text: str = Field(description="Palabra clave minimalista para la pantalla")

# 2. Esquema del Proyecto Completo
class VideoProjectSchema(BaseModel):
    brand_name: str = "esentia"
    concept: str = Field(description="Concepto creativo de la campaña")
    scenes: List[SceneSchema] = Field(description="Lista de las 5 escenas del video")

# 3. El Estado del Grafo (Lo que viaja entre nodos)
class GraphState(TypedDict):
    # Datos de entrada y creatividad
    project_data: Optional[VideoProjectSchema]
    
    # Rutas de archivos generados
    image_paths: List[str]
    audio_path: Optional[str]
    video_url: Optional[str] 
    
    # Control de flujo
    error_message: Optional[str]
    status: str