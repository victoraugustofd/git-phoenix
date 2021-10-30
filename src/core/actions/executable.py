import re
from typing import List, Dict

from regex import regex

from src.core import template_methods
from src.core.exceptions import (
    InvalidPatternException,
    InvalidVariableException,
    MethodNotImplementedException,
)
from src.core.models import ActionExecution
from src.core.phoenix import read_input
from src.core.template_models import Pattern
from src.core.template_methods import *
from src.core.utils import list_functions

AVAILABLE_METHODS = list_functions(template_methods)


def _adjust_regex(r: str) -> str:
    if not r.startswith("^"):
        r = "^" + r
    if not r.endswith("$"):
        r += "$"
    return r.replace("/", "\/")


def _validate_pattern(pattern: Pattern, text: str, msg: str = None):
    if pattern.regex:
        r = _adjust_regex(pattern.regex)
        pattern = regex.compile(r)

        if not pattern.match(text):
            raise InvalidPatternException(msg)


def _is_regex(value: str) -> bool:
    return value.startswith("^") and value.endswith("$")


def _ismethod(value: str) -> bool:
    return value.startswith("@")


def _isvariable(value: str) -> bool:
    return "$" in value and not value.endswith("$")


def _ismultiplechoice(value: str) -> bool:
    return " or " in value


class Executable:
    def __init__(self, action_execution: ActionExecution):
        self.action_execution = action_execution
        self.is_implemented = True
        self._parse_action_parameters()

    def execute(self):
        pass

    def confirm_execution(self, cls, msg):
        answer = read_input(cls=cls, msg=msg + " [[y]es/[n]o]")

        yes = {"yes", "y"}

        if answer.lower() in yes:
            return True

        return False

    def _parse_action_parameters(self):
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

    def _change_value(self, value):
        if isinstance(value, str):
            return self._process_str(value)
        elif isinstance(value, list):
            return self._process_list(value)
        elif isinstance(value, dict):
            return self._process_dict(value)

        return value

    def _process_str(self, value: str) -> str:
        if _ismultiplechoice(value):
            return self._process_multiple_choice(value)
        elif _ismethod(value):
            return self._process_method(value)
        elif _isvariable(value):
            return self._process_variable(value)

        return value

    def _process_list(self, value: List) -> List:
        return [self._change_value(item) for item in value]

    def _process_dict(self, value: Dict) -> Dict:
        return {k: self._change_value(v) for k, v in value.items()}

    def _process_multiple_choice(self, value: str) -> str:
        if value.startswith("(") and value.endswith(")"):
            value = value[1:-1]

        for choice in value.split(" or "):
            self._change_value(choice)

    def _process_method(self, value: str) -> str:
        method_definition = value.split("@")[1]
        method_name = method_definition[0 : method_definition.find("(")]

        if method_name not in AVAILABLE_METHODS:
            raise MethodNotImplementedException()

        original_arguments = method_definition[
            method_definition.find("(") + 1 : method_definition.find(")")
        ]

        # refs.: https://stackoverflow.com/a/48838456/7973282
        parsed_arguments = eval("dict({})".format(original_arguments))

        parsed_arguments = {
            k: self._change_value(v) for k, v in parsed_arguments.items()
        }

        parsed_arguments = ",".join(
            [f"{k}='{v}'" for k, v in parsed_arguments.items()]
        )

        method_definition = method_definition.replace(
            original_arguments, parsed_arguments
        )

        return eval(method_definition)

    def _process_variable(self, value: str) -> str:
        variables = value.split("$")[1:]

        if "self" == variables[0]:
            pass
        elif "version" == variables[0]:
            pass
        else:
            for variable in variables:
                var = variable.replace("/", "")
                v = self._change_value(self._search_variable(var))

                if _is_regex(v):
                    v = v.replace("^", "").replace("$", "")

                value = value.replace("$" + var, v)

        return value

    def _has_parameters(self, method):
        return "(" in method
