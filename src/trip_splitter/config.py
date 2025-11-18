# src/trip_splitter/config.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import toml

CONFIG_DIR = Path.home() / ".trip_splitter"
CONFIG_PATH = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG: Dict[str, Any] = {
    "mongo": {
        "uri": "",
        "db_name": "Trips",
    }
}


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_file_config() -> Dict[str, Any]:
    """
    Load config from ~/.trip_splitter/config.toml if it exists,
    otherwise return a copy of DEFAULT_CONFIG.
    """
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()
    data = toml.load(CONFIG_PATH)
    # merge shallowly with defaults so we always have mongo/db_name
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(data)
    if "mongo" in data:
        cfg["mongo"].update(data["mongo"])
    return cfg


def save_config(config: Dict[str, Any]) -> None:
    ensure_config_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def get_config(st_secrets=None) -> Dict[str, Any]:
    """
    Final config resolution order:
    1. Local file (~/.trip_splitter/config.toml)
    2. Environment variables
       - TRIP_SPLITTER_MONGO_URI
       - TRIP_SPLITTER_DB_NAME
    3. Streamlit secrets (if provided)
       st.secrets["mongo"]["uri"], ["db_name"]
    """
    cfg = load_file_config()

    # 1) ENV vars
    env_uri = os.getenv("TRIP_SPLITTER_MONGO_URI")
    env_db = os.getenv("TRIP_SPLITTER_DB_NAME")

    if env_uri:
        cfg["mongo"]["uri"] = env_uri
    if env_db:
        cfg["mongo"]["db_name"] = env_db

    # 2) Streamlit secrets
    if st_secrets is not None and "mongo" in st_secrets:
        mongo_sec = st_secrets["mongo"]
        if "uri" in mongo_sec:
            cfg["mongo"]["uri"] = mongo_sec["uri"]
        if "db_name" in mongo_sec:
            cfg["mongo"]["db_name"] = mongo_sec["db_name"]

    return cfg
