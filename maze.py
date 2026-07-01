import random


class Maze:
    def __init__(self, width: int, height: int, perfect: bool, seed: int):
        self._width = width
        self._height = height
        self._perfect = perfect
        self._seed = seed
        self.wall_color = "47"
        self.pattern_color = "42"
        if self._seed == None:
            random.seed()
        else:
            random.seed(self._seed)
        self._grid = []
        for row in range(self._height):
            current_row = []
            for colomn in range(self._width):
                current_row.append(15)
            self._grid.append(current_row)

        self._visited = []
        for row in range(self._height):
            current_row = []
            for colomn in range(self._width):
                current_row.append(False)
            self._visited.append(current_row)
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        if self._width > 7 and self._height > 5:
            start_x = (self._width - 7) // 2
            start_y = (self._height - 5) // 2
            for r in range(5):
                for c in range(7):
                    if pattern[r][c] == 1:
                        maze_x = start_x + c
                        maze_y = start_y + r
                        self._grid[maze_y][maze_x] = 15
                        self._visited[maze_y][maze_x] = True

    def _get_unvisited_neighbors(self, x: int, y: int) -> list[
            tuple[int, int, str]]:
        neighbors = []
        next_y = y - 1
        if next_y >= 0 and not self._visited[next_y][x]:
            neighbors.append((x, next_y, "N"))
        next_y = y + 1
        if next_y < self._height and not self._visited[next_y][x]:
            neighbors.append((x, next_y, "S"))
        next_x = x - 1
        if next_x >= 0 and not self._visited[y][next_x]:
            neighbors.append((next_x, y, "W"))
        next_x = x + 1
        if next_x < self._width and not self._visited[y][next_x]:
            neighbors.append((next_x, y, "E"))
        return neighbors

    def generate_maze(self, start_x: int, start_y: int) -> None:
        self._visited[start_y][start_x] = True
        stack = [(start_x, start_y)]
        while stack:
            curr_x, curr_y = stack[-1]
            neighbors = self._get_unvisited_neighbors(curr_x, curr_y)
            if neighbors:
                next_x, next_y, direction = random.choice(neighbors)
                if direction == "N":
                    self._grid[curr_y][curr_x] = self._grid[curr_y][curr_x] - 1
                    self._grid[next_y][next_x] = self._grid[next_y][next_x] - 4
                elif direction == "S":
                    self._grid[curr_y][curr_x] = self._grid[curr_y][curr_x] - 4
                    self._grid[next_y][next_x] = self._grid[next_y][next_x] - 1
                elif direction == "E":
                    self._grid[curr_y][curr_x] = self._grid[curr_y][curr_x] - 2
                    self._grid[next_y][next_x] = self._grid[next_y][next_x] - 8
                elif direction == "W":
                    self._grid[curr_y][curr_x] = self._grid[curr_y][curr_x] - 8
                    self._grid[next_y][next_x] = self._grid[next_y][next_x] - 2
                self._visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
        if not self._perfect:
            for row in range(self._height):
                for colomn in range(self._width):
                    if random.random() <= 0.2 and (colomn + 1) < self._width:
                        ####### we need edit here to make the maze 42 and not to break it 
                        if (
                                (self._grid[row][colomn] & 2) != 0
                                and (self._grid[row][colomn + 1] & 8) != 0):
                            self._grid[row][colomn] -= 2
                            self._grid[row][colomn + 1] -= 8
                            if self._is_3x3(row, colomn):
                                self._grid[row][colomn] += 2
                                self._grid[row][colomn + 1] += 8

    def _is_3x3(self, row: int, colomn: int) -> bool:
        if self._height <= 3 or self._width <= 3:
            return False
        if row + 2 >= self._height or colomn + 2 >= self._width:
            return False
        for j in range(2):
            for i in range(3):
                if ((self._grid[row + j][colomn + i] & 4) != 0):
                    return False
        for j in range(3):
            for i in range(2):
                if ((self._grid[row + j][colomn + i] & 2) != 0):
                    return False
        return True

    def rotate_colors(self):
        colors = ["47", "41", "42", "43", "44", "45", "46"]
        self.wall_color = random.choice(colors)
        self.pattern_color = random.choice(colors)

    def print_maze(self):
        WALL = f"\033[{self.wall_color}m \033[0m"
        PATH = "  "
        print(WALL * ((self._width * 3) + 1))
        for r in range(self._height):
            row_str = WALL
            col_str = WALL
            for c in range(self._width):
                row_str += PATH

                if self._grid[r][c] & 2 != 0:
                    row_str += WALL
                else:
                    row_str += " "

                if self._grid[r][c] & 4 != 0:
                    col_str += WALL * 3
                else:
                    col_str += PATH + WALL

            print(row_str)
            print(col_str)
