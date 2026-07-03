import sys
from src.config import loading_setup
from mazegen import MazeGenerator, write_maze
from mazegen.solver import Solver, NoSolutionError
from src.display import render_maze

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        sys.exit(1)

    cfg = loading_setup(sys.argv[1])
    if not cfg:
        sys.exit(1)

    gen = MazeGenerator(
        cfg.width,
        cfg.height,
        cfg.entry,
        cfg.exit,
        cfg.output_file,
        cfg.perfect,
        cfg.seed
    )
    gen.generate()

    try:
        solver = Solver(gen)
        path = solver.solver(gen.entry, gen.exit)
    except NoSolutionError as e:
        print(f"Error: {e}")
        sys.exit(1)

    write_maze(gen)
    render_maze(gen, path, True, "magenta", "blue")
