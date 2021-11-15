from dataclasses import dataclass
from typing import List

from src import LOGGER
from src.core.actions.executable import Executable
from src.core.enums import TagIncrement, TagReference
from src.core.models import ActionExecution
from src.core.template_models import Branch


@dataclass
class TagParameters:
    reference: TagReference
    increment: TagIncrement
    targets: List[Branch]


class Tag(Executable):
    parameters: TagParameters

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = TagParameters(
            reference=action_parameters.get("reference"),
            increment=action_parameters.get("increment"),
            targets=[
                Branch(branch)
                for branch in action_parameters.get("targets", {})
            ],
        )

    def execute(self):
        LOGGER.warn("Not implemented yet!")
