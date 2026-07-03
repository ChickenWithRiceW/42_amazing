from enum import IntEnum
import random


class Wall(IntEnum):
    """Wall direction flags encoded as bit values.
    Each value represents one wall of a cell. Multiple walls are
    combined with bitwise OR. Bit 0=North, 1=East, 2=South, 3=West.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


OPPOSITE = {
    Wall.NORTH: Wall.SOUTH,
    Wall.SOUTH: Wall.NORTH,
    Wall.EAST: Wall.WEST,
    Wall.WEST: Wall.EAST
}

DELTA = {
    Wall.NORTH: (-1, 0),
    Wall.SOUTH: (1, 0),
    Wall.EAST: (0, 1),
    Wall.WEST: (0, -1)
}

PATTERN: list[list[str]] = [
    ['X', ' ', 'X', ' ', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', ' ', 'X', 'X', 'X'],
    [' ', ' ', 'X', ' ', 'X', ' ', ' '],
    [' ', ' ', 'X', ' ', 'X', 'X', 'X']
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5


class MazeGenerator:
    """Generates a 2D maze using the recursive backtracker algorithm.
    Args:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell coordinates as (x, y).
        exit: Exit cell coordinates as (x, y).
        output_file: Path to write the maze output.
        perfect: If True, generates a perfect maze
        seed: Random seed for reproducibility. None picks a random seed.
    Attributes:
        grid: 2D list of ints encoding wall state per cell.
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            output_file: str,
            perfect: bool,
            seed: int | None
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []
        self.solution: list[str] = []

    def generate(self) -> None:
        """Generate the maze grid using recursive backtracker (iterative DFS).
        Seeds the random generator, initialises all cells as fully walled,
        then carves passages until all cells are visited. Sets self.grid.
        """

        random.seed(self.seed)
        self.grid = [[0xF] * self.width for _ in range(self.height)]

        blocked: set[tuple[int, int]] = set()
        if self._check_pattern_fits():
            self._stamp_pattern(blocked)

        visited: set[tuple[int, int]] = set()
        start_col, start_row = self.entry
        stack: list[tuple[int, int]] = [(start_row, start_col)]
        visited.add((start_row, start_col))

        while stack:
            row, col = stack[-1]

            # Find all valid unvisited neighbours
            neighbours = self._find_neighbours(row, col, visited, blocked)
            if neighbours:
                # Pick a random neighbour
                direction, new_row, new_col = random.choice(neighbours)

                # Remove a wall between current cell and chosen neighbour
                self.grid[row][col] &= ~direction
                self.grid[new_row][new_col] &= ~OPPOSITE[direction]

                # Mark neighbour visited and push onto stack
                visited.add((new_row, new_col))
                stack.append((new_row, new_col))
            else:
                # Backtrack
                stack.pop()

        if not self.perfect:
            self._add_loops(blocked)

    def solve(self) -> list[tuple[int, int]]:
        from .solver import Solver

        solve_instance = Solver(self)
        return solve_instance.solver(self.entry, self.exit)

    def _find_neighbours(
            self, row: int, col: int,
            visited: set[tuple[int, int]],
            blocked: set[tuple[int, int]]
            ) -> list[tuple[Wall, int, int]]:
        """Return valid unvisited neighbours of a cell.
        Also checks for a blocked cells if they are set.
        Args:
            row: Row index of the current cell.
            col: Column index of the current cell.
            visited: Set of already visited (row, col) positions.
            blocked: Set of blocked cells (cannot open any wall)
        Returns:
            List of tuples for each valid neighbour.
        """

        neighbours: list[tuple[Wall, int, int]] = []
        for direction, (dr, dc) in DELTA.items():
            new_row = row + dr
            new_col = col + dc
            # Must be inside the grid and not visited yet
            if (0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and (new_row, new_col) not in visited
                    and (new_row, new_col) not in blocked):
                neighbours.append((direction, new_row, new_col))
        return neighbours

    def _check_pattern_fits(self) -> bool:
        """Check if the maze is large enough to fit the 42 pattern.
        Returns:
            True if the pattern fits, False otherwise.
        """

        if (self.width - 2 >= PATTERN_WIDTH
                and self.height - 2 >= PATTERN_HEIGHT):
            return True
        print("\n=== Scheizeschlage man, pattern doesnt fit ===\n")
        return False

    def _stamp_pattern(self, blocked: set[tuple[int, int]]) -> None:
        """Populate the blocked set with cells forming the 42 pattern.
        Calculates the centered position and marks all pattern cells
        as blocked so the generator routes around them.
        Args:
            blocked: Set to populate with (row, col)
            positions of pattern cells.
        """

        start_row = (self.height - PATTERN_HEIGHT) // 2
        start_col = (self.width - PATTERN_WIDTH) // 2

        for r, row in enumerate(PATTERN):
            for c, cell in enumerate(row):
                if cell == 'X':
                    blocked.add((start_row + r, start_col + c))

    def _add_loops(self, blocked: set[tuple[int, int]]) -> None:
        candidates = []
        for r in range(self.height - 1):
            for c in range(self.width):
                if (r, c) not in blocked and (r+1, c) not in blocked:
                    if self.grid[r][c] & Wall.SOUTH:
                        candidates.append((r, c, Wall.SOUTH))

        for r in range(self.height):
            for c in range(self.width - 1):
                if (r, c) not in blocked and (r, c+1) not in blocked:
                    if self.grid[r][c] & Wall.EAST:
                        candidates.append((r, c, Wall.EAST))

        random.shuffle(candidates)

        target = len(candidates) // 7
        removed = 0

        for r, c, direction in candidates:
            if removed >= target:
                break

            dr, dc = DELTA[direction]
            nr, nc = r + dr, c + dc

            self.grid[r][c] &= ~direction
            self.grid[nr][nc] &= ~OPPOSITE[direction]

            # CHeck all nearby 3x3 blocks
            created_open_area = False
            for br in range(max(0, r - 2), min(self.height - 2, r + 1)):
                for bc in range(max(0, c - 2), min(self.width - 2, c + 1)):
                    if self._creates_3x3_area(br, bc):
                        created_open_area = True
                        break
                if created_open_area:
                    break

            if created_open_area:
                # UNDO
                self.grid[r][c] |= direction
                self.grid[nr][nc] |= OPPOSITE[direction]
            else:
                removed += 1

    def _creates_3x3_area(self, br: int, bc: int) -> bool:
        """Return True if the 3x3 block at (br, bc) is fully open"""
        for r in range(br, br + 3):
            for c in range(bc, bc + 2):
                if self.grid[r][c] & Wall.EAST:
                    return False
        for r in range(br, br + 2):
            for c in range(bc, bc + 3):
                if self.grid[r][c] & Wall.SOUTH:
                    return False
        return True

    def __str__(self) -> str:
        is_perfect = "Perfect" if self.perfect else "Not perfect"
        return (
            f"Width:\t{self.width}\n"
            f"Height:\t{self.height}\n"
            f"Entry:\t{self.entry}\n"
            f"Exit:\t{self.exit}\n"
            f"File:\t{self.output_file}\n"
            f"Type:\t{is_perfect}\n"
            f"Seed:\t{self.seed}\n"
        )
