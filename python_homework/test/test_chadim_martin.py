from pathlib import Path

from python_homework.year_2021.chadim_martin.aoc202101 import part1 as day_01_part1, part2 as day_01_part2
from python_homework.year_2021.chadim_martin.aoc202102 import part1 as day_02_part1, part2 as day_02_part2

PUZZLE_DIR = Path(__file__).parent.parent


def test_day01_input1():
    puzzle_input = Path(PUZZLE_DIR / "year_2021/aoc202101_part1.txt").read_text().strip()
    assert day_01_part1(puzzle_input) == 1462


def test_day01_input2():
    puzzle_input = Path(PUZZLE_DIR / "year_2021/aoc202101_part2.txt").read_text().strip()
    assert day_01_part2(puzzle_input) == 1497


def test_day02_input1():
    puzzle_input = Path(PUZZLE_DIR / "year_2021/aoc202102_part1.txt").read_text().strip()
    assert day_02_part1(puzzle_input) == 1815044


def test_day02_input2():
    puzzle_input = Path(PUZZLE_DIR / "year_2021/aoc202102_part2.txt").read_text().strip()
    assert day_02_part2(puzzle_input) == 1739283308
