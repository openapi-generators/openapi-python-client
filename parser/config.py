from dataclasses import dataclass
from typing import Sequence


@dataclass
class Config:
    include_methods: Sequence[str] = ("get",)
