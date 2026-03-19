import os
from typing import List

def get_memory_tool(agent_id: str, query: str) -> List[str]:
    """
    A tool used by agents during simulation to search their own local memory.
    Replaces the cloud search tool.
    """
    from .zep_graph_memory_updater import retrieve_relevant_context
    
    # We call our newly created local retrieval function
    memories = retrieve_relevant_context(agent_id, query)
    
    if not memories:
        return ["No relevant past trading memories found."]
    
    return memories[0] # Returns the most relevant historical text

def clear_simulation_state():
    """Wipes the local memory to start a new market prediction run."""
    from .zep_graph_memory_updater import client
    try:
        client.delete_collection(name="market_simulation_graph")
        return "Local simulation memory cleared successfully."
    except:
        return "No collection found to clear."
