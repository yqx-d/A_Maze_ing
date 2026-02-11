from Maze.generator import Cell
from Maze.solver import MazeSolver
from typing import Any, Tuple, List
import time


class Display:
    @staticmethod
    def theme_maze(
        theme: str
    ) -> tuple:
        entry = "█"
        exit = "█"
        wall = "█"
        path = "█"
        forty_two = "█"
        space = " "

        if theme.upper() == "BLUE":
            entry = "\033[94;1m" + entry + "\033[0m"
            exit = "\033[36;1m" + exit + "\033[0m"
            wall = "\033[34m" + wall + "\033[0m"
            path = "\033[96;1m" + path + "\033[0m"
            forty_two = "\033[94;1m" + forty_two + "\033[0m"
        elif theme.upper() == "YELLOW":
            entry = "\033[93;1m" + entry + "\033[0m"
            exit = "\033[91;1m" + exit + "\033[0m"
            wall = "\033[33m" + wall + "\033[0m"
            path = "\033[97;1m" + path + "\033[0m"
            forty_two = "\033[93;1m" + forty_two + "\033[0m"
        elif theme.upper() == "PURPLE":
            entry = "\033[95;1m" + entry + "\033[0m"
            exit = "\033[94;1m" + exit + "\033[0m"
            wall = "\033[35m" + wall + "\033[0m"
            path = "\033[95;1m" + path + "\033[0m"
            forty_two = "\033[35;1m" + forty_two + "\033[0m"
        else:
            entry = "\033[97;1m" + entry + "\033[0m"
            exit = "\033[37;1m" + exit + "\033[0m"
            wall = "\033[97m" + wall + "\033[0m"
            path = "\033[97;1m" + path + "\033[0m"
            forty_two = "\033[92;1m" + forty_two + "\033[0m"

        return entry, exit, wall, space, path, forty_two

    @staticmethod
    def display_maze(
        maze: list[list[Cell]],
        config: dict[str, Any],
        show_path: bool,
        theme: str,
        forty_two_pos: List[Tuple[int, int]]
    ) -> None:
        entry, exit, wall, space, path, forthy_two = Display.theme_maze(theme)

        if show_path:
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
            # TOP LINE
            top_line = ""
            for x in range(len(maze[y])):
                cell = maze[y][x]

                top_line += wall
                if ((x, y) in forty_two_pos and
                   (x, y-1) in forty_two_pos):
                    top_line += forthy_two
                elif ((x, y-1) in forty_two_pos and
                      (x, y) not in forty_two_pos):
                    top_line += wall
                elif cell.north:
                    top_line += wall
                elif ((x, y) in path_to_exit and
                      (x, y-1) in path_to_exit and
                      show_path):
                    top_line += path
                else:
                    top_line += space
            top_line += wall

            # MIDDLE LINE
            mid_line = ""
            for x in range(len(maze[y])):
                cell = maze[y][x]
                if ((x, y) in forty_two_pos and
                   (x-1, y)) in forty_two_pos:
                    mid_line += forthy_two
                elif ((x-1, y) in forty_two_pos
                      and (x, y) not in forty_two_pos):
                    mid_line += wall
                elif cell.west:
                    mid_line += wall
                elif ((x, y) in path_to_exit and
                      (x-1, y) in path_to_exit and
                      show_path):
                    mid_line += path
                else:
                    mid_line += space

                if (x, y) == config["ENTRY"]:
                    mid_line += entry
                elif (x, y) == config["EXIT"]:
                    mid_line += exit
                elif (x, y) in forty_two_pos:
                    mid_line += forthy_two
                elif (x, y) in path_to_exit and show_path:
                    mid_line += path
                else:
                    mid_line += space

            if maze[y][-1].east:
                mid_line += wall
            else:
                mid_line += space
            time.sleep(0.025)
            print(top_line)
            print(mid_line)

        bot_line = ""
        for x in range(len(maze[-1])):
            cell = maze[-1][x]
            bot_line += wall
            if cell.south:
                bot_line += wall
            else:
                bot_line += space

        bot_line += wall
        print(bot_line)
