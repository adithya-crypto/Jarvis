import json
import os

MEMORY_FILE = "memory/user_profile.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_memory_to_file(memory_data):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_data, f, indent=4)

def remember(key, value):
    """Save a piece of information to memory."""
    memory = load_memory()
    memory[key] = value
    save_memory_to_file(memory)
    return f"I've remembered that {key} is {value}."

def recall(key):
    """Retrieve a piece of information from memory."""
    memory = load_memory()
    value = memory.get(key)
    if value:
        return f"You told me that {key} is {value}."
    else:
        return f"I don't have any information about {key}."
