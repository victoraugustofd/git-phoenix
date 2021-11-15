from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Execution:
    command: Dict
    action: Dict
    variables: Dict
    arguments: List[str]


@dataclass
class ActionExecution:
    variables: Dict
    parameters: Dict
    arguments: List[str]


@dataclass
class Choice:
    index: int = 0
    choice_text: str = ""
    text: str = ""
