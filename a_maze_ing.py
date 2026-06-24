import sys
from pathlib import Path
from typing import TypeAlias

from maze_generator import MazeGenerator


ConfigValue: TypeAlias = int | str | bool | tuple[int, int]


def validate_config(config: dict[str, ConfigValue]) -> bool:
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]

    if not isinstance(width, int) or not isinstance(height, int):
        print("Error: WIDTH and HEIGHT must be integers")
        return False

    if not isinstance(entry, tuple) or not isinstance(exit_, tuple):
        print("Error: ENTRY and EXIT must be coordinates")
        return False

    entry_x, entry_y = entry
    exit_x, exit_y = exit_

    if width <= 0:
        print("Error: WIDTH must be greater than 0")
        return False

    if height <= 0:
        print("Error: HEIGHT must be greater than 0")
        return False

    if entry == exit_:
        print("Error: ENTRY and EXIT cannot be the same")
        return False

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print("Error: ENTRY is outside maze bounds")
        return False

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print("Error: EXIT is outside maze bounds")
        return False

    return True


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"Error: file not found: {config_path}")
        return

    config: dict[str, ConfigValue] = {}

    with config_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)

            if key in ("WIDTH", "HEIGHT", "SEED"):
                config[key] = int(value)
            elif key in ("ENTRY", "EXIT"):
                x, y = value.split(",")
                config[key] = (int(x), int(y))
            elif key == "PERFECT":
                val_clean = value.lower()
                if val_clean not in ("true", "false"):
                    raise ValueError
                config[key] = val_clean == "true"
            else:
                config[key] = value

    if not validate_config(config):
        return

    width = config["WIDTH"]
    height = config["HEIGHT"]
    seed = config.get("SEED")

    if not isinstance(width, int) or not isinstance(height, int):
        return

    if seed is not None and not isinstance(seed, int):
        print("Error: SEED must be an integer")
        return

    maze = MazeGenerator(width, height, seed)
    maze.generate_maze()

    print(f"Maze generated: {maze.width}x{maze.height}")
    print(f"Seed: {maze.seed}")


if __name__ == "__main__":
    main()
