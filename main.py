import sys
from typing import TypeAlias
from pathlib import Path
from maze import Maze


ConfigValue: TypeAlias = int | str | bool | tuple[int, int]


def validate_config(config: dict[str, ConfigValue]) -> bool:
    """Validate the parsed configuration dictionary for the maze.

    Checks if all required keys are present, types are correct, and
    coordinates are within the logical boundaries of the maze.

    Args:
        config: A dictionary containing the configuration keys and values.

    Returns:
        True if the configuration is valid and safe to use, False otherwise.
    """
    required_keys = [
            "WIDTH", "HEIGHT", "ENTRY",
            "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required_keys:
        if key not in config:
            print(f"Error: Missing required configuration key: '{key}'")
            return False
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]
    output_file = config["OUTPUT_FILE"]

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
        print("config file does not exist!")
        return
    config: dict[str, ConfigValue] = {}
    with config_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print(f"Error: Invalid line format: '{line}'")
                return
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key in config:
                print(f"Error: Duplicate key found: '{key}'")
                return
            try:
                if key in ("WIDTH", "HEIGHT"):
                    config[key] = int(value)
                elif key in ("seed", "SEED"):
                    key = key.upper()
                    config[key] = int(value)
                elif key in ("ENTRY", "EXIT"):
                    x_str, y_str = value.split(",")
                    config[key] = (int(x_str), int(y_str))
                elif key == "PERFECT":
                    val_clean = value.lower()
                    if val_clean not in ("true", "false"):
                        raise ValueError
                    config[key] = val_clean == "true"
                else:
                    config[key] = value

            except (ValueError, IndexError):
                print(f"Error: Invalid value format for "
                      f"key '{key}' with value '{value}'")
                return
    if not validate_config(config):
        return
    seed_value = config.get("SEED", None)
    seed = Maze(config["WIDTH"], config["HEIGHT"]
                , config["PERFECT"], seed_value)
    seed.generate_maze(0, 0)
    seed.print_maze()
    while True:
        print("=== A-Maze-ing ===\n"
              "1. Re-generate a new maze\n"
              "2. Show/Hide path from entry to exit\n"
              "3. Rotate maze colors\n"
              "4. Quit\n")
        choice = input("Choice? (1-4): ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            seed.rotate_colors()
            seed.print_maze()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")



if __name__ == "__main__":
    main()
