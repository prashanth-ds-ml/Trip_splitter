# src/trip_splitter/config.py
from __future__ import annotations

from typing import Any, Dict


def get_config(st_secrets) -> Dict[str, Any]:
    """
    Load config ONLY from Streamlit secrets (or a similar mapping).

    Supported formats in secrets.toml:

    1) Nested (recommended on Streamlit Cloud):

       [mongo]
       uri = "mongodb+srv://user:pass@cluster.mongodb.net/"
       db_name = "Trips"

    2) Flat (also supported):

       mongo_uri = "mongodb+srv://user:pass@cluster.mongodb.net/"
       mongo_db_name = "Trips"
    """
    if st_secrets is None:
        raise RuntimeError(
            "No Streamlit secrets found. "
            "Please configure MongoDB credentials in Streamlit secrets."
        )

    cfg: Dict[str, Any] = {"mongo": {"uri": "", "db_name": "Trips"}}

    # Preferred nested structure
    if "mongo" in st_secrets:
        mongo_sec = st_secrets["mongo"]
        if "uri" in mongo_sec:
            cfg["mongo"]["uri"] = mongo_sec["uri"]
        if "db_name" in mongo_sec:
            cfg["mongo"]["db_name"] = mongo_sec["db_name"]

    # Also support flat keys
    if "mongo_uri" in st_secrets:
        cfg["mongo"]["uri"] = st_secrets["mongo_uri"]
    if "mongo_db_name" in st_secrets:
        cfg["mongo"]["db_name"] = st_secrets["mongo_db_name"]

    if not cfg["mongo"]["uri"]:
        raise RuntimeError(
            "MongoDB URI not found in Streamlit secrets. "
            "Expected either [mongo].uri or mongo_uri."
        )

    return cfg
