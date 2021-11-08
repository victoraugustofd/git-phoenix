import importlib.resources as lib_resources
import json
import logging

import coloredlogs
from questionary import Style

from . import resources

# initialize logger
LOGGER = logging.getLogger("Git Phoenix")

# parse phoenix-schema
PHOENIX_SCHEMA = json.loads(
    lib_resources.read_text(resources, "phoenix-schema.json")
)

# refs.: https://stackoverflow.com/a/20112491/7973282
fmt = (
    "%(asctime)s :: %(name)s :: %(levelname)s - "
    "%(message)s (%(filename)s:%(lineno)d - %(funcName)s())"
)

coloredlogs.DEFAULT_FIELD_STYLES = {
    "asctime": {"color": "white"},
    "levelname": {"color": "black", "bold": True},
    "name": {"color": "red", "bold": True},
}

coloredlogs.DEFAULT_LEVEL_STYLES = {
    "info": {"color": "cyan"},
    "notice": {"color": "magenta"},
    "verbose": {"color": "blue"},
    "success": {"color": "green", "bold": True},
    "spam": {"color": "blue"},
    "critical": {"color": "red", "bold": True},
    "error": {"color": "red"},
    "debug": {"color": "green"},
    "warning": {"color": "yellow"},
}

coloredlogs.install(level="INFO", logger=LOGGER, fmt=fmt, milliseconds=True)

CUSTOM_STYLE = Style(
    [
        ("qmark", "ansibrightyellow bold"),  # token in front of the question
        ("question", "ansiwhite bold"),  # question text
        (
            "answer",
            "ansibrightmagenta bold",
        ),  # submitted answer text behind the question
        (
            "pointer",
            "ansibrightblue bold",
        ),  # pointer used in select and checkbox prompts
        (
            "highlighted",
            "ansibrightblack bold",
        ),  # pointed-at choice in select and checkbox prompts
        (
            "selected",
            "ansibrightblack",
        ),  # style for a selected item of a checkbox
        ("separator", "ansibrightmagenta"),  # separator in lists
        (
            "instruction",
            "",
        ),  # user instructions for select, rawselect, checkbox
        ("text", ""),  # plain text
        (
            "disabled",
            "ansibrightblack italic",
        ),  # disabled choices for select and checkbox prompts
    ]
)
