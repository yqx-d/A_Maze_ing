from Maze.generator import Cell
from typing import Any, Tuple, List
from Maze.solver import solve_maze


class Display:
    @staticmethod
    def theme_maze(theme: str) -> tuple:
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
        theme: str,
        forty_two_pos: List[Tuple[int, int]]
    ) -> None:
        entry, exit, wall, space, path, forthy_two = Display.theme_maze(theme)

        if show_path:
            path_to_exit = solve_maze(
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

                if cell.north:
                    top_line += wall
                    #ok
                elif (x, y) in path_to_exit and show_path:
                    top_line += path
                elif (x, y) in forty_two_pos:
                    top_line += forthy_two
                else:
                    top_line += space
            top_line += wall

            # MIDDLE LINE
            mid_line = ""
            for x in range(len(maze[y])):
                cell = maze[y][x]
                # Mur ouest ou espace
                if cell.west:
                    mid_line += wall
                # retire le prb est mais genere Nord
                elif (x, y) in path_to_exit and show_path:
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

            print(top_line)
            print(mid_line)

        bot_line = ""
        for x in range(len(maze[-1])):
            cell = maze[-1][x]
            bot_line += wall
            if cell.south:
                bot_line += wall
            elif (x, y) in path_to_exit and show_path:
                bot_line += path
            elif (x, y) in forty_two_pos:
                bot_line += forthy_two
            else:
                bot_line += space
        # Coin sud-est
        bot_line += wall
        print(bot_line)
