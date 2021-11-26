from distutils.version import LooseVersion

from src.core.px_git import get_tags
from src.core.enums import TagIncrement
from src.core.px_questionary import text


def user_input(msg: str, execute: bool = True):
    if execute:
        return text(msg=msg.replace("%", ""))
    else:
        input_variable_name = "o parâmetro"

        if msg.count("%") == 2:
            input_variable_name = msg.split("%")[1]

        return f"Você quer digitar {input_variable_name}?"


def get_latest_version(increase: str, execute: bool = True):
    if execute:
        latest_tag = max(get_tags(), key=LooseVersion)
        version = latest_tag.split(".")
        tag_increment = TagIncrement(increase.lower())

        if tag_increment == TagIncrement.MAJOR:
            version[0] = str(int(version[0]) + 1)
            version[1] = "0"
            version[2] = "0"

        elif tag_increment == TagIncrement.MINOR:
            version[1] = str(int(version[1]) + 1)
            version[2] = "0"

        else:
            version[2] = str(int(version[2]) + 1)

        return ".".join(version)
    else:
        return "Identifique a última tag para mim"


def get_latest_tag(increase: TagIncrement, execute: bool = True):
    pass  # this method will be implemented on version 1.1.0


def get_branch(pattern: str, execute: bool = True):
    pass  # this method will be implemented on version 1.1.0


def get_origin_branch(execute: bool = True):
    pass  # this method will be implemented on version 1.1.0
