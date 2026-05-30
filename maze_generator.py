class Cell:
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = self._create_grid()

    def _create_grid(self) -> list[list[Cell]]:
        return [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]
