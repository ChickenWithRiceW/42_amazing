from src.config import loading_setup
from mazegen import MazeGenerator, write_maze
from src.display import render_maze
from src.mazegen.solver import Solver

if __name__ == "__main__":
    cfg = loading_setup("config.txt")
    if not cfg:
        exit(0)
    gen = MazeGenerator(
        cfg.width,
        cfg.height,
        cfg.entry,
        cfg.exit,
        cfg.output_file,
        cfg.perfect,
        None   # ! keine seed attribute in Config bitte fixen danke
    )
    print(gen)
    gen.generate()
    print("\nGrid:", gen.grid, sep="\n")
    # write_maze(gen, ['P', 'E', 'N', 'I', 'S'])
    solv = Solver(gen.grid)
    path = solv.solver((0, 0), (30, 30))
    render_maze(gen, path, True, "magenta", "red")
