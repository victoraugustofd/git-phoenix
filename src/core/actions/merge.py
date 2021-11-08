import re
import ast
from typing import Type, List

import questionary
from src.core.models import ActionExecution
from src.core.template_models import Branch
from src.core.phoenix import define_pattern, read_input, determine_pattern
from src.core.actions.executable import (
    Executable,
    _validate_pattern,
    _validate_branch_patterns,
)
from src.core import merge
from dataclasses import dataclass


@dataclass
class MergeParameters:
    source: Branch = None
    targets: List[Branch] = None
    allow_new_merge: bool = None


@dataclass
class MergeRequestParameters:
    source: Branch = None
    target: Branch = None
    mr_template: str = None


class Merge(Executable):
    parameters: MergeParameters = None

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = MergeParameters(
            source=Branch(action_parameters.get("source", {})),
            targets=[
                Branch(branch)
                for branch in action_parameters.get("targets", {})
            ],
            allow_new_merge=action_parameters.get("allow_new_merge", {}),
        )

    def execute(self):
        source = self.parameters.source
        targets = self.parameters.targets
        allow_new_merge = self.parameters.allow_new_merge

        _validate_pattern(source.pattern, source.name, "Source name invalid")
        _validate_branch_patterns(targets, "Target name invalid")

        confirmed = questionary.confirm(
            message=f"Você confirma o merge da "
            f"branch {source.name} com a(s) branch(es) "
            f"{[','.join(branch.name) for branch in targets]}?"
        ).ask()

        if confirmed:
            for target in targets:
                targets.pop(0)
                merge(source.name, target.name, allow_new_merge)


class MergeRequest(Executable):
    parameters: MergeRequestParameters = None

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        action_parameters = self.action_execution.parameters

        self.parameters = MergeRequestParameters(
            source=Branch(action_parameters.get("source", {})),
            target=Branch(action_parameters.get("target", {})),
            mr_template=action_parameters.get("mr_template", {}),
        )

    def execute(self):
        source = self.parameters.source
        target = self.parameters.target
        mr_template = self.parameters.mr_template

        _validate_pattern(source.pattern, source.name, "Source name invalid")
        _validate_pattern(target.pattern, target.name, "Target name invalid")

        confirmed = questionary.confirm(
            message=f"Você confirma abrir o merge request da "
            f"branch {source.name} com a(s) branch(es) "
            f"{target.name}?"
        ).ask()

        if confirmed:
            merge(source.name, target.name)
