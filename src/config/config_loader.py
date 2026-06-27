from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError
from typing import Annotated
import sys

class Config(BaseModel):
    def __init__(self, file_name):
        cfg = load_config(file_name)
        # print(cfg)
        super().__init__(**cfg)

    # The constrains will need to be more precise, maze cant be 2x2
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
    def split_entry(cls, v):
        return tuple(map(int, v.split(",")))

    @model_validator(mode="after")
    def validate(self) -> "Config":
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT cannot be the same")
        else:
            return self


@staticmethod
def load_config(file_name: str) -> dict[str, str]:
    """Parses the given config file and returns a dict of k, v pairs
    
    Returns stripped value, key pair. It does not support the "" operator
    and also strips all spaces.
    """

    allowed = {
    "width",
    "height",
    "entry",
    "exit",
    "output_file",
    "perfect"
    }

    cfg = {}

    with open(file_name) as f:
        for line in f:
            # Remove any trailing white spaces
            line = line.strip().lower()

            # If empty or is a comment skip
            if not line or line.startswith('#'):
                continue

            key, _, val = line.partition("=")

            # Checks if the partition method actually found the seperator
            if not val:
                continue
            # Checks if key is relevant to our config
            if key in allowed:
                # Strips any spaces again and removes comments
                val = val.strip().split(" ", 1)[0]
                cfg[key.strip()] = val
                cfg.update()
    return cfg