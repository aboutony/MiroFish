import os
import chromadb
from chromadb.config import Settings
from datetime import datetime

# Initialize the local ChromaDB client using the settings from your .env
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_SERVER_HTTP_PORT", 8000))

# Connect to the local database container
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

def get_collection(name="market_simulation_graph"):
    """Fetches or creates a local vector collection for agent state."""
    return client.get_or_create_collection(name=name)

def update_agent_graph_memory(agent_id, interaction_summary, importance=1):
    """
    Updates the local memory of an agent after a trading simulation round.
    Replaces the original Zep Cloud updater logic.
    """
    collection = get_collection()
    timestamp = datetime.now().isoformat()
    
    collection.add(
        documents=[interaction_summary],
        metadatas=[{
            "agent_id": str(agent_id), 
            "timestamp": timestamp,
            "type": "trading_action",
            "importance": importance
        }],
        ids=[f"agent_{agent_id}_{timestamp}"]
    )
    return f"Local graph memory updated for Agent {agent_id}."

def retrieve_relevant_context(agent_id, query, n_results=3):
    """
    Retrieves past memories to help the agent make a localized decision.
    """
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        where={"agent_id": str(agent_id)},
        n_results=n_results
    )
    return results['documents']
