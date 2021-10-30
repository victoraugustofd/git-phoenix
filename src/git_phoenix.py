import importlib.resources as lib_resources
import json
import sys
from json import JSONDecodeError
from typing import List, Dict

import click
import questionary
from jsonschema import validate, ValidationError
from questionary import Style

from src.core.exceptions import (
    InvalidTemplateException,
    CommandNotFoundException,
    ActionNotFoundException,
    ShowHelpException,
    PhoenixException,
)
from src.core.git import require_git_repo
from src.core.models import Execution
from src.core.phoenix import get_template
from src.core.rules import fire_rules
from . import resources

PHOENIX_SCHEMA = json.loads(
    lib_resources.read_text(resources, "phoenix-schema.json")
)
CUSTOM_STYLE = Style(
    [
        ("qmark", "fg:#673ab7 bold"),  # token in front of the question
        ("question", "fg:#673ab7 bold"),  # question text
        (
            "answer",
            "fg:#f44336 bold",
        ),  # submitted answer text behind the question
        (
            "pointer",
            "fg:#ff0000 bold",
        ),  # pointer used in select and checkbox prompts
        (
            "highlighted",
            "fg:#673ab7 bold",
        ),  # pointed-at choice in select and checkbox prompts
        ("selected", "fg:#cc5454"),  # style for a selected item of a checkbox
        ("separator", "fg:#cc5454"),  # separator in lists
        (
            "instruction",
            "",
        ),  # user instructions for select, rawselect, checkbox
        ("text", ""),  # plain text
        (
            "disabled",
            "fg:#858585 italic",
        ),  # disabled choices for select and checkbox prompts
    ]
)


def _is_argument(arg):
    return arg.startswith("-")


def _get_template():
    template_path = get_template()

    with open(template_path) as template_file:
        try:
            return json.load(template_file)
        except JSONDecodeError as e:
            raise InvalidTemplateException(
                f"{e.msg} - Error at line:"
                f" {e.lineno} "
                f"and "
                f"column: {e.colno}"
            )


def _validate_if_init(args, template):
    if "init" == args[0] and {} != template.get("init"):
        raise InvalidTemplateException()


def _get_commands(template) -> List[str]:
    choices = []

    if {} != template.get("init"):
        choices.append("init")

    choices.extend(command.get("name") for command in template.get("commands"))

    return choices


def _get_command_by_template(template) -> Dict:
    command = questionary.form(
        command_name=questionary.select(
            "Choose one of the commands below",
            choices=_get_commands(template),
            style=CUSTOM_STYLE,
        )
    ).ask()

    command = command.get("command_name")

    return _get_command_by_name(command, template)


def _get_command_by_name(command, template):
    return next(
        filter(
            lambda x: x.get("name") == command,
            template.get("commands"),
        ),
        None,
    )


def _get_actions(command) -> List[str]:
    return [action.get("name") for action in command.get("actions")]


def _get_action_by_command(command) -> Dict:
    action = questionary.form(
        action_name=questionary.select(
            "Choose one of the actions below",
            choices=_get_actions(command),
            style=CUSTOM_STYLE,
        )
    ).ask()

    action = action.get("action_name")

    return _get_action_by_name(action, command)


def _get_action_by_name(action, command):
    return next(
        filter(
            lambda x: x.get("name") == action,
            command.get("actions"),
        ),
        None,
    )


def _passed_command(args: List[str]) -> bool:
    return len(args) > 0


def _get_command_by_argument(command: str, template: Dict):
    commands = _get_commands(template)

    if command not in commands:
        raise CommandNotFoundException(command)
    else:
        return _get_command_by_name(command, template)


def _passed_action(args: List[str]) -> bool:
    return len(args) > 1


def _get_action_by_argument(action: str, command: Dict):
    actions = _get_actions(command)

    if action not in actions:
        raise ActionNotFoundException(action)
    else:
        return _get_action_by_name(action, command)


def _get_command(args, template):
    if _passed_command(args):
        command = _get_command_by_argument(args[0], template)

        if len(args) > 1 and "-h" == args[1]:
            raise ShowHelpException(command.get("help"))

        return command
    else:
        return _get_command_by_template(template)


def _get_action(args, command):
    if _passed_action(args):
        action = _get_action_by_argument(args[1], command)

        if len(args) > 2 and "-h" == args[2]:
            raise ShowHelpException(action.get("help"))

        return action
    else:
        return _get_action_by_command(command)


@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    )
)
@click.version_option(
    package_name="git-phoenix",
    prog_name="Git Phoenix",
)
def main(*args, **kwargs):
    try:
        args = sys.argv[1:]

        require_git_repo()
        template = _get_template()

        try:
            validate(instance=template, schema=PHOENIX_SCHEMA)

            command = _get_command(args=args, template=template)
            action = _get_action(args=args, command=command)
            variables = template.get("variables")
            arguments = args[2:]

            # Create execution object to carry template and
            # arguments through execution
            execution = Execution(
                command=command,
                action=action,
                variables=variables,
                arguments=arguments,
            )

            print("Firing rules...")

            fire_rules(execution)
        except ValidationError as e:
            raise InvalidTemplateException(e.message)
    except PhoenixException as e:
        print(e.message)
    except Exception as e:
        print(str(e))
