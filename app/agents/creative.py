import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import GraphState, VideoProjectSchema

# Inicializamos modelo de LangChain

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Configuramos LLM para JSON estructurado
structured_llm = llm.with_structured_output(VideoProjectSchema)

async def creative_node(state: GraphState):
    print("🧠 Agente Creativo: Diseñando la campaña de esentia...")
    
    prompt = """
    Actúa como Director Creativo para 'esentia'. 
    
    IMPORTANTE PARA LA SEGURIDAD:
    - No uses palabras que puedan interpretarse como contenido sensual o humano explícito.
    - Enfócate en objetos: botellas de perfume, madera de cedro, texturas de cuero, luz ambiental.
    - Evita mencionar personas, partes del cuerpo, o términos que puedan interpretarse como provocativos.
    - Describe solo objetos inanimados: 'superficie de cuero sintético oscuro', 'bloque de madera tallada', 'frasco de cristal ahumado'.
    - Enfócate en objetos (perfumes, relojes, cristalería), iluminación dramática y texturas como mármol, seda o metal.
    - Usa 'iluminación de estudio' y 'estética de bodegón publicitario'.
    - Los image_prompts deben ser puramente descriptivos de arquitectura y diseño de interiores.
    
    Tu misión es diseñar un video vertical de 5 escenas para un video de fragancias de lujo, que evoque:
    - Notas olfativas: Cuero premium y maderas nobles (cedro, sándalo).
    - Estética: Lujo minimalista, espacios despejados, iluminación cinemática.
    - Emoción: Calma, exclusividad y sofisticación.

    Instrucciones específicas:
    - Escena 1: Introducción de marca.
    - Escenas 2-4: Transición entre texturas (cuero/madera) y el producto.
    - Escena 5: Cierre con la frase "Los detalles viven en el alma".

    PARA CADA ESCENA DEBES GENERAR:
    1. image_prompt: Descripción fotorealista de lujo minimalista.
    2. voiceover_text: El guion breve y elegante.
    3. overlay_text: Una SOLA palabra poderosa (ej: ESENCIA, ALMA, PUREZA) 
        que aparecerá en pantalla. Máximo 12 caracteres.
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