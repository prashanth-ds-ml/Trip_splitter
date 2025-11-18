# src/trip_splitter/cli.py
from __future__ import annotations

import subprocess
import sys
from typing import Optional

import typer

from .config import load_file_config, save_config, CONFIG_PATH

app = typer.Typer(help="Trip Splitter CLI")


@app.command()
def init() -> None:
    """
    Interactive setup: configure MongoDB URI + DB name
    and save to ~/.trip_splitter/config.toml
    """
    cfg = load_file_config()

    typer.echo(f"Config file: {CONFIG_PATH}")

    current_uri = cfg["mongo"].get("uri", "")
    current_db = cfg["mongo"].get("db_name", "Trips")

    uri = typer.prompt(
        "Enter your MongoDB URI (e.g. mongodb+srv://user:pass@cluster/...)",
        default=current_uri,
    )
    db_name = typer.prompt(
        "Enter MongoDB database name",
        default=current_db,
    )

    cfg["mongo"]["uri"] = uri
    cfg["mongo"]["db_name"] = db_name

    save_config(cfg)
    typer.secho("✅ Configuration saved.", fg=typer.colors.GREEN)


@app.command()
def run() -> None:
    """
    Run the Trip Splitter Streamlit app.
    """
    # Use streamlit CLI; assumes 'streamlit' is in PATH
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "-m", "trip_splitter.app"],
            check=False,
        )
    except FileNotFoundError:
        typer.secho(
            "Error: streamlit not found. Install it with `pip install streamlit`.",
            fg=typer.colors.RED,
        )
