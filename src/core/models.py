from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Execution:
    command: Dict = None
    action: Dict = None
    variables: Dict = None
    arguments: List[str] = None


@dataclass
class ActionExecution:
    variables: Dict = None
    parameters: Dict = None
    arguments: List[str] = None


@dataclass
class Choice:
    index: int = 0
    choice: str = None
    text: str = None