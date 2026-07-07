import heapq
from typing import TypeAlias
from .generator import DELTA, MazeGenerator

DELTA_str = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}


Cell: TypeAlias = tuple[int, int]


class NoSolutionError(Exception):
    def __init__(self) -> None:
        super().__init__("No solution can be found")


class Solver():
    """A Solver that uses the A* algorithm to find the best path to
    solve a maze.

    Usage:
        Instantiate with a maze instance from the generator class,
        then call the solver method to attempt to solve the maze.

    Args:
        maze: A MazeGenerator instance containing the grid to solve.

    Side effect:
        Sets the maze instance's solution attribute to the calculated
        path directions when using solver method
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

    def _back_trace(self, current_cell: Cell) -> list[Cell]:
        """Backtraces from current cell all the way until origin (entry cell).

        Side effect:
            Sets the maze instance's solution attribute to the calculated
            path directions.

        Returns:
            A list of (x, y) tuples (Cell), as a route through the maze,
            from entry to exit.
        """

        self.maze_instance.solution = []
        path = [current_cell]

        while par := self.parent.get(current_cell):
            path.append(par)
            for direction, (dx, dy) in DELTA_str.items():
                # appends reversed direction onto list
                if (current_cell[0] - dx, current_cell[1] - dy) == par:
                    self.maze_instance.solution.append(direction)
            current_cell = par

        # Reverse lists to match desired output from entry to exit
        path.reverse()
        self.maze_instance.solution.reverse()

        return path

    def solver(self, entry_pos: Cell, exit_pos: Cell) -> list[Cell]:
        """Solver that uses the A* algorithm to find the best path to
        solve a maze.

        Args:
            entry_pos: Entry position of the maze example: (0, 0)
            exit_pos: Exit position of the maze example: (10, 10)

        Side effect:
            Sets the maze instance's solution attribute to the calculated
            path directions.

        Returns:
            A list of (x, y) tuples describing the route through the maze,
            from entry to exit.
        """
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

    @staticmethod
    def _manhattan_distance(a: Cell, b: Cell) -> int:
        """Returns the manhatten distance between two (x, y) cells)"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _find_neighbours(self, cell: Cell) -> list[Cell]:
        """Finds accessible, unclosed neighbours of a cell.

        Checks the four orthogonal directions around the cell and skips
        any that are wall-blocked or already in the closed set.

        Args:
            cell: The (x, y) position to check neighbours of.

        Returns:
            A list of (x, y) tuples for each valid neighbour.
        """

        x, y = cell
        neighbours: list[Cell] = []

        for direction, (dx, dy) in DELTA.items():

            # Skip if neighbour is not blocked by wall
            if self.maze[y][x] & direction:
                continue

            new_x = x + dx
            new_y = y + dy
            if (0 <= new_y < self.max_y and 0 <= new_x < self.max_x
                    and (new_x, new_y) not in self.closed):
                neighbours.append((new_x, new_y))

        return neighbours
