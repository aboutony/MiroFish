import json
import random
import os

# Updated path to point to our new market archetypes
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/persona_templates.json")

def load_archetypes():
    """Loads the trading behaviors we defined in the JSON file."""
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)["market_archetypes"]
    except Exception as e:
        # Fallback in case of path issues during initialization
        return [{
            "role": "Standard Trader",
            "risk_tolerance": "Medium",
            "behavior": "Balanced approach to market news.",
            "influence_weight": 0.5
        }]

def generate_market_agent_profile(agent_id: int):
    """
    Spawns a new agent with a specific trading personality.
    Replaces generic personas with Stock Market archetypes.
    """
    archetypes = load_archetypes()
    # Randomly assign a role to create a diverse market "crowd"
    profile = random.choice(archetypes)
    
    return {
        "id": agent_id,
        "name": f"Trader_{agent_id}",
        "role": profile["role"],
        "traits": {
            "risk_tolerance": profile["risk_tolerance"],
            "strategy": profile["behavior"]
        },
        "influence": profile["influence_weight"],
        "memory_window": "10_rounds"
    }

def batch_spawn_market(count=50):
    """Creates a full 'Trading Floor' of agents for the simulation."""
    return [generate_market_agent_profile(i) for i in range(count)]
