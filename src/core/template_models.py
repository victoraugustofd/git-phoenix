from abc import ABC
from dataclasses import dataclass
from typing import List, Type, Dict

from src.core.enums import Action


@dataclass
class Affix:
    prefix: List[str]
    suffix: List[str]
    join_char: str

    def __init__(self, affix: Dict):
        self.prefix = affix.get("prefix", [])
        self.suffix = affix.get("suffix", [])
        self.join_char = affix.get("join_char", "/")


@dataclass
class Pattern:
    regex: str
    message: str
    example: str

    def __init__(self, pattern: Dict):
        self.regex = pattern.get("regex", "")
        self.message = pattern.get("message", "")
        self.example = pattern.get("example", "")


@dataclass
class Branch:
    name: str
    pattern: Pattern

    def __init__(self, branch: Dict):
        self.name = branch.get("name", "")
        self.pattern = Pattern(branch.get("pattern", {}))


@dataclass
class Parameters(ABC):
    pass


@dataclass
class Do:
    action: Type[Action]
    parameters: Type[Parameters]


@dataclass
class Execution:
    step: int
    do: Type[Do]


@dataclass
class Action:
    name: str
    alias: str
    execution: List[Execution]


@dataclass
class Command:
    name: str
    alias: str
    actions: List[Action]


@dataclass
class Init:
    execution: List[Execution]


@dataclass
class Template:
    init: Type[Init]
    commons: Dict
    commands: List[Command]
