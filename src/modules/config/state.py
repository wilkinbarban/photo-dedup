import json
import os
import logging
import platform
import pickle
from pathlib import Path
from datetime import datetime

app_name = "PhotoDedup"

if platform.system() == "Windows":
    app_data_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
elif platform.system() == "Darwin":
    app_data_dir = Path.home() / "Library" / "Application Support" / app_name
else:
    app_data_dir = Path.home() / f".{app_name.lower()}"

app_data_dir.mkdir(parents=True, exist_ok=True)

CACHE_FILE = app_data_dir / 'photo_dedup_cache.json'
CONFIG_FILE = app_data_dir / 'photo_dedup_config.json'
HISTORY_FILE = app_data_dir / 'photo_dedup_history.json'
EMBEDDINGS_CACHE_FILE = app_data_dir / 'photo_dedup_embeddings.pkl'


def load_embeddings_cache() -> dict:
    """Loads the AI embeddings cache."""
    try:
        if EMBEDDINGS_CACHE_FILE.exists():
            with open(EMBEDDINGS_CACHE_FILE, 'rb') as file_handle:
                cache = pickle.load(file_handle)
                if isinstance(cache, dict):
                    return cache
                logging.warning("Embeddings cache has invalid shape; starting with an empty cache.")
    except Exception as error:
        logging.warning("Error loading embeddings cache from %s: %s", EMBEDDINGS_CACHE_FILE, error, exc_info=True)
    return {}


def save_embeddings_cache(cache: dict) -> None:
    """Saves the AI embeddings cache."""
    try:
        with open(EMBEDDINGS_CACHE_FILE, 'wb') as file_handle:
            pickle.dump(cache, file_handle)
    except Exception as error:
        logging.warning("Error saving embeddings cache to %s: %s", EMBEDDINGS_CACHE_FILE, error, exc_info=True)


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
            with open(CACHE_FILE, 'r', encoding='utf-8') as file_handle:
                cache = json.load(file_handle)
                if isinstance(cache, dict):
                    return cache
                logging.warning("Photo cache has invalid shape; starting with an empty cache.")
    except Exception as error:
        logging.warning("Error loading cache from %s: %s", CACHE_FILE, error, exc_info=True)
    return {}


def save_cache(cache: dict) -> None:
    """
    Saves the current photo analysis cache to the JSON cache file.

    Args:
        cache (dict): The dictionary containing the photo metadata to be saved.
    """
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as file_handle:
            json.dump(cache, file_handle, indent=2)
    except Exception as error:
        logging.warning("Error saving cache to %s: %s", CACHE_FILE, error, exc_info=True)


def load_config() -> dict:
    """
    Loads user preferences and settings from the configuration file.

    Returns:
        dict: A dictionary containing the configuration settings. If the file is missing
              or corrupted, it returns a set of default configuration values.
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file_handle:
                config = json.load(file_handle)
                if isinstance(config, dict):
                    return config
                logging.warning("Config file has invalid shape; using defaults.")
    except Exception as error:
        logging.warning("Error loading config from %s: %s", CONFIG_FILE, error, exc_info=True)
    return {"theme": "dark", "duplicate_mode": "similar", "auto_backup": True}


def save_config(config: dict) -> None:
    """
    Saves user preferences and settings to the configuration file.

    Args:
        config (dict): The dictionary containing the configuration to be saved.
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file_handle:
            json.dump(config, file_handle, indent=2)
    except Exception as error:
        logging.warning("Error saving config to %s: %s", CONFIG_FILE, error, exc_info=True)


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
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as file_handle:
                history = json.load(file_handle)
                if not isinstance(history, list):
                    logging.warning("History file has invalid shape; starting a new history list.")
                    history = []

        history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        })

        with open(HISTORY_FILE, 'w', encoding='utf-8') as file_handle:
            json.dump(history, file_handle, indent=2)
    except Exception as error:
        logging.warning("Error logging history to %s: %s", HISTORY_FILE, error, exc_info=True)


def load_history() -> list:
    """
    Retrieves the entire action history from the JSON history file.

    Returns:
        list: A list of dictionaries representing the logged actions. Returns an empty list
              if no history is found or an error occurs.
    """
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as file_handle:
                history = json.load(file_handle)
                if isinstance(history, list):
                    return history
                logging.warning("History file has invalid shape; returning an empty history.")
    except Exception as error:
        logging.warning("Error loading history from %s: %s", HISTORY_FILE, error, exc_info=True)
    return []
