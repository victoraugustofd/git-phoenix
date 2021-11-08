from dataclasses import dataclass
from typing import List

from src.core.enums import TagIncrement, TagReference
from src.core.models import ActionExecution
from src.core.template_models import Branch
from src.core.actions.executable import Executable


@dataclass
class TagParameters:
    reference: TagReference = None
    increment: TagIncrement = None
    targets: List[Branch] = None


class Tag(Executable):
    parameters: TagParameters = None

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
        Logger.warn(cls=Tag, msg="Not implemented yet!")

    def _parse(self):
        pass
