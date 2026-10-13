"""CLI bootstrap. `beat-studio <command>` enters here."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from beatstudio import __version__
from beatstudio.host.bootstrap import HostBootstrap
from beatstudio.utils.logging import configure_logging

app = typer.Typer(no_args_is_help=True, add_completion=False)
plugins_app = typer.Typer(no_args_is_help=True, help="Inspect and manage generator plugins.")
app.add_typer(plugins_app, name="plugins")

_console = Console()


@app.command()
def version() -> None:
    """Print host version and detected audio backend."""
    _console.print(f"ai-beat-instrumental-studio [bold]{__version__}[/bold]")


@app.command()
def render(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Text prompt for the beat."),
    bpm: int = typer.Option(92, "--bpm"),
    bars: int = typer.Option(16, "--bars"),
    seed: int = typer.Option(6767, "--seed"),
    out: Path = typer.Option(Path("renders/take.wav"), "--out"),
) -> None:
    """Render an instrumental take from a prompt."""
    boot = HostBootstrap.from_config()
    boot.render(prompt=prompt, bpm=bpm, bars=bars, seed=seed, out=out)


@plugins_app.command("list")
def plugins_list() -> None:
    """List plugins the loader resolved."""
    boot = HostBootstrap.from_config()
    for spec in boot.registry.specs():
        state = "on" if spec.enabled else "off"
        _console.print(f"[{state}] {spec.id:<18} {spec.module}")


def main() -> None:
    configure_logging()
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()