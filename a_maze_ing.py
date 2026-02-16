"""A-Maze-ing: Interactive maze generator and solver.

This module provides an interactive terminal interface for generating mazes,
visualizing them with different color themes, and displaying the solution path.

Usage:
    python3 a_maze_ing.py config.txt

Where config.txt contains maze configuration parameters.
"""
from Maze.generator import MazeGenerator
from Maze.parser import Parser
from Maze.exporter import Exporter
from Maze.display import Display
import sys
import os


if __name__ == "__main__":

    if len(sys.argv) == 2:

        config_path = sys.argv[1]
        try:
            theme = ["BLUE", "YELLOW", "PURPLE", "DEFAULT"]
            theme_index = 0
            show_path = False
            error = None

            config = Parser.parse_config(config_path)
            try:
                maze = MazeGenerator(config)
                maze.generate()
            except Exception as e:
                error = e
            while True:
                os.system("cls" if os.name == "nt" else "clear")

                try:
                    Display.display_maze(
                        (maze.maze), config,
                        show_path, theme[theme_index], maze.forty_two
                    )
                except KeyboardInterrupt:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("\nExit program.")
                    sys.exit(0)

                if error:
                    print(f"{error}\n")
                    error = None

                print(
                    "\n=== A-Maze-ing ===\n"
                    "1. Re-generate a new maze\n"
                    "2. Show/Hide path from the entry to exit\n"
                    "3. Rotate maze colors\n"
                    "4. Export the Maze in hexa\n"
                    "5. Quit"
                )
                try:
                    answer = int(input("Choice? (1-5): "))
                    if 1 <= answer <= 5:

                        if answer == 1:
                            try:
                                maze = MazeGenerator(config)
                                maze.generate()
                            except Exception as e:
                                error = e
                            continue

                        elif answer == 2:
                            show_path = not show_path
                            continue

                        elif answer == 3:
                            theme_index = (theme_index + 1) % len(theme)
                            continue

                        elif answer == 4:
                            Exporter.export_to(
                                maze.maze,
                                config
                            )
                            continue

                        elif answer == 5:
                            sys.exit(0)
                    else:
                        print("Please choose between 1 and 5.")
                        continue

                except ValueError:
                    print("Please choose a DIGIT between 1 and 5.")
                    continue

                except KeyboardInterrupt:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("\nExit program.")
                    sys.exit(0)

        except Exception as e:
            print(e)
            sys.exit(1)

    else:
        print(
            "Invalid arguments. You must run the program like this:\n",
            f"> python3 {__file__.split('/')[len(__file__.split('/')) - 1]}",
            "config.txt")
