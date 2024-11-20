from pathlib import Path


def parse(file_data: str) -> list:
    """Parse input."""
    return file_data.split("\n")  # note: you might want to change this


def part1(file_data: str):
    """Solve part 1."""
    input = parse(file_data)
    fuel_list = []
    for mass in input:
        fuel = int(mass) // 3 - 2
        fuel_list.append(fuel)
    return sum(fuel_list)


def calculate_fuel(mass: int) -> int:
    if mass <= 0:
        return 0
    else:
        fuel = mass // 3 - 2
        if fuel <= 0:
            return 0

        fuel += calculate_fuel(fuel)
        return fuel


def part2(file_data: str):
    """Solve part 2."""
    input = parse(file_data)
    fuel_list = []
    for mass in input:
        fuel_list.append(calculate_fuel(int(mass)))
    return sum(fuel_list)


if __name__ == "__main__":
    PUZZLE_DIR = Path(__file__).parent

    puzzle_input = (PUZZLE_DIR / "input1.txt").read_text().strip()
    print(f"part1: {part1(puzzle_input)}")

    puzzle_input = (PUZZLE_DIR / "input2.txt").read_text().strip()
    print(f"part2: {part2(puzzle_input)}")
