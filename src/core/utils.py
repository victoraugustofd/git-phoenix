import inspect
import sys

from src.core.px_git import get_config


def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return [
        func.__name__
        for func in mod.__dict__.values()
        if is_mod_function(mod, func)
    ]


def raiser(ex: BaseException):
    raise ex


def capitalize_first_letter(word):
    return word[:1].upper() + word[1:]


def get_template():
    return get_config("phoenix.template-path")


def px_print(msg):
    print(msg, file=sys.stderr)
