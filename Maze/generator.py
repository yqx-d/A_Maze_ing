from typing import Any, List, Tuple, Optional, Dict
import random


class Cell:
    """
    Represents a single cell in the maze grid.

    Each cell has four walls (north, east, south, west) and a visited flag
    used during maze generation.
    """

    def __init__(self) -> None:
        """Initialize a cell with all walls closed and not visited."""
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class MazeGenerator:
    """
    Generate a maze using depth-first search algorithm.

    Generates either perfect mazes (single path between entry and exit)
    or random mazes with multiple loops using recursive backtracking.
    """

    def __init__(
        self,
        config: dict[str, Any]
    ) -> None:
        """
        Initialize the maze generator with configuration parameters.

        Args:
            config: Dict with WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, SEED.
                WIDTH (int): Maze width in cells.
                HEIGHT (int): Maze height in cells.
                ENTRY (tuple): Entry point (x, y).
                EXIT (tuple): Exit point (x, y).
                PERFECT (bool): Generate perfect maze.
                SEED (int or None): Random seed.
        """
        self.config = config
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
        """
        Get all unvisited neighbors of a given cell.

        Args:
            x: X coordinate of the cell.
            y: Y coordinate of the cell.

        Returns:
            List of tuples (x, y, direction) for each unvisited neighbor.
        """
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
        """
        Remove wall between two adjacent cells.

        Updates both cells to maintain maze coherence: if cell A has no
        east wall, then cell B to the east must have no west wall.

        Args:
            x1: X coordinate of the first cell.
            y1: Y coordinate of the first cell.
            x2: X coordinate of the second cell.
            y2: Y coordinate of the second cell.
            direction: Wall to remove: 'north', 'south', 'east', 'west'.
        """
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

    def place_forty_two(
        self
    ) -> bool:
        """
        Place the '42' pattern as fully closed cells in the maze center.

        The pattern is only placed if the maze is large enough.

        Returns:
            True if pattern was successfully placed, False if maze
            is too small.
        """
        mheight = 8
        mwidth = 11

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

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2
        self.forty_two = [(start_x + x, start_y + y) for x, y in pattern]

        return True

    def dfs(self) -> None:
        """Generate maze using depth-first search algorithm."""
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

    def bfs(self) -> None:
        """Generate maze using breadth-first search algorithm."""
        queue = [(self.entry_x, self.entry_y)]
        self.maze[self.entry_y][self.entry_x].visited = True

        while queue:
            x, y = queue.pop(0)
            neighbors = self.neighbors(x, y)
            random.shuffle(neighbors)

            for nx, ny, direction in neighbors:
                self.remove_wall(x, y, nx, ny, direction)
                self.maze[ny][nx].visited = True
                queue.append((nx, ny))

    def generate(
        self,
        other_algorithm: Optional[bool] = False,
    ) -> None:
        """
        Generate the maze using DFS or BFS algorithm.

        Args:
            other_algorithm: If True, use BFS; if False, use DFS.

        For perfect mazes: generates a spanning tree with single path
        between entry and exit.
        For random mazes: adds random loops respecting the 2-cell max
        corridor width.

        Raises:
            Exception: If maze is too small to place '42' pattern.
        """

        if not self.place_forty_two():
            self.forty_two = []
            raise Exception(
                "Error: Maze too small to place the '42' pattern.")

        if (self.entry_x, self.entry_y) in self.forty_two:
            raise ValueError("Entry on 42")

        if (self.exit_x, self.exit_y) in self.forty_two:
            raise ValueError("Exit on 42")

        for x, y in self.forty_two:
            self.maze[y][x].visited = True

        if other_algorithm:
            self.bfs()
        else:
            self.dfs()

        if not self.perfect:
            for row in self.maze:
                for cell in row:
                    cell.visited = False

            loop = (self.height + self.width) - 1

            while loop:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (x, y) not in self.forty_two:
                    neighbors = self.neighbors(x, y)

                    if neighbors:
                        nx, ny, direction = random.choice(neighbors)
                        if (nx, ny) not in self.forty_two:
                            self.remove_wall(x, y, nx, ny, direction)

                    loop -= 1

        MazeGenerator.export_to(self.maze, self.config)

    @staticmethod
    def solve_maze(
        maze: List[List[Cell]],
        w: int,
        h: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Find the shortest path through the maze using BFS algorithm.

        Args:
            maze: 2D list of Cell objects representing the maze.
            w: Maze width in cells.
            h: Maze height in cells.
            entry: Starting point as (x, y) coordinates.
            exit: Destination point as (x, y) coordinates.

        Returns:
            List of (x, y) tuples representing the path from entry to exit.
        """
        entry_x, entry_y = entry
        exit_x, exit_y = exit

        visited = [
            [False for _ in range(w)]
            for _ in range(h)
        ]

        parents: Dict[Tuple[int, int], Tuple[int, int]] = {}
        queue: List[Tuple[int, int]] = []

        queue.append((entry_x, entry_y))
        visited[entry_y][entry_x] = True

        while queue:
            x, y = queue.pop(0)

            if (x, y) == (exit_x, exit_y):
                break
            cell = maze[y][x]

            if (not cell.north and y > 0 and not visited[y - 1][x]):
                visited[y-1][x] = True
                parents[(x, y-1)] = (x, y)
                queue.append((x, y-1))

            if (not cell.south and y < h - 1 and not visited[y + 1][x]):
                visited[y+1][x] = True
                parents[(x, y+1)] = (x, y)
                queue.append((x, y+1))

            if (not cell.west and x > 0 and not visited[y][x-1]):
                visited[y][x-1] = True
                parents[(x-1, y)] = (x, y)
                queue.append((x-1, y))

            if (not cell.east and x < w-1 and not visited[y][x+1]):
                visited[y][x+1] = True
                parents[(x+1, y)] = (x, y)
                queue.append((x+1, y))

        path = []
        current = exit_x, exit_y

        while current in parents:
            path.append(current)
            current = parents[current]

        path.append((entry_x, entry_y))
        path.reverse()

        return path

    @staticmethod
    def solve_directions(
        path: List[Tuple[int, int]]
    ) -> str:
        """
        Convert a path of coordinates into a direction string.

        Args:
            path: List of (x, y) tuples representing the solution path.

        Returns:
            String of direction characters (N, E, S, W) representing movement.
        """
        str_dir = ""
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]

            if x1 < x2:
                str_dir += "E"
            elif x1 > x2:
                str_dir += "W"
            elif y1 < y2:
                str_dir += "S"
            elif y1 > y2:
                str_dir += "N"
        return str_dir

    @staticmethod
    def export_to(
        maze: list[list[Cell]],
        config: dict[str, Any]
    ) -> None:
        """
        Export maze to a file in hexadecimal format with solution path.

        Format: Each cell is one hexadecimal digit encoding wall positions.
        Bits: 0=North, 1=East, 2=South, 3=West
        (1=wall closed, 0=wall open).
        Followed by entry coords, exit coords, and path as direction string.

        Args:
            maze: 2D list of Cell objects representing the maze.
            config: Dictionary containing OUTPUT_FILE, WIDTH, HEIGHT,
                ENTRY, EXIT.

        Raises:
            FileNotFoundError: If output file path is invalid.
            PermissionError: If permission denied when writing file.
        """
        path = config['OUTPUT_FILE']
        content = ""

        for row in maze:
            for cell in row:
                cell_binary = (
                    ("1" if cell.west else "0") +
                    ("1" if cell.south else "0") +
                    ("1" if cell.east else "0") +
                    ("1" if cell.north else "0")
                )
                value = int(cell_binary, 2)
                content += format(value, "X")
            content += "\n"

        content += "\n"
        entry_x, entry_y = config['ENTRY']
        exit_x, exit_y = config['EXIT']

        content += f"{entry_x},{entry_y}\n"
        content += f"{exit_x},{exit_y}\n"
        path_directions = MazeGenerator.solve_directions(
            MazeGenerator.solve_maze(
                maze,
                config["WIDTH"],
                config["HEIGHT"],
                config["ENTRY"],
                config["EXIT"]
            )
        )
        content += f"{path_directions}\n"

        try:
            with open(path, "w") as f:
                f.write(content)

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {path} not found")

        except PermissionError:
            raise PermissionError("Error: Permission denied")
