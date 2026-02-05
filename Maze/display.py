from Maze.generator import Cell
from typing import Any


class Display:

    @staticmethod
    def theme_maze(
        theme: str
    ) -> tuple:

        entry = "█"
        exit = "█"
        wall = "█"
        path = "█"
        forthy_two = "█"
        space = " "

        if theme.upper() == "BLUE":
            entry = "\033[94m" + entry + "\033[0m"
            exit = "\033[34m" + exit + "\033[0m"
            wall = "\033[44m" + wall + "\033[0m"
            path = "\033[96m" + path + "\033[0m"
            forthy_two = "\033[94;1m" + forthy_two + "\033[0m"

        elif theme.upper() == "YELLOW":
            entry = "\033[93m" + entry + "\033[0m"
            exit = "\033[33m" + exit + "\033[0m"
            wall = "\033[43m" + wall + "\033[0m"
            path = "\033[33;1m" + path + "\033[0m"
            forthy_two = "\033[93;1m" + forthy_two + "\033[0m"

        elif theme.upper() == "PURPLE":
            entry = "\033[95m" + entry + "\033[0m"
            exit = "\033[35m" + exit + "\033[0m"
            wall = "\033[45m" + wall + "\033[0m"
            path = "\033[95;1m" + path + "\033[0m"
            forthy_two = "\033[35;1m" + forthy_two + "\033[0m"

        else:
            entry = "\033[97m" + entry + "\033[0m"
            exit = "\033[37m" + exit + "\033[0m"
            wall = "\033[107m" + wall + "\033[0m"
            path = "\033[97;1m" + path + "\033[0m"
            forthy_two = "\033[92;1m" + forthy_two + "\033[0m"

        return entry, exit, wall, space, path, forthy_two

    @staticmethod
    def display_maze(
        maze: list[list[Cell]],
        config: dict[str, Any],
        show_path: bool,
        theme: str
    ) -> None:

        entry, exit, wall, space, path, forthy_two = Display.theme_maze(theme)
