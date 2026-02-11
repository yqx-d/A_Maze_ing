from typing import List, Tuple, Dict


class MazeSolver:

    @staticmethod
    def solve_maze(maze,
                   w: int,
                   h: int,
                   entry: Tuple[int, int],
                   exit: Tuple[int, int]
                   ) -> List[Tuple[int, int]]:
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

            # NORTH
            if (not cell.north and y > 0 and not visited[y - 1][x]):
                visited[y-1][x] = True
                parents[(x, y-1)] = (x, y)
                queue.append((x, y-1))

            # SOUTH
            if (not cell.south and y < h - 1 and not visited[y + 1][x]):
                visited[y+1][x] = True
                parents[(x, y+1)] = (x, y)
                queue.append((x, y+1))
            # WEST
            if (not cell.west and x > 0 and not visited[y][x-1]):
                visited[y][x-1] = True
                parents[(x-1, y)] = (x, y)
                queue.append((x-1, y))

            # EAST
            if (not cell.east and x < w-1 and not visited[y][x+1]):
                visited[y][x+1] = True
                parents[(x+1, y)] = (x, y)
                queue.append((x+1, y))

            # Rebuild the path

        path: List = []
        current = exit_x, exit_y

        while current in parents:
            path.append(current)
            current = parents[current]

        path.append((entry_x, entry_y))
        path.reverse()

        return path
