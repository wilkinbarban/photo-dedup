import os
import json
import logging
import platform
from pathlib import Path
from datetime import datetime

# Determine the application data directory based on the operating system
# This ensures that configuration, cache, and history files are stored in the
# appropriate user-specific data folder rather than cluttering the working directory.
app_name = "PhotoDedup"

if platform.system() == "Windows":
    # On Windows, use the %APPDATA% environment variable.
    # Example: C:\Users\Username\AppData\Roaming\PhotoDedup
    app_data_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
elif platform.system() == "Darwin":
    # On macOS, use the standard ~/Library/Application Support directory.
    # Example: /Users/Username/Library/Application Support/PhotoDedup
    app_data_dir = Path.home() / "Library" / "Application Support" / app_name
else:
    # On Linux and other UNIX-like systems, use a hidden folder in the home directory.
    # Example: /home/username/.photodedup
    app_data_dir = Path.home() / f".{app_name.lower()}"

# Create the data directory if it does not exist already.
# parents=True ensures that any missing parent directories are also created.
# exist_ok=True prevents an error if the directory already exists.
app_data_dir.mkdir(parents=True, exist_ok=True)

# Define full paths for the application's data files
CACHE_FILE = app_data_dir / 'photo_dedup_cache.json'
CONFIG_FILE = app_data_dir / 'photo_dedup_config.json'
HISTORY_FILE = app_data_dir / 'photo_dedup_history.json'
EMBEDDINGS_CACHE_FILE = app_data_dir / 'photo_dedup_embeddings.pkl'

import pickle

def load_embeddings_cache() -> dict:
    """Loads the AI embeddings cache."""
    try:
        if EMBEDDINGS_CACHE_FILE.exists():
            with open(EMBEDDINGS_CACHE_FILE, 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        logging.error(f"Error loading embeddings cache: {e}")
    return {}

def save_embeddings_cache(cache: dict) -> None:
    """Saves the AI embeddings cache."""
    try:
        with open(EMBEDDINGS_CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)
    except Exception as e:
        logging.error(f"Error saving embeddings cache: {e}")

def load_cache() -> dict:
    """
    Loads the photo analysis cache from the JSON cache file.
    The cache stores previously computed hashes and metadata to speed up future scans.
    
    Returns:
        dict: A dictionary containing cached photo data. Returns an empty dict if the file 
              does not exist or if an error occurs during reading.
    """
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading cache: {e}")
    return {}

def save_cache(cache: dict) -> None:
    """
    Saves the current photo analysis cache to the JSON cache file.
    
    Args:
        cache (dict): The dictionary containing the photo metadata to be saved.
    """
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            # indent=2 formats the JSON for human readability
            json.dump(cache, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving cache: {e}")

def load_config() -> dict:
    """
    Loads user preferences and settings from the configuration file.
    
    Returns:
        dict: A dictionary containing the configuration settings. If the file is missing 
              or corrupted, it returns a set of default configuration values.
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {e}")
    # Return default settings if the file cannot be loaded
    return {"theme": "dark", "duplicate_mode": "similar", "auto_backup": True}

def save_config(config: dict) -> None:
    """
    Saves user preferences and settings to the configuration file.
    
    Args:
        config (dict): The dictionary containing the configuration to be saved.
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving config: {e}")

def log_history(action: str, details: dict) -> None:
    """
    Logs user actions (such as moving or deleting duplicate photos) to the history file.
    This allows the application to keep an audit trail of changes made to the user's files.
    
    Args:
        action (str): A string describing the action performed (e.g., 'move', 'delete').
        details (dict): A dictionary containing metadata about the action (e.g., file paths, groups).
    """
    try:
        history = []
        # Load existing history if the file is present
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # Append the new action with a timestamp
        history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })
        
        # Save the updated history back to the file
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Error logging history: {e}")

def load_history() -> list:
    """
    Retrieves the entire action history from the JSON history file.
    
    Returns:
        list: A list of dictionaries representing the logged actions. Returns an empty list 
              if no history is found or an error occurs.
    """
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading history: {e}")
    return []
