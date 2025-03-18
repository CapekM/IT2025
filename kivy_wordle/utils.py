from enum import StrEnum
from pathlib import Path
from typing import Final

GREEN_COLOR: Final[str] = "03fc1c"
YELLOW_COLOR: Final[str] = "fcc603"
BLACK_COLOR: Final[str] = "000000"


class GamePages(StrEnum):
    WELCOME = "Welcome Page"
    GAME = "Game Page"
    OVER = "Over Page"
    SETTINGS = "Settings Page"


def get_similar_letter(couple_letters: list[tuple[str, str]], letter: str) -> str | None:
    for couple in couple_letters:
        if letter == couple[0]:
            return couple[1]
        elif letter == couple[1]:
            return couple[0]
    return None


def get_word_list() -> list[str]:
    words_file_path = Path(__file__).parent / "cz_words_5.txt"
    return [x.upper() for x in words_file_path.read_text(encoding="utf-8").strip().splitlines()]
