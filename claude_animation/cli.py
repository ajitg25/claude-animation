import sys
from pathlib import Path

import click

from claude_animation import __version__
from claude_animation.animations import REGISTRY
from claude_animation import engine

ZSHRC = Path.home() / '.zshrc'
KEYBINDING_MARKER = '# claude-animation'
KEYBINDING = f'\n{KEYBINDING_MARKER}\nbindkey -s \'^W\' \'claude-animation whip\\n\'\n'


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Terminal animations — crack a whip and more."""


@main.command()
def whip() -> None:
    """Crack the whip."""
    engine.play(REGISTRY['whip'])


@main.command(name='list')
def list_animations() -> None:
    """List all available animations."""
    for name in REGISTRY:
        click.echo(f'  {name}')


@main.command()
def install() -> None:
    """Add Ctrl+W keybinding to ~/.zshrc."""
    content = ZSHRC.read_text() if ZSHRC.exists() else ''
    if KEYBINDING_MARKER in content:
        click.echo('Keybinding already installed in ~/.zshrc')
        return
    with ZSHRC.open('a') as f:
        f.write(KEYBINDING)
    click.echo('Done. Restart your terminal or run:  source ~/.zshrc')
    click.echo('Then press Ctrl+W to crack the whip.')
