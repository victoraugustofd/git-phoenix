from abc import ABC
from dataclasses import dataclass
from typing import List, Type, Dict

from core.enums import Action, TagReference, TagIncrement


@dataclass
class Affix:
    prefix: List[str] = None
    suffix: List[str] = None
    join_char: str = None


@dataclass
class Pattern:
    regex: str = None
    message: str = None
    example: str = None


@dataclass
class Branch:
    name: str = None
    pattern: Type[Pattern] = None


@dataclass
class Parameters(ABC):
    pass


@dataclass
class CreateBranchParameters:
    name: str = None
    source: Type[Branch] = None
    affix: Type[Affix] = None
    pattern: Type[Pattern] = None


@dataclass
class DeleteBranchParameters:
    source: Type[Branch] = None
    pattern: Type[Pattern] = None


@dataclass
class MergeParameters:
    source: Type[Branch] = None
    target: List[Branch] = None
    allow_new_merge: bool = None


@dataclass
class MergeRequestParameters:
    source: Type[Branch] = None
    target: Type[Branch] = None
    mr_template: str = None


@dataclass
class TagParameters:
    reference: Type[TagReference] = None
    increment: Type[TagIncrement] = None
    target: List[Branch] = None


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
