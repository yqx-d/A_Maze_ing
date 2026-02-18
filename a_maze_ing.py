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
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("assets/error.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("Exit program")
        sys.exit(1)


def exit_sound() -> None:
    """Play exit sound effect, ignore if not available."""
    try:
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("assets/bye.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("Exit program")
        sys.exit(1)


def settings_manager(fconfig: str) -> None:
    """
    Manage maze configuration settings interactively.

    This function provides a terminal interface to view and modify
    individual keys in a configuration file. It supports:
    - WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED
    - backing up the file if errors occur
    - retrying on invalid inputs
    - handling Ctrl+C to exit gracefully

    Args:
        fconfig (str): Path to the configuration file.

    Raises:
        KeyboardInterrupt: If the user presses Ctrl+C during input.
        ValueError: If the user enters an invalid choice.
        Exception: If the configuration file cannot be parsed.
    """
    settings = {
        "1": "WIDTH",
        "2": "HEIGHT",
        "3": "ENTRY",
        "4": "EXIT",
        "5": "OUTPUT_FILE",
        "6": "PERFECT",
        "7": "SEED",
    }

    error = ""
    while True:
        clear()
        if error:
            print(f"\033[41;1m {error} \033[0m")
            sound_error()
            error = ""

        try:
            answer = int(input(
                "\n╔══════════════════════════╗\n"
                "║     Settings Manager     ║\n"
                "╠══════════════════════════╣\n"
                "║  1. WIDTH                ║\n"
                "║  2. HEIGHT               ║\n"
                "║  3. ENTRY                ║\n"
                "║  4. EXIT                 ║\n"
                "║  5. OUTPUT_FILE          ║\n"
                "║  6. PERFECT              ║\n"
                "║  7. SEED                 ║\n"
                "║  8. Exit to Menu         ║\n"
                "╚══╦═══════════════════════╝\n"
                "   ╚◎ Choice? (1-8): "
            ))

            if 1 <= answer <= 8:

                if answer == 8:
                    return

                key = settings[str(answer)]

                sErr = ""
                save_file: list[str] = []
                while True:

                    try:
                        clear()
                        if sErr:
                            if save_file:
                                try:
                                    print(f"Try backup {fconfig}...")
                                    with open(fconfig, "w") as f:
                                        f.writelines(save_file)

                                    print(f"{fconfig} backup success !")

                                except Exception as e:
                                    sErr += f"\n{e}"

                            print(f"\033[41;1m {sErr} \033[0m")
                            sound_error()
                            sErr = ""

                        with open(fconfig, "r") as f:
                            lines = f.readlines()
                            save_file = lines

                        content = ""
                        for line in lines:
                            line = line.strip()
                            if line.startswith(key + "=") and '=' in line:
                                content = line.split('=', 1)[1].strip()
                                break

                        answer_option = input(
                            "\n╔══════════════════════════╗\n"
                            "║     Settings Manager     ║\n"
                            "╚══╦═══════════════════════╝\n"
                            f"   ╠═◎ KEY: \033[41;1m{key}\033[0m\n"
                            f"   ╠═◎ CONTENT: \033[32;1m{content}\033[0m\n"
                            "   ║\n"
                            f"   ╚◎ New content for {key} "
                            "(Ctrl+C to exit): "
                        )

                        with open(fconfig, "w") as f:
                            for line in lines:
                                if line.strip().startswith(key + "="):
                                    f.write(f"{key}={answer_option}\n")
                                else:
                                    f.write(line)

                        try:
                            config = Parser.parse_config(fconfig)
                            if not config:
                                sErr = "config file empty"
                                continue

                        except Exception as e:
                            sErr = str(e)
                            continue

                        break

                    except Exception as e:
                        error = str(e)
                        break

                    except KeyboardInterrupt:
                        return

            else:
                error = "Please choose between 1 and 8."

        except ValueError:
            error = "Please choose between 1 and 8."
            continue

        except Exception as e:
            error = str(e)
            continue

        except KeyboardInterrupt:
            return


if __name__ == "__main__":

    if len(sys.argv) == 2:

        config_path = sys.argv[1]
        try:
            theme = ["BLUE", "YELLOW", "PURPLE", "DEFAULT"]
            theme_index = 0
            show_path = False
            error = None
            input_error = None

            try:
                config = Parser.parse_config(config_path)
                maze = MazeGenerator(config)
                maze.generate()
                Exporter.export_to(maze.maze, config)

            except Exception as e:
                clear()
                print(f"\033[41;1m {e}\nProgram exit \033[0m")
                sys.exit(1)

            while True:
                clear()

                try:
                    if not error:
                        Display.display_maze(
                            (maze.maze), config,
                            show_path, theme[theme_index], maze.forty_two
                        )

                except KeyboardInterrupt:
                    clear()
                    print("\nExit program.")
                    exit_sound()
                    sys.exit(0)

                if error:
                    print(f"\033[41;1m {error} \033[0m")
                    error = None
                    sound_error()

                if input_error:
                    print(f"\033[41;1m {input_error} \033[0m")
                    input_error = None
                    sound_error()

                try:
                    answer = int(input(
                        "\n╔══════════════════════════╗\n"
                        "║     🌀 A-Maze-ing 🌀     ║\n"
                        "╠══════════════════════════╣\n"
                        "║  1. Re-generate maze     ║\n"
                        "║  2. Show/Hide path       ║\n"
                        "║  3. Rotate colors        ║\n"
                        "║  4. Export maze          ║\n"
                        "║  5. Change config        ║\n"
                        "║  6. Quit                 ║\n"
                        "╚══╦═══════════════════════╝\n"
                        "   ╚◎ Choice? (1-5): "
                    ))

                    if 1 <= answer <= 6:

                        if answer == 1:

                            wErr = ""
                            maze = MazeGenerator(config)
                            while True:
                                try:
                                    clear()
                                    if wErr:
                                        print(f"\033[41;1m {wErr} \033[0m\n")
                                        sound_error()
                                    algo_input = int(input(
                                        "╔═══════════════════════════════╗\n"
                                        "║ ☝🤓 Choose your algorithm ☝🤓 ║\n"
                                        "╠═══════════════════════════════╣\n"
                                        "║ 1. Depth-First Search (DFS)   ║\n"
                                        "║ 2. Breadth-First Search (BFS) ║\n"
                                        "╚══╦════════════════════════════╝\n"
                                        "   ╚◎ Choice? (1-2): "
                                    ))

                                    if algo_input == 1:
                                        maze.generate(other_algorithm=False)
                                        break

                                    elif algo_input == 2:
                                        maze.generate(other_algorithm=True)
                                        break

                                    else:
                                        wErr = "Please choose "
                                        wErr += "between 1 and 2."

                                except ValueError:
                                    wErr = "Please choose between 1 and 2."
                                    continue

                                except KeyboardInterrupt:
                                    clear()
                                    print("\nExit program.")
                                    exit_sound()
                                    sys.exit(0)

                                except Exception as e:
                                    wErr = str(e)
                                    continue

                            continue

                        elif answer == 2:
                            if config['HEIGHT'] > 95:
                                show_path = not show_path
                                continue
                            else:
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
                            try:
                                settings_manager(config_path)
                                config = Parser.parse_config(config_path)

                            except Exception as e:
                                clear()
                                print(f"\033[41;1m {e}\nProgram exit \033[0m")
                                sys.exit(1)

                            continue

                        elif answer == 6:
                            exit_sound()
                            sys.exit(0)
                    else:
                        input_error = "Please choose between 1 and 5."
                        continue

                except ValueError:
                    input_error = "Please choose a DIGIT between 1 and 5."
                    continue

                except KeyboardInterrupt:
                    clear()
                    print("\nExit program.")
                    exit_sound()
                    sys.exit(0)

        except Exception as e:
            print(e)
            sys.exit(1)

        except KeyboardInterrupt:
            clear()
            print("\nExit program.")
            exit_sound()
            sys.exit(0)

    else:
        print(
            "Invalid arguments. You must run the program like this:\n",
            f"> python3 {__file__.split('/')[len(__file__.split('/')) - 1]}",
            "config.txt")
