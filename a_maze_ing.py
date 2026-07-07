import sys
from src.config import loading_setup
from mazegen import MazeGenerator
from src.display import run_display
from rich.console import Console

# Instance to use stderr without clutter in code
err = Console(stderr=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        sys.exit(1)

    print("Parsing config...")
    print('-'*40)
    cfg = loading_setup(sys.argv[1])
    if not cfg:
        sys.exit(1)
    print('-'*40)

    try:
        gen = MazeGenerator(
            cfg.width,
            cfg.height,
            cfg.entry,
            cfg.exit,
            cfg.output_file,
            cfg.perfect,
            cfg.seed
        )
    except ValueError as e:
        err.print(f"[red]MazeGenerator error[/red]: {e}")
        sys.exit(1)

    gen.generate()

    run_display(gen)
