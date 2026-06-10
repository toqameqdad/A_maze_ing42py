import random


class Cell:
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.grid = self._create_grid()

    def _create_grid(self) -> list[list[Cell]]:
        return [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []

        if y > 0:
            neighbors.append((x, y - 1))

        if x < self.width - 1:
            neighbors.append((x + 1, y))

        if y < self.height - 1:
            neighbors.append((x, y + 1))

        if x > 0:
            neighbors.append((x - 1, y))

        return neighbors

    def remove_wall(
        self,
        current_x: int,
        current_y: int,
        next_x: int,
        next_y: int,
    ) -> None:
        current = self.grid[current_y][current_x]
        next_cell = self.grid[next_y][next_x]

        if next_x == current_x + 1:
            current.east = False
            next_cell.west = False

        elif next_x == current_x - 1:
            current.west = False
            next_cell.east = False

        elif next_y == current_y + 1:
            current.south = False
            next_cell.north = False

        elif next_y == current_y - 1:
            current.north = False
            next_cell.south = False

    def generate_maze(self) -> None:
        stack: list[tuple[int, int]] = []

        current_x = 0
        current_y = 0

        self.grid[current_y][current_x].visited = True
        stack.append((current_x, current_y))

        while stack:
            current_x, current_y = stack[-1]

            neighbors = self.get_neighbors(current_x, current_y)

            unvisited_neighbors = [
                (x, y)
                for x, y in neighbors
                if not self.grid[y][x].visited
            ]

            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)

                self.remove_wall(current_x, current_y, next_x, next_y)

                self.grid[next_y][next_x].visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()


if __name__ == "__main__":
    maze = MazeGenerator(3, 3, seed=42)
    maze.generate_maze()

    print(maze.grid[0][0].north)
    print(maze.grid[0][0].east)
    print(maze.grid[0][0].south)
    print(maze.grid[0][0].west)
