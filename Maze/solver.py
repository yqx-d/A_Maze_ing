from typing import List, Tuple, Dict
from Maze.generator import Cell


class MazeSolver:
    """Solve a maze by finding the shortest path from entry to exit."""

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
