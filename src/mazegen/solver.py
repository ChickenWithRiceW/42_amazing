import heapq
from typing import TypeAlias
from .generator import DELTA, MazeGenerator

DELTA_str = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}


Cell: TypeAlias = tuple[int, int]


class NoSolutionError(Exception):
    def __init__(self) -> None:
        super().__init__("No solution can be found")


class Solver():
    """A Solver class that uses the A* algorithm to find the best path to
    solve a maze
    """
    def __init__(self, maze: MazeGenerator) -> None:
        # input
        self.maze = maze.grid
        self.maze_instance = maze

        # Calculated Boundaries
        self.max_x = maze.width
        self.max_y = maze.height

        # Init
        self.open_list: list[tuple[int, int, Cell]] = []
        self.closed: set[Cell] = set()
        self.g_score: dict[Cell, int] = {}
        self.parent: dict[Cell, Cell] = {}

    def solver(self, entry_pos: Cell, exit_pos: Cell) -> list[Cell]:
        # Pushes the entry into the open_list, init with f=0, h=0, pos
        heapq.heappush(self.open_list, (0, 0, entry_pos))
        self.g_score[entry_pos] = 0

        # As long list is not empty
        while self.open_list:
            # Grabs only the cell not the {f, h} data
            current_cell = heapq.heappop(self.open_list)[2]

            if current_cell in self.closed:
                continue

            # Adds to closed as this was the best f cost
            # with a constant heuristic it cant get any better
            # as the best path was figured out
            self.closed.add(current_cell)

            if current_cell == exit_pos:
                return self._back_trace(current_cell)

            neighbours = self._find_neighbours(current_cell)

            for neighbour in neighbours:
                h = self._manhattan_distance(neighbour, exit_pos)
                g = self.g_score[current_cell] + 1

                if (neighbour not in self.g_score
                        or g < self.g_score[neighbour]):

                    self.g_score[neighbour] = g
                    f = g + h
                    self.parent[neighbour] = current_cell
                    heapq.heappush(self.open_list, (f, h, neighbour))
        raise NoSolutionError()

    def _back_trace(self, current_cell: Cell) -> list[Cell]:
        """Backtraces the parents of given current pos cell

        Returns list of (x,y) tuples from entry to exit
        """
        path = [current_cell]
        while par := self.parent.get(current_cell):
            path.append(par)
            for direction, (dy, dx) in DELTA_str.items():
                if (current_cell[0] - dx, current_cell[1] - dy) == par:
                    self.maze_instance.solution.append(direction)
            current_cell = par

        path.reverse()
        self.maze_instance.solution.reverse()
        return path

    @staticmethod
    def _manhattan_distance(a: Cell, b: Cell) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _find_neighbours(self, cell: Cell) -> list[Cell]:
        """Finds neighbours of cell and returns them if not blocked/closed

        Checks for valid neighbours horizontal or vertical of cell.
        Returns neighbours that aren't closed or blocked in a list.
        """
        x, y = cell
        neighbours: list[Cell] = []

        for direction, (dy, dx) in DELTA.items():

            # Skip if neighbour is not accessible
            if self.maze[y][x] & direction:
                continue

            new_y = y + dy
            new_x = x + dx
            if (0 <= new_y < self.max_y and 0 <= new_x < self.max_x
                    and (new_x, new_y) not in self.closed):
                neighbours.append((new_x, new_y))

        return neighbours
