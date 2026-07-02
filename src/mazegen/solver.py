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


# TODO: Would like to change to x,y
DELTA = {
    Wall.NORTH: (-1, 0),
    Wall.SOUTH: (1, 0),
    Wall.EAST: (0, 1),
    Wall.WEST: (0, -1)
}


# ! Only there for testing
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


class Solver():
    """A Solver class that uses the A-* algorithm to find the best path to
    solve a maze
    """
    def __init__(self, entry: tuple[int, int], exit: tuple[int, int],
                 maze: list[list[int]]) -> list[tuple[int, int] | None]:
        # input
        self.entry = entry
        self.exit = exit
        self.maze = maze

        # Calculated Boundaries
        self.max_x = len(maze[0])
        self.max_y = len(maze)

        # Init
        self.open_list: list[tuple[int, int, tuple[int, int]]] = []
        self.closed: set = set()
        self.g_score: dict[tuple[int, int], int] = {}
        self.parent: dict[tuple[int, int], tuple[int, int]] = {}

        # Pushes the entry into the open_list, init with f=0, h=0, pos
        heapq.heappush(self.open_list, (0, 0, self.entry))
        self.g_score[self.entry] = 0

    def solver(self) -> None:
        # As long list is not empty
        while self.open_list:
            _, _, current_pos = heapq.heappop(self.open_list)

            if current_pos in self.closed:
                continue
            self.closed.add(current_pos)

            if current_pos == self.exit:
                print("Found exit!")
                self._back_trace(current_pos)
                return

            neighbours = self._find_neighbours(current_pos)

            for neighbour in neighbours:
                h = self._manhattan_distance(neighbour, self.exit)
                g = self.g_score[current_pos] + 1

                if neighbour not in self.g_score or g < self.g_score[neighbour]:
                    self.g_score[neighbour] = g
                    f = g + h
                    self.parent[neighbour] = current_pos
                    heapq.heappush(self.open_list, (f, h, neighbour))
        print("Nothing found :(")
        return None

    def _back_trace(self, current_pos: tuple[int, int]):
        """Backtraces the parents of given current pos cell

        Returns list of (x,y) tuples from entry to exit
        """
        path = [current_pos]

        while par := self.parent.get(current_pos):
            path.append(par)
            current_pos = par

        path.reverse()
        print(path)     # Just for showing remove later
        return path

    @staticmethod
    def _manhattan_distance(a: tuple, b: tuple) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _find_neighbours(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """Finds neighbours of pos and returns them if not blocked/visited

        Checks for valid neighbours horizontal or vertical of pos.
        Returns neighbours that aren't visited or blocked.
        """
        x, y = pos
        neighbours: list[tuple[int, int]] = []

        for direction, (dy, dx) in DELTA.items():

            # Skip if there is a wall in this direction
            if self.maze[y][x] & direction:
                continue

            new_y = y + dy
            new_x = x + dx
            if (0 <= new_y < self.max_y and 0 <= new_x < self.max_x
                    and (new_x, new_y) not in self.closed):
                neighbours.append((new_x, new_y))

        return neighbours

if __name__ == "__main__":
    solver((0, 0), (19, 14), pregen)
    # print(closed_set)