from pathlib import Path

from python_homework.year_2020.musil_jakub.aoc202001 import part1 as day_01_part1, part2 as day_01_part2
from python_homework.year_2020.musil_jakub.aoc202002 import part1 as day_02_part1, part2 as day_02_part2

PUZZLE_DIR = Path(__file__).parent.parent


def test_day01_input1():
    puzzle_input = Path(PUZZLE_DIR / "year_2020/aoc202001_part1.txt").read_text().strip()
    assert day_01_part1(puzzle_input) == 32064


def test_day01_input2():
    puzzle_input = Path(PUZZLE_DIR / "year_2020/aoc202001_part2.txt").read_text().strip()
    assert day_01_part2(puzzle_input) == 193598720


def test_day02_input1():
    puzzle_input = Path(PUZZLE_DIR / "year_2020/aoc202002_part1.txt").read_text().strip()
    assert day_02_part1(puzzle_input) == 445


def test_day02_input2():
    puzzle_input = Path(PUZZLE_DIR / "year_2020/aoc202002_part2.txt").read_text().strip()
    assert day_02_part2(puzzle_input) == 491
