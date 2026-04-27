import sys
import time


def play(frames: list[tuple[list[str], float]]) -> None:
    _hide_cursor()
    _save_cursor()
    try:
        for lines, pause in frames:
            _render(lines)
            if pause:
                time.sleep(pause)
        time.sleep(0.4)
        _clear_screen()
    except KeyboardInterrupt:
        _clear_screen()
    finally:
        _restore_cursor()
        _show_cursor()


def _render(lines: list[str]) -> None:
    _clear_screen()
    sys.stdout.write('\n'.join(lines) + '\n')
    sys.stdout.flush()


def _clear_screen() -> None:
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


def _save_cursor() -> None:
    sys.stdout.write('\033[s')
    sys.stdout.flush()


def _restore_cursor() -> None:
    sys.stdout.write('\033[u')
    sys.stdout.flush()


def _hide_cursor() -> None:
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()


def _show_cursor() -> None:
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()
