from Maze.generator import Cell
from MazeUtils.solver import MazeSolver
from typing import Any, List, Tuple


class Exporter:
    """Export maze data to a file in hexadecimal wall format."""

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
        path_directions = Exporter.solve_directions(
            MazeSolver.solve_maze(
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
