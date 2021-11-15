from dataclasses import dataclass

from src.core.actions.executable import Executable
from src.core.models import ActionExecution
from src.core.template_models import Branch, Pattern


@dataclass
class DeleteBranchParameters:
    source: Branch
    pattern: Pattern


class DeleteBranch(Executable):
    parameters: DeleteBranchParameters

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = DeleteBranchParameters(
            source=Branch(action_parameters.get("source", {})),
            pattern=Pattern(action_parameters.get("pattern", {})),
        )

    def execute(self):
        pass  # this method will be implemented on version 1.1.0
