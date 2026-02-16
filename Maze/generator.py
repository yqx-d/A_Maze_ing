from typing import Any, List, Tuple
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
        config: dict[str, Any]
    ) -> None:

        self.perfect = config['PERFECT']
        self.height = config['HEIGHT']
        self.width = config['WIDTH']
        self.entry_x, self.entry_y = config['ENTRY']
        self.exit_x, self.exit_y = config['EXIT']
        self.forty_two: List[Tuple[int, int]] = []
        if config['SEED'] is not None:
            random.seed(config['SEED'])

        self.maze = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def neighbors(
        self,
        x: int,
        y: int
    ) -> List[Tuple[int, int, str]]:

        directions = []
        if y > 0 and not self.maze[y-1][x].visited:
            directions.append((x, y-1, 'north'))

        if y < self.height - 1 and not self.maze[y+1][x].visited:
            directions.append((x, y+1, 'south'))

        if x > 0 and not self.maze[y][x-1].visited:
            directions.append((x-1, y, 'west'))

        if x < self.width - 1 and not self.maze[y][x+1].visited:
            directions.append((x+1, y, 'east'))

        return directions

    def remove_wall(
        self,
        x1: int, y1: int,
        x2: int, y2: int,
        direction: str
    ) -> None:

        if direction == 'north':
            self.maze[y1][x1].north = False
            self.maze[y2][x2].south = False

        elif direction == 'south':
            self.maze[y1][x1].south = False
            self.maze[y2][x2].north = False

        elif direction == 'west':
            self.maze[y1][x1].west = False
            self.maze[y2][x2].east = False

        elif direction == 'east':
            self.maze[y1][x1].east = False
            self.maze[y2][x2].west = False

    def get_forty_two(
        self
    ) -> bool:

        mheight = 5
        mwidth = 7

        if self.height < mheight or self.width < mwidth:
            return False

        pattern = [
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),

            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        ]

        start_x = (self.width - mwidth) // 2
        start_y = (self.height - mheight) // 2
        self.forty_two = [(start_x + x, start_y + y) for x, y in pattern]

        return True

    def is_forty_two_placable(
        self,
        forty_two: List[Tuple[int, int]]
    ) -> bool:

        blocked = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for x, y in forty_two:
            blocked[y][x] = True

        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        queue = [(self.entry_x, self.entry_y)]
        visited[self.entry_y][self.entry_x] = True

        while queue:
            x, y = queue.pop(0)

            if (x, y) == (self.exit_x, self.exit_y):
                return True

            cell = self.maze[y][x]

            if (not cell.north and y > 0
                    and not visited[y-1][x] and not blocked[y-1][x]):
                visited[y-1][x] = True
                queue.append((x, y-1))

            if (not cell.south and y < self.height - 1
                    and not visited[y+1][x] and not blocked[y+1][x]):
                visited[y+1][x] = True
                queue.append((x, y+1))

            if (not cell.west and x > 0
                    and not visited[y][x-1] and not blocked[y][x-1]):
                visited[y][x-1] = True
                queue.append((x-1, y))

            if (not cell.east and x < self.width - 1
                    and not visited[y][x+1] and not blocked[y][x+1]):
                visited[y][x+1] = True
                queue.append((x+1, y))

        return False

    def place_forty_two(
        self,
        forty_two: List[Tuple[int, int]]
    ) -> None:

        for x, y in forty_two:
            cell = self.maze[y][x]

            cell.north = True
            if y > 0 and (x, y-1) not in forty_two:
                self.maze[y-1][x].south = True

            cell.south = True
            if y < self.height - 1 and (x, y+1) not in forty_two:
                self.maze[y+1][x].north = True

            cell.west = True
            if x > 0 and (x-1, y) not in forty_two:
                self.maze[y][x-1].east = True

            cell.east = True
            if x < self.width - 1 and (x+1, y) not in forty_two:
                self.maze[y][x+1].west = True

    def generate(
        self
    ) -> None:

        stack = []
        self.maze[self.entry_y][self.entry_x].visited = True
        stack.append((self.entry_x, self.entry_y))

        while stack:
            x, y = stack[-1]
            neighbors = self.neighbors(x, y)

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.remove_wall(x, y, nx, ny, direction)

                self.maze[ny][nx].visited = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            for row in self.maze:
                for cell in row:
                    cell.visited = False

            if self.height < 2 or self.width < 2:
                loop = 1
            else:
                loop = (self.height + self.width) - 1

            while loop:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                neighbors = self.neighbors(x, y)

                if neighbors:
                    nx, ny, direction = random.choice(neighbors)
                    self.remove_wall(x, y, nx, ny, direction)

                loop -= 1

        if self.get_forty_two():
            if self.is_forty_two_placable(self.forty_two):
                self.place_forty_two(self.forty_two)
            else:
                self.forty_two = []
                raise Exception(
                    "Error: 42 pattern blocks all solutions, "
                    "cannot place it in the Maze.")
        else:
            self.forty_two = []
            raise Exception(
                "Error: Maze too small to place the '42' pattern.")
