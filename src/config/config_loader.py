from pydantic import BaseModel, Field, model_validator, field_validator, \
    ValidationError
from typing import Annotated, Self
from rich.console import Console

# Instance to use stderr without clutter in code
err = Console(stderr=True)


class Config(BaseModel):
    # TODO: Change constrains to be more precise. Maze cant be 0x0
    width: int = Field(ge=0)
    height: int = Field(ge=0)
    entry: tuple[
        Annotated[int, Field(ge=0)],
        Annotated[int, Field(ge=0)],
    ]
    exit: tuple[
        Annotated[int, Field(ge=0)],
        Annotated[int, Field(ge=0)],
    ]
    output_file: str
    perfect: bool

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def split_entry(cls, v: str) -> tuple[int, int]:
        x, y = v.split(",")
        return int(x), int(y)

    @model_validator(mode="after")
    def compare_entry_and_exit(self) -> Self:
        if self.entry == self.exit:
            raise ValueError("'entry' and 'exit' cannot be the same")
        else:
            return self


def load_config(file_name: str) -> dict[str, str]:
    """Parses the given config file and returns a dict of key=value pairs

    Does not support "" operator or any spaces in the config file.
    Return key value pairs with all spaces removed.
    """

    err.print(f"Loading config file '{file_name}':")

    cfg = {}
    syntax_error = False
    with open(file_name) as f:
        for line in f:
            # Removes any white spaces and newline
            line = line.replace(' ', '').strip().lower()

            # If empty after stripping or is a comment skip
            if not line or line.startswith('#'):
                continue

            args = line.split('=')

            # checks if the list is empty
            if not args:
                continue

            # Checks key value pair has wrong syntax
            if len(args) != 2:
                err.print(f" [red][Fail][/red]: Invalid syntax: '{line}'")
                syntax_error = True
                continue

            key, value = args
            # Extracts value without comment on the same line
            if '#' in value:
                value = value[:value.find('#')]

            cfg[key] = value
    if syntax_error:
        err.print(" [yellow]Expected format[/yellow]: [blue]KEY[/blue]=VALUE")
    else:
        err.print(" [[green]Success[/green]]")

    return cfg


def loading_setup(file_name: str) -> Config | None:
    """Takes in a config file name, loads it and parses it

    Returns Config model when successful or None if parsing failed
    """
    try:
        config_file = load_config(file_name)

        err.print("\nValidating input:")
        config = Config(**config_file)
    except ValidationError as e:
        for error in e.errors():
            err.print(" [[red]Fail[/red]]", end='')

            msg: str = error.get("msg")
            key = error.get("loc")
            value = error.get("input", "None provided")

            if error.get("type") == "missing":
                err.print(f" Field {key[0]} is missing")
            else:
                err.print(f" Field {key[0]}: {msg} got: '{value}'")
    except FileNotFoundError:
        err.print(f" [red]Fail[/red]: No {file_name} found")
    else:
        err.print(" [[green]Success[/green]]")
        return config
    return None
