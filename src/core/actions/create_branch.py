from dataclasses import dataclass

from src.core.actions.executable import Executable
from src.core.actions.executable import _validate_pattern
from src.core.models import ActionExecution
from src.core.px_git import checkout_new_branch
from src.core.px_questionary import confirm
from src.core.template_models import Branch, Affix, Pattern


@dataclass
class CreateBranchParameters:
    name: str
    source: Branch
    affix: Affix
    pattern: Pattern


class CreateBranch(Executable):
    parameters: CreateBranchParameters

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = CreateBranchParameters(
            name=action_parameters.get("name", ""),
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
            final_name = [name]

            if affix.prefix:
                final_name = affix.prefix + final_name
                name = affix.join_char.join(final_name)
            if affix.suffix:
                final_name.extend(affix.suffix)
                name = affix.join_char.join(final_name)

        confirmed = confirm(
            msg=f"Você confirma a criação da "
            f"branch {name} com base na "
            f"branch {source.name}?"
        )

        if confirmed:
            checkout_new_branch(source=source.name, branch=name)
