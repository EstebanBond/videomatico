import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import GraphState, VideoProjectSchema

# Inicializamos Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,  # Un toque de creatividad sin perder el control
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Configuramos LLM -  formato JSON
structured_llm = llm.with_structured_output(VideoProjectSchema)

async def creative_node(state: GraphState):
    print("Agente Creativo: Diseñando la campaña de esentia...")
    
    prompt = f"""
    Actúa como un Director Creativo Senior para 'esentia', una marca de lujo de fragancias ambientales.
    
    Tu misión es diseñar un video vertical de 5 escenas que evoque:
    - Notas olfativas: Cuero premium y maderas nobles (cedro, sándalo).
    - Estética: Lujo minimalista, espacios despejados, iluminación cinemática.
    - Emoción: Calma, exclusividad y sofisticación.

    Instrucciones específicas:
    - Escena 1: Introducción de marca.
    - Escenas 2-4: Transición entre texturas (cuero/madera) y el producto.
    - Escena 5: Cierre con la frase "Los detalles viven en el alma".

    Asegúrate de que los image_prompts sean detallados y de estilo fotorealista 4k.
    """

    try:
        # Ejecución asíncrona antibloqueo
        response = await structured_llm.ainvoke(prompt)
        
        # Actualizamos el estado con la creatividad generada
        return {
            "project_data": response,
            "status": "creative_script_generated"
        }
    except Exception as e:
        return {
            "error_message": f"Error en Agente Creativo: {str(e)}",
            "status": "failed"
        }