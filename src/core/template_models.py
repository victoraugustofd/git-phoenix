from abc import ABC
from dataclasses import dataclass
from typing import List, Type, Dict

from src.core.enums import TagIncrement, TagReference, Action


@dataclass
class Affix:
    prefix: List[str] = None
    suffix: List[str] = None
    join_char: str = None

    def __init__(self, affix: Dict):
        self.prefix = affix.get("prefix", [])
        self.suffix = affix.get("suffix", [])
        self.join_char = affix.get("join_char", "/")


@dataclass
class Pattern:
    regex: str = None
    message: str = None
    example: str = None

    def __init__(self, pattern: Dict):
        self.regex = pattern.get("regex", "")
        self.message = pattern.get("message", "")
        self.example = pattern.get("example", "")


@dataclass
class Branch:
    name: str = None
    pattern: Pattern = None

    def __init__(self, branch: Dict):
        self.name = branch.get("name")
        self.pattern = Pattern(branch.get("pattern", {}))


@dataclass
class Parameters(ABC):
    pass


@dataclass
class Do:
    action: Type[Action] = None
    parameters: Type[Parameters] = None


@dataclass
class Execution:
    step: int = None
    do: Type[Do] = None


@dataclass
class Action:
    name: str = None
    alias: str = None
    execution: List[Execution] = None


@dataclass
class Command:
    name: str = None
    alias: str = None
    actions: List[Action] = None


@dataclass
class Init:
    execution: List[Execution] = None


@dataclass
class Template:
    init: Type[Init] = None
    commons: Dict = None
    commands: List[Command] = None
