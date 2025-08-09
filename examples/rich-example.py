import numpy as np
import polars as pl
from rich import inspect
from rich import print as rprint
from rich.pretty import pprint
from dataclasses import dataclass


@dataclass
class Animal:
    legs: int
    claws: bool
    sound: str


cat = Animal(4, True, "Meow")

inspect(cat)

example_array = np.full((3, 3), np.nan)

example_array[1, 1] = 5

inspect(example_array)

example_dict = {"apples": 10, "bananas": 5, "coconuts": 2, "durian": 47}

pprint(example_dict, expand_all=True)

df = pl.DataFrame(
    {
        "foo": [1, 2, 3],
        "bar": [6, 7, 8],
        "ham": ["a", "b", "c"],
    }
)

rprint(df)
