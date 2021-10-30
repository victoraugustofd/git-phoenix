from dataclasses import dataclass

from src.core.actions.executable import Executable
from src.core.actions.executable import _validate_pattern
from src.core.git import checkout_new_branch
from src.core.models import ActionExecution
from src.core.template_models import Branch, Affix, Pattern
from src.core.logger import Logger


@dataclass
class CreateBranchParameters:
    name: str = None
    source: Branch = None
    affix: Affix = None
    pattern: Pattern = None


class CreateBranch(Executable):
    parameters: CreateBranchParameters = None

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = CreateBranchParameters(
            name=action_parameters.get("name"),
            source=Branch(action_parameters.get("source", {})),
            affix=Affix(action_parameters.get("affix", {})),
            pattern=Pattern(action_parameters.get("pattern", {})),
        )

    def execute(self):
        name = self.parameters.name
        source = self.parameters.source
        affix = self.parameters.affix
        pattern = self.parameters.pattern

        _validate_pattern(source.pattern, source.name, "Source name invalid")
        _validate_pattern(pattern, name, "Name invalid")

        if affix:
            if affix.prefix:
                name = affix.join_char.join([affix.prefix, name])
            if affix.suffix:
                name = affix.join_char.join([name, affix.suffix])

        checkout_new_branch(source=source.name, branch=name)
