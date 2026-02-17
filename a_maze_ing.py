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


def clear() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def sound_error() -> None:
    """Play error sound effect, ignore if not available."""
    try:
        from playsound import playsound
        playsound("error.mp3")
    except Exception as e:
        print(e)


def exit_sound() -> None:
    """Play exit sound effect, ignore if not available."""
    try:
        from playsound import playsound
        playsound("bye.mp3")
    except Exception as e:
        print(e)


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
                Exporter.export_to(maze.maze, config)

            except Exception as e:
                error = e

            while True:
                clear()

                try:
                    Display.display_maze(
                        (maze.maze), config,
                        show_path, theme[theme_index], maze.forty_two
                    )
                except KeyboardInterrupt:
                    clear()
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

                            wErr = ""
                            maze = MazeGenerator(config)
                            while True:
                                try:
                                    clear()
                                    if wErr:
                                        print(wErr)
                                    algo_input = int(input(
                                        "Choose your algorithm: \n"
                                        "1. Depth-First Search (DFS)\n"
                                        "2. Breadth-First Search (BFS)\n"
                                        "\nChoice? (1-2): "
                                    ))

                                    if algo_input == 1:
                                        maze.generate(other_algorithm=False)
                                        break

                                    elif algo_input == 2:
                                        maze.generate(other_algorithm=True)
                                        break

                                    else:
                                        wErr = "Please choose "
                                        wErr += "between 1 and 2.\n"

                                except ValueError:
                                    wErr = "Please choose between 1 and 2.\n"
                                    continue

                                except KeyboardInterrupt:
                                    clear()
                                    print("\nExit program.")
                                    sys.exit(0)

                                except Exception as e:
                                    wErr = e
                                    continue

                            continue

                        elif answer == 2:
                            if show_path:
                                show_path = False
                                print("\033[H", end="", flush=True)
                                try:
                                    Display.animate_path(
                                        maze=maze.maze, config=config,
                                        theme=theme[theme_index],
                                        forty_two_pos=maze.forty_two,
                                        state=show_path
                                    )
                                except Exception as e:
                                    error = e
                            else:
                                show_path = True
                                print("\033[H", end="", flush=True)
                                try:
                                    Display.animate_path(
                                        maze=maze.maze, config=config,
                                        theme=theme[theme_index],
                                        forty_two_pos=maze.forty_two,
                                        state=show_path
                                    )
                                except Exception as e:
                                    error = e
                            continue

                        elif answer == 3:
                            theme_index = (theme_index + 1) % len(theme)
                            continue

                        elif answer == 4:
                            try:
                                Exporter.export_to(
                                    maze.maze,
                                    config
                                )
                            except Exception as e:
                                error = e

                            continue

                        elif answer == 5:
                            exit_sound()
                            sys.exit(0)
                    else:
                        print("Please choose between 1 and 5.")
                        sound_error()
                        continue

                except ValueError:
                    print("Please choose a DIGIT between 1 and 5.")
                    sound_error()
                    continue

                except KeyboardInterrupt:
                    clear()
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
