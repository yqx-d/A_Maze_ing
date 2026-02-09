from typing import List, Tuple, Dict

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

    # queue : liste de cases a explorer
    # parent: dictionnaire qui memorise le chemin et qui permettra de le reconstruire a la fin

    parents: Dict[Tuple[int, int], Tuple[int, int]]  = {}
    queue: List[Tuple[int, int]] = []

    queue.append((entry_x, entry_y))
    visited[entry_y][entry_x] = True

    while queue:
        x, y = queue.pop(0)

        if (x, y) == (exit_x, exit_y):
            break
        cell = maze[y][x]

        # Si mur nord est ouvert et que y ne soit pas hors grille et nord pas encore visite
        if (not cell.north and y > 0 and not visited[y - 1][x]):
            visited[y-1][x] = True  # nord visite
            parents[(x, y-1)] = (x, y)  # pour arriver a (x, y-1), on vient de x y
            queue.append((x, y-1))  # ajout de la case pour etre explorer par BFS

        # y < height - 1 (pas sortir de la grille) SUD

        # x > 0 OUEST



        # x < width - 1   EST


        # Construire le chemin
