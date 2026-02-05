from Maze.generator import Cell
from typing import Any


class Exporter:

    @staticmethod
    def export_to(
        maze: list[list[Cell]],
        config: dict[str, Any],
        shortest_path: str
    ) -> None:

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
        content += f"{shortest_path}\n"

        try:
            with open(path, "w") as f:
                f.write(content)

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {path} not found")

        except PermissionError:
            raise PermissionError("Error: Permission denied")
