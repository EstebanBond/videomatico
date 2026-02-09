from langgraph.graph import StateGraph, END
from app.models.state import GraphState
from app.agents.creative import creative_node
from app.agents.media import media_node
from app.agents.assembler import assembler_node

# 1. Definimos la estructura del grafo
workflow = StateGraph(GraphState)

# 2. Añadimos nuestros nodos (Agentes)
workflow.add_node("director_creativo", creative_node)
workflow.add_node("generador_medios", media_node)
workflow.add_node("ensamblador_final", assembler_node)

# 3. Conectamos los puntos (Flujo de trabajo)
workflow.set_entry_point("director_creativo")
workflow.add_edge("director_creativo", "generador_medios")
workflow.add_edge("generador_medios", "ensamblador_final")
workflow.add_edge("ensamblador_final", END)

# 4. Compilamos el grafo
esentia_graph = workflow.compile()