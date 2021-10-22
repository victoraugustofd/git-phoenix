import argparse
import importlib.resources as lib_resources
import json
import sys
from json import JSONDecodeError

import pkg_resources
from jsonschema import validate, ValidationError
from src import InvalidTemplateException
from src import PhoenixException
from src import Execution
from src import get_template
from src import require_git_repo
from src import fire_rules

from . import resources

PARSER = argparse.ArgumentParser(description="Description of your program")

PARSER.add_argument(
    "-v",
    "--version",
    help="View version of Phoenix",
    action="store_true",
    required=False,
)

PARSED_ARGS, UNKNOWN = PARSER.parse_known_args()
PHOENIX_SCHEMA = json.loads(
    lib_resources.read_text(resources, "phoenix-schema.json")
)


def _get_version():
    print("Git Phoenix " + pkg_resources.require("git-phoenix")[0].version)


def _is_argument(arg):
    return arg.startswith("-")


def _execute_args_rules():
    if PARSED_ARGS.version:
        _get_version()


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
    return "init" == args[0] and {} != template["init"]


def main():
    try:
        args = sys.argv[1:]

        if args:
            if _is_argument(args[0]):
                _execute_args_rules()
            else:
                require_git_repo()
                template = _get_template()

                try:
                    validate(instance=template, schema=PHOENIX_SCHEMA)

                    if not _validate_if_init(args, template):
                        print("Your template doesn't have an init component!")

                    # Create execution object to carry template and arguments through execution
                    execution = Execution(args, template)

                    print("Firing rules...")

                    fire_rules(execution=execution)
                except ValidationError as e:
                    raise InvalidTemplateException(e.message)
        else:
            # Logger.error(
            #     cls=Phoenix, msg="Please inform arguments to Phoenix!"
            # )
            print("Please inform arguments to Phoenix!")
    except PhoenixException as e:
        print(e.message)
    except Exception as e:
        print(str(e))
