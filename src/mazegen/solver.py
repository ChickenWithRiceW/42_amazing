from enum import IntEnum
import heapq

class Wall(IntEnum):
    """Wall direction flags encoded as bit values.
    Each value represents one wall of a cell. Multiple walls are
    combined with bitwise OR. Bit 0=North, 1=East, 2=South, 3=West.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

DELTA = {
    Wall.NORTH: (-1, 0),
    Wall.SOUTH: (1, 0),
    Wall.EAST: (0, 1),
    Wall.WEST: (0, -1)
}



pregen = [
    [11, 9, 3, 9, 3, 9, 5, 5, 5, 5, 3, 13, 1, 5, 5, 5, 3, 9, 3, 11],
    [10, 10, 10, 10, 10, 10, 9, 5, 5, 3, 12, 3, 8, 5, 3, 13, 4, 6, 12, 2],
    [12, 6, 12, 6, 10, 10, 12, 5, 7, 12, 5, 2, 12, 7, 12, 3, 13, 3, 9, 6],
    [9, 5, 7, 9, 6, 10, 9, 5, 5, 5, 3, 12, 5, 5, 5, 6, 9, 6, 10, 11],
    [8, 5, 5, 6, 9, 4, 4, 5, 7, 9, 6, 9, 5, 3, 9, 3, 8, 5, 6, 10],
    [10, 13, 5, 1, 6, 9, 3, 9, 5, 6, 9, 6, 11, 10, 10, 14, 10, 13, 1, 2],
    [12, 5, 3, 10, 9, 6, 12, 6, 9, 5, 6, 9, 2, 12, 2, 9, 6, 9, 6, 10],
    [13, 3, 10, 14, 10, 13, 5, 5, 2, 9, 5, 6, 10, 11, 10, 12, 5, 6, 9, 6],
    [9, 6, 10, 9, 6, 9, 5, 3, 10, 10, 13, 5, 4, 6, 12, 5, 5, 3, 10, 11],
    [10, 9, 6, 10, 13, 2, 11, 10, 10, 12, 1, 5, 5, 5, 1, 3, 9, 6, 10, 10],
    [10, 12, 5, 6, 9, 6, 8, 6, 12, 3, 14, 9, 5, 3, 14, 12, 2, 9, 6, 10],
    [8, 1, 5, 3, 10, 11, 10, 9, 5, 2, 9, 6, 11, 12, 5, 3, 14, 10, 9, 2],
    [10, 10, 9, 6, 10, 12, 4, 6, 9, 6, 10, 13, 0, 1, 7, 12, 3, 10, 14, 10],
    [14, 10, 10, 9, 2, 9, 3, 9, 4, 7, 12, 3, 14, 10, 9, 5, 6, 10, 9, 6],
    [9, 6, 12, 6, 14, 10, 10, 12, 3, 9, 3, 10, 9, 2, 12, 5, 3, 10, 8, 3],
    [12, 3, 9, 5, 5, 6, 12, 3, 14, 10, 10, 12, 6, 10, 9, 7, 12, 6, 14, 10],
    [9, 6, 10, 13, 5, 5, 3, 12, 3, 10, 12, 5, 5, 6, 12, 5, 1, 5, 3, 10],
    [8, 5, 6, 9, 5, 5, 2, 11, 10, 10, 13, 1, 3, 13, 1, 5, 6, 11, 10, 10],
    [12, 5, 3, 10, 9, 3, 12, 2, 12, 6, 9, 6, 12, 3, 12, 3, 9, 2, 10, 10],
    [13, 5, 4, 6, 14, 12, 5, 4, 5, 5, 6, 13, 5, 4, 5, 6, 14, 12, 4, 6]
    ]

max_x = len(pregen[0])
max_y = len(pregen)

# WIDTH=12
# HEIGHT=15

# EXIT=19,14
# ENTRY=0,0

# y
# x
open_list: list[tuple[int, tuple[int, int]]] = []
visited = set()
traveled_list = []
g_score = {}


def start(entry: tuple[int, int], exit: tuple[int, int]) -> None:
    g_score[entry] = 0

    heapq.heappush(open_list, (0, entry))   # (f_score, coordinate)
    neighbours = _find_neighbours(*open_list[-1], visited)
    visited.add(entry)

    for neighbour in neighbours:
        tentative_h = manhattan_distance(neighbour, exit)
        tentative_g = g_score[entry] + 1


        if neighbour not in g_score or tentative_g < g_score[neighbour]:
            g_score[neighbour] = tentative_g
            f = tentative_g + tentative_h
            heapq.heappush(open_list, (f, neighbour))
    


def manhattan_distance(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _find_neighbours(y: int, x: int, visited: set[tuple[int, int]]
                     ) -> list[tuple[Wall, int, int]]:


    """
    Firstly check if direction is open
    Then check if its in bounds and not visited
    """

    neighbours: list[tuple[int, int]] = []

    for direction, (dr, dc) in DELTA.items():

        # Skip if there is a wall in this direction
        if pregen[y][x] & direction:
            continue

        new_y = y + dr
        new_x = x + dc
        if (0 <= new_y < max_y and 0 <= new_x < max_x
                and (new_y, new_x) not in visited):
            neighbours.append((new_y, new_x))

    return neighbours

if __name__ == "__main__":
    start((0, 0), (19, 14))