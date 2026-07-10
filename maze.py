import random
import shutil
from collections import deque


class Maze:
    def __init__(self, width: int, height: int, perfect: bool, seed: int):
        self._width = width
        self._height = height
        self._perfect = perfect
        self._seed = seed
        self.wall_color = "47"
        self.pattern_color = "42"
        self._show_path = False
        self.path_color = "46"
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
        self._pattern_cells = set()
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
                        self._pattern_cells.add((maze_x, maze_y))

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

        for c, r in self._pattern_cells:
            self._visited[r][c] = True
            self._grid[r][c] = 15
            
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
                        if (
                                (self._grid[row][colomn] & 2) != 0
                                and (self._grid[row][colomn + 1] & 8) != 0
                                and self._grid[row][colomn + 1] != 15
                                and self._grid[row][colomn] != 15):
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
        colors = ["47", "41", "42", "43", "44", "45", "46", "47", "100", "101", "102", "103", "104", "105", "106"]
        self.wall_color = random.choice(colors)
        self.pattern_color = random.choice(colors)
        self.path_color = random.choice(colors)

    def print_maze(self):
        WALL = f"\033[{self.wall_color}m \033[0m"
        PATTERN = f"\033[{self.pattern_color}m \033[0m"
        PATH = f"\033[{self.path_color}m   \033[0m"
        ENTRY = "\033[45m   \033[0m"   # بنفسجي
        EXIT = "\033[41m   \033[0m"    # أحمر

    # السقف
        top = WALL
        for _ in range(self._width):
            top += WALL * 3 + WALL
        print(top)

        for r in range(self._height):

            middle = WALL
            bottom = WALL

            for c in range(self._width):

                wall_char = WALL

            # محتوى الخلية
                if hasattr(self, "_entry") and (c, r) == self._entry:
                    cell = ENTRY
                elif hasattr(self, "_exit") and (c, r) == self._exit:
                    cell = EXIT

                elif (
                    hasattr(self, "_path")
                    and self._show_path
                    and (c, r) in self._path
                ):
                    cell = PATH

                elif (c, r) in self._pattern_cells:
                    cell = f"\033[{self.pattern_color}m   \033[0m"
                
                else:
                    cell = "   "

                middle += cell

            # الجدار الشرقي
                if self._grid[r][c] & 2:
                    middle += wall_char
                else:
                    if (
                        hasattr(self, "_path")
                        and self._show_path
                        and (c, r) in self._path
                        and (c + 1, r) in self._path
                    ):
                        middle += f"\033[{self.path_color}m \033[0m"
                    else:
                        middle += " "

            # الجدار الجنوبي
                if self._grid[r][c] & 4:
                    bottom += wall_char * 3
                else:
                    if (
                        hasattr(self, "_path")
                        and self._show_path
                        and (c, r) in self._path
                        and (c, r + 1) in self._path
                    ):
                        bottom += f"\033[{self.path_color}m   \033[0m"
                    else:
                        bottom += "   "
            # الفاصل بين الخلايا
               # bottom += wall_char
               # الفاصل بين الخلايا (الزاوية المشتركة)
                # تكون جداراً فقط إذا كان هناك جدار واحد على الأقل متصل بها
                has_east = (self._grid[r][c] & 2) != 0
                has_south = (self._grid[r][c] & 4) != 0
                has_next_south = (self._grid[r][c + 1] & 4) != 0 if (c + 1 < self._width) else True
                has_down_east = (self._grid[r + 1][c] & 2) != 0 if (r + 1 < self._height) else True

                if has_east or has_south or has_next_south or has_down_east:
                    bottom += wall_char
                else:
                    # إذا كانت كل الجدران حول هذه الزاوية مهدومة، نطبع فراغاً لتصبح المساحة نظيفة
                    bottom += " "

            print(middle)
            print(bottom)

    def solve_path(self, entry: tuple[int, int], exit: tuple[int, int]) -> list[tuple[int, int]]:
        self._entry = entry
        self._exit = exit
        queue = deque([entry])
        visited = set([entry])
        parent = {entry: None}

        directions = [
            (0, -1, 1), #N
            (0, 1, 4), #S
            (-1, 0, 8), #W
            (1, 0, 2) #E
        ]

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit:
                break

            cell = self._grid[y][x]

            for dx, dy, wall in directions:
                # Check if there is no wall in that direction
                if cell & wall != 0:
                    continue

                nx, ny = x + dx, y + dy

                #حدود المتاهة
                if nx < 0 or nx >= self._width or ny < 0 or ny >= self._height:
                    continue

                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

            # اذا ما وصلنا لل exit
        if exit not in parent:
            self._path = []
            return []

        # بناء المسار من exit الى entry
        path = []
        node = exit

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()

        self._path = path
        return path


    def check_terminal_size(self) -> bool:
        """Check if terminal size is enough to display the maze."""

        terminal = shutil.get_terminal_size()

        required_width = self._width * 2 + 1
        required_height = self._height + 2

        if terminal.columns < required_width or terminal.lines < required_height:
            return False

        return True
