# src/trip_splitter/cli.py
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer(help="Trip Splitter CLI")


@app.command()
def run() -> None:
    """
    Run the Trip Splitter Streamlit app.

    Note:
      MongoDB credentials are ONLY read from Streamlit secrets:
      - On Streamlit Cloud: app secrets
      - Locally (optional): .streamlit/secrets.toml
    """
    app_path = Path(__file__).with_name("app.py")

    if not app_path.exists():
        typer.secho(f"Could not find app.py at {app_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            check=False,
        )
    except FileNotFoundError:
        typer.secho(
            "Error: streamlit not found. Install it with `pip install streamlit`.",
            fg=typer.colors.RED,
        )
