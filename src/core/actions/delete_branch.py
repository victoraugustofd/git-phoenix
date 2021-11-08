from dataclasses import dataclass

import regex
import sys

from src.core.template_models import Branch, Pattern
from src.core.actions.executable import Executable


@dataclass
class DeleteBranchParameters:
    source: Branch = None
    pattern: Pattern = None


class DeleteBranch(Executable):

    def __init__(self, execution, action_execution):
        super().__init__(execution, action_execution)

    def execute(self):
        delete(self.pattern)

    def _parse(self):
        if hasattr(self, "pattern"):
            self.pattern = "".join(self.pattern)
        else:
            self.pattern = read_input(cls=DeleteBranch, msg="Inform the branch pattern to delete:")

    def confirm_execution(self):
        return super()._confirm_execution(cls=DeleteBranch, msg=("Confirm deleting branch(es)" +
                                                                 PythonCommons.LIGHT_CYAN +
                                                                 " {}" +
                                                                 PythonCommons.NC +
                                                                 "?").format(self.pattern))
