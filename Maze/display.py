from Maze.generator import Cell
from Maze.solver import MazeSolver
from typing import Any, Tuple, List, Optional
import time


class Display:
    """Display maze in terminal with ASCII art and ANSI color support."""

    @staticmethod
    def theme_maze(
        theme: str
    ) -> tuple[str, str, str, str, str, str]:
        """
        Apply color theme to maze display elements.

        Args:
            theme: Theme name ('BLUE', 'YELLOW', 'PURPLE', 'DEFAULT').

        Returns:
            Tuple of formatted strings: entry, exit, wall, space, path,
            forty_two.
        """
        entry = "██"
        exit = "██"
        wall = "██"
        path = "██"
        forty_two = "██"
        space = "  "

        if theme.upper() == "BLUE":
            entry = "\033[94;1m" + entry + "\033[0m"
            exit = "\033[36;1m" + exit + "\033[0m"
            wall = "\033[34m" + wall + "\033[0m"
            path = "\033[96;1m" + path + "\033[0m"
            forty_two = "\033[41;1m" + forty_two + "\033[0m"
        elif theme.upper() == "YELLOW":
            entry = "\033[93;1m" + entry + "\033[0m"
            exit = "\033[91;1m" + exit + "\033[0m"
            wall = "\033[33m" + wall + "\033[0m"
            path = "\033[97;1m" + path + "\033[0m"
            forty_two = "\033[93;1m" + forty_two + "\033[0m"
        elif theme.upper() == "PURPLE":
            entry = "\033[94m" + entry + "\033[0m"
            exit = "\033[94;1m" + exit + "\033[0m"
            wall = "\033[35m" + wall + "\033[0m"
            path = "\033[96;1m" + path + "\033[0m"
            forty_two = "\033[106;1m" + forty_two + "\033[0m"
        else:
            entry = "\033[31;1m" + entry + "\033[0m"
            exit = "\033[37;1m" + exit + "\033[0m"
            wall = "\033[97m" + wall + "\033[0m"
            path = "\033[32;1m" + path + "\033[0m"
            forty_two = "\033[31;1m" + forty_two + "\033[0m"

        return entry, exit, wall, space, path, forty_two

    @staticmethod
    def display_maze(
        maze: list[list[Cell]],
        config: dict[str, Any],
        show_path: bool,
        theme: str,
        forty_two_pos: List[Tuple[int, int]],
        path_override: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        """
        Render maze with optional solution path and colors.

        Args:
            maze: 2D list of Cell objects representing the maze.
            config: Dict containing WIDTH, HEIGHT, ENTRY, EXIT.
            show_path: Whether to display the solution path.
            theme: Color theme name.
            forty_two_pos: Coordinates where the '42' pattern is located.
        """
        entry, exit, wall, space, path, forthy_two = (
            Display.theme_maze(theme)
        )
        if path_override is not None:
            path_to_exit = path_override
        elif show_path:
            path_to_exit = MazeSolver.solve_maze(
                maze,
                config['WIDTH'],
                config['HEIGHT'],
                config['ENTRY'],
                config['EXIT']
            )
        else:
            path_to_exit = []

        for y in range(len(maze)):
            top_line = ""
            for x in range(len(maze[y])):
                cell = maze[y][x]

                top_line += wall
                if cell.north:
                    top_line += wall
                elif ((x, y) in path_to_exit and (x, y-1) in path_to_exit
                      and (show_path or path_override is not None)):
                    top_line += path
                else:
                    top_line += space

            top_line += wall

            mid_line = ""
            for x in range(len(maze[y])):
                cell = maze[y][x]
                if cell.west:
                    mid_line += wall
                elif ((x, y) in path_to_exit and (x-1, y) in path_to_exit
                      and (show_path or path_override is not None)):
                    mid_line += path
                else:
                    mid_line += space

                if (x, y) == config["ENTRY"]:
                    mid_line += entry
                elif (x, y) == config["EXIT"]:
                    mid_line += exit
                elif (x, y) in forty_two_pos:
                    mid_line += forthy_two
                elif ((x, y) in path_to_exit and
                      (show_path or path_override is not None)):
                    mid_line += path
                else:
                    mid_line += space

            if maze[y][-1].east:
                mid_line += wall
            else:
                mid_line += space
            print(top_line, flush=True)
            print(mid_line, flush=True)

        bot_line = ""
        for x in range(len(maze[-1])):
            cell = maze[-1][x]
            bot_line += wall
            if cell.south:
                bot_line += wall
            else:
                bot_line += space

        bot_line += wall
        print(bot_line, flush=True)

    @staticmethod
    def animate_path(
        maze: List[list[Cell]],
        config: dict[str, Any],
        theme: str,
        forty_two_pos: List[Tuple[int, int]],
        state: bool,
    ) -> None:
        """
        Animate the solution path revealing or hiding it step by step.

        Args:
            maze: 2D list of Cell objects representing the maze.
            config: Dict containing WIDTH, HEIGHT, ENTRY, EXIT.
            theme: Color theme name.
            forty_two_pos: Coordinates where the '42' pattern is located.
            state: True to reveal path, False to hide it.
        """
        path = MazeSolver.solve_maze(
            maze, config['WIDTH'], config['HEIGHT'],
            config['ENTRY'], config['EXIT']
        )
        if config['HEIGHT'] > 25:
            delay = 0.015
        else:
            delay = 0.025
        if state:
            revealed = []
            for cell in path:
                revealed.append(cell)

                print("\033[H", end="")
                Display.display_maze(
                    maze,
                    config,
                    show_path=False,
                    theme=theme,
                    forty_two_pos=forty_two_pos,
                    path_override=revealed
                )
                time.sleep(delay)
        else:
            revealed = [cell for cell in path]
            while revealed:
                revealed.pop()

                print("\033[H", end="")
                Display.display_maze(
                    maze,
                    config,
                    show_path=False,
                    theme=theme,
                    forty_two_pos=forty_two_pos,
                    path_override=revealed
                )
                time.sleep(delay)
