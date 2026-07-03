import sys
from src.config import loading_setup
from mazegen import MazeGenerator
from src.display import run_display

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

    run_display(gen)
