# claude-animation

Terminal animations, brew-installable. V1: crack a whip.

## Install

```bash
brew tap ajitg25/claude-animation
brew install claude-animation
claude-animation install   # sets up Ctrl+W in ~/.zshrc
```

## Usage

```bash
claude-animation whip      # crack the whip
claude-animation list       # list animations
```

Or press `Ctrl+W` in any terminal after running `install`.

## Adding animations

Drop a file in `claude_animation/animations/`, export `FRAMES: list[tuple[list[str], float]]`, and register it in `animations/__init__.py`.
