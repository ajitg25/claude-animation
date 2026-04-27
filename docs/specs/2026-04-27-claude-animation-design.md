# claude-animation — Design Spec
_Date: 2026-04-27_

## Goal

A brew-installable Python CLI that plays terminal animations as full-screen ANSI overlays. V1 ships with one animation (whip). Press `Ctrl+W` in any terminal to crack the whip; terminal state is fully restored after.

---

## Architecture

```
claude-animation/
├── pyproject.toml
├── claude_animation/
│   ├── cli.py                  # Click entry point
│   ├── engine.py               # ANSI overlay: save cursor → play frames → restore
│   └── animations/
│       ├── __init__.py         # Animation registry
│       └── whip.py             # Whip frames
├── install.sh                  # Post-install: writes zsh keybinding
└── Formula/
    └── claude-animation.rb     # Homebrew formula
```

---

## Components

### CLI (`cli.py`)
Entry point registered in `pyproject.toml` as `claude-animation`.

| Command | Behaviour |
|---|---|
| `claude-animation whip` | Play whip overlay |
| `claude-animation list` | Print available animations |
| `claude-animation install` | Append `Ctrl+W` keybinding to `~/.zshrc` |

### Engine (`engine.py`)
1. Hide cursor (`\033[?25l`)
2. Save cursor position (`\033[s`)
3. Clear screen, render frames with `time.sleep` between them
4. Clear animation area
5. Restore cursor position (`\033[u`)
6. Show cursor (`\033[?25h`)

### Animation Registry (`animations/__init__.py`)
Dict mapping name → animation module. Adding a new animation = drop a file in `animations/` and register it. Each module exports `FRAMES: list[tuple[list[str], float]]`.

### Whip (`animations/whip.py`)
6 frames migrated from existing `~/.claude/scripts/whip_animation.py`. Frames: rest → windup → swing → extend → CRACK! → settle.

### Keybinding (`claude-animation install`)
Appends to `~/.zshrc`:
```zsh
# claude-animation
bindkey -s '^W' 'claude-animation whip\n'
```
Idempotent — checks for existing entry before writing.

---

## Distribution

- **Main repo:** `github.com/<user>/claude-animation` — tagged releases with `dist/` wheel
- **Tap repo:** `github.com/<user>/homebrew-claude-animation` — single `claude-animation.rb` formula
- **Install UX:**
  ```bash
  brew tap <user>/claude-animation
  brew install claude-animation
  claude-animation install   # sets up Ctrl+W
  ```

---

## Dependencies

| Dep | Why |
|---|---|
| `click` | CLI argument parsing |
| Python 3.9+ | f-strings, type hints |

No other runtime deps. `brew` handles Python.

---

## Out of Scope (V1)

- Always-visible sidebar panel
- Sound effects
- Windows / Linux
- More than one animation
