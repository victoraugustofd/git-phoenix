from src.core.exceptions import (
    CommandNotFoundException,
    ActionNotFoundException,
)
from src.core.git import get_config

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN_ORANGE = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
NC = "\033[0m"  # No Color


def get_template():
    return get_config("phoenix.template-path")


def get_command(commands, command_name):
    print(f"Validating command {command_name}...")

    command = next(
        filter(lambda x: x.get("name") == command_name, commands), None
    )

    if not command:
        raise CommandNotFoundException(command_name)

    return command


def get_action(actions, action_name):
    print(f"Validating action {action_name}...")

    action = next(
        filter(lambda x: x.get("name") == action_name, actions), None
    )

    if not action:
        raise ActionNotFoundException(action_name)

    return action


def read_input(cls, msg):

    user_input = None

    while not user_input:
        try:
            print(msg)
            user_input = input()
        except EOFError:
            print(f"Please, {msg}")
        except KeyboardInterrupt:
            print("Stopping execution")

    return user_input


def define_pattern(pattern, should_start, should_end):
    if isinstance(pattern, list):
        for i in range(len(pattern)):
            pattern[i] = (
                pattern[i].replace("^", "").replace("$", "").replace("/", "\/")
            )

        pattern = "".join(pattern)

    if should_start:
        pattern = "^" + pattern
    if should_end:
        pattern = pattern + "$"

    return pattern


def determine_pattern(pattern):
    if isinstance(pattern, list):
        for i in range(len(pattern)):
            pattern[i] = (
                pattern[i].replace("^", "").replace("$", "").replace("/", "\/")
            )

    pattern = "".join(pattern)
    pattern = "^" + pattern + "$"

    return pattern


def capitalize_first_letter(word):
    return word[:1].upper() + word[1:]
