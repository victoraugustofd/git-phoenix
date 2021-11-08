from dataclasses import dataclass

from src.core.models import ActionExecution
from src.core.actions.executable import Executable
from src.core.template_models import Branch, Pattern


@dataclass
class DeleteBranchParameters:
    source: Branch = None
    pattern: Pattern = None


class DeleteBranch(Executable):
    parameters: DeleteBranchParameters = None

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = DeleteBranchParameters(
            source=action_parameters.get("source"),
            pattern=action_parameters.get("pattern"),
        )

    def execute(self):
        delete(self.pattern)

    def _parse(self):
        if hasattr(self, "pattern"):
            self.pattern = "".join(self.pattern)
        else:
            self.pattern = read_input(
                cls=DeleteBranch, msg="Inform the branch pattern to delete:"
            )
