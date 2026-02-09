import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import GraphState, VideoProjectSchema

# Inicializamos modelo de LangChain

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Configuramos LLM para JSON estructurado
structured_llm = llm.with_structured_output(VideoProjectSchema)

async def creative_node(state: GraphState):
    print("🧠 Agente Creativo: Diseñando la campaña de esentia...")
    
    prompt = """
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
        # Ejecución asíncrona
        response = await structured_llm.ainvoke(prompt)
        
        print("✅ Guion generado exitosamente por Gemini.")
        return {
            "project_data": response,
            "status": "creative_script_generated"
        }
    except Exception as e:
        print(f"❌ Error en Gemini: {str(e)}")
        return {
            "project_data": None, 
            "status": "failed"
        }