from dataclasses import dataclass
from typing import Any


@dataclass
class ListItem:
    value: Any
    name: str
