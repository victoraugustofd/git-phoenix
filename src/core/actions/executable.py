from abc import ABC
from typing import List, Dict

from regex import regex

from src import LOGGER
from src.core import template_methods
from src.core.exceptions import (
    InvalidPatternException,
    InvalidVariableException,
    InvalidTemplateException,
    MethodNotImplementedException,
)
from src.core.models import ActionExecution, Choice
from src.core.px_questionary import select
from src.core.template_models import Pattern, Branch
from src.core.utils import list_functions

AVAILABLE_METHODS = list_functions(template_methods)


def _adjust_regex(r: str) -> str:
    if not r.startswith("^"):
        r = "^" + r
    if not r.endswith("$"):
        r += "$"
    return r.replace("/", "\\/")


def _validate_pattern(pattern: Pattern, text: str, msg: str):
    if pattern.regex:
        r = _adjust_regex(pattern.regex)
        p = regex.compile(r)

        if not p.match(text):
            if pattern.message:
                msg = pattern.message

            raise InvalidPatternException(
                f"Invalid text: {text} | {msg} | Example: {pattern.example}"
            )


def _validate_branch_patterns(branches: List[Branch], msg: str):
    for branch in branches:
        _validate_pattern(branch.pattern, branch.name, msg)


def _is_regex(value: str) -> bool:
    return value.startswith("^") and value.endswith("$")


def _ismethod(value: str) -> bool:
    return value.startswith("@")


def _isvariable(value: str) -> bool:
    return "$" in value and not value.endswith("$")


def _ismultiplechoice(value: str) -> bool:
    return " or " in value


class Executable(ABC):
    def __init__(self, action_execution: ActionExecution):
        self.action_execution = action_execution
        self.is_implemented = True
        self.index_method_executed = 0
        self._parse_action_parameters()

    def execute(self):
        raise NotImplementedError("This is an abstract method!")

    def _parse_action_parameters(self):
        LOGGER.info("Realizando parse da ação no template...")

        self.action_execution.parameters = {
            k: self._change_value(v)
            for k, v in self.action_execution.parameters.items()
        }

    def _search_variable(self, variable: str) -> str:
        try:
            return self.action_execution.variables[variable]
        except KeyError:
            raise InvalidVariableException(
                f"Variable {variable} not found on " "template"
            )

    def _change_value(self, value, execute: bool = True):
        if isinstance(value, str):
            return self._process_str(value, execute)
        elif isinstance(value, list):
            return self._process_list(value, execute)
        elif isinstance(value, dict):
            return self._process_dict(value, execute)

        return value

    def _process_str(self, value: str, execute: bool = True) -> str:
        LOGGER.debug(f"Processando parse de string {value}...")

        if _ismultiplechoice(value):
            return self._process_multiple_choice(value)
        elif _ismethod(value):
            return self._process_method(value, execute)
        elif _isvariable(value):
            return self._process_variable(value)

        return value

    def _process_list(self, value: List, execute: bool = True) -> List:
        LOGGER.debug(f"Processando parse de lista {value}...")

        return [self._change_value(item, execute) for item in value]

    def _process_dict(self, value: Dict, execute: bool = True) -> Dict:
        LOGGER.debug(f"Processando parse de dicionário {value}...")

        return {k: self._change_value(v, execute) for k, v in value.items()}

    def _process_multiple_choice(self, value: str) -> str:
        LOGGER.debug(f"Processando parse de escolhas {value}...")

        begin = 0
        end = len(value)

        if value.startswith("("):
            begin = 1
        if value.endswith(")"):
            end = -1

        value = value[begin:end]

        if "user_input" in value and self.action_execution.arguments:
            index = self.index_method_executed
            self.index_method_executed += 1
            return self.action_execution.arguments[index]

        choices = {}
        choice_index = 1

        for choice in value.split(" or "):
            choices[str(choice_index)] = Choice(
                choice_index, choice, self._change_value(choice, execute=False)
            )

            choice_index += 1

        choice = select(
            "Escolha uma das opções abaixo:",
            choices=[f"{k}. {v.text}" for k, v in choices.items()],
        )

        user_choice = choices.get(
            choice.get("answer").split(".")[0]
        ).choice_text

        return self._change_value(user_choice)

    def _process_method(self, value: str, execute: bool = True) -> str:
        LOGGER.debug(f"Processando parse método {value}...")

        method_definition = value.split("@")[1]
        method_name = method_definition[0 : method_definition.find("(")]

        if method_name not in AVAILABLE_METHODS:
            raise MethodNotImplementedException()

        if "user_input" == method_name and self.action_execution.arguments:
            return self.action_execution.arguments[self.index_method_executed]

        original_arguments = method_definition[
            method_definition.find("(") + 1 : method_definition.find(")")
        ]

        # refs.: https://stackoverflow.com/a/48838456/7973282
        parsed_arguments = eval("dict({})".format(original_arguments))

        parsed_arguments = {
            k: self._change_value(v) for k, v in parsed_arguments.items()
        }

        parsed_arguments["execute"] = execute

        parsed_arguments = ",".join(
            [
                f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}"
                for k, v in parsed_arguments.items()
            ]
        )

        method_definition = f"{method_name}({parsed_arguments})"

        try:
            return eval(f"template_methods.{method_definition}")
        except TypeError as e:
            LOGGER.error(str(e))
            raise InvalidTemplateException()

    def _process_variable(self, value: str) -> str:
        LOGGER.debug(f"Processando parse de variável {value}...")

        variables = value.split("$")[1:]

        if "self" == variables[0]:
            pass  # this method will be implemented on version 1.1.0
        elif "version" == variables[0]:
            pass  # this method will be implemented on version 1.1.0
        else:
            for variable in variables:
                var = variable.replace("/", "")
                v = self._change_value(self._search_variable(var))

                if _is_regex(v):
                    v = v.replace("^", "").replace("$", "")

                value = value.replace(f"${var}", v)

        return value


def test():
    pass
