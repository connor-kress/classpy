import os


def clear_screen() -> None:
    """Clears the running terminal's screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
