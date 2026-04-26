import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'account.json')

def load_data():
    """Loads accounts from the JSON file."""
    if not os.path.exists(DATA_FILE):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        # Create empty dictionary if file doesn't exist
        save_data({})
        return {}
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data):
    """Saves the data dictionary to the JSON file."""
    # Ensure directory exists before saving setup
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
