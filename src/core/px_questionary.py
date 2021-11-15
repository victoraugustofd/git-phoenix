from typing import List, TextIO

from prompt_toolkit.output.win32 import NoConsoleScreenBufferError, Win32Output
from questionary import form as f, select as s, confirm as c, text as t

from core.utils import px_print
from src import CUSTOM_STYLE
from src.core.utils import raiser
from src.core.exceptions import (
    ProcessCancelledException,
    InvalidOptionException,
)

IS_VALID_ENV = True

try:
    Win32Output(stdout=TextIO()).get_win32_screen_buffer_info()
except NoConsoleScreenBufferError:
    IS_VALID_ENV = False


def select(msg: str, choices: List[str]):
    if IS_VALID_ENV:
        answer = f(
            answer=s(
                msg,
                choices=choices,
                style=CUSTOM_STYLE,
            )
        ).ask(kbi_msg="")

        return _return(answer)
    else:
        px_print(f"? {msg}")

        for choice in choices:
            px_print(f"» {choice}")

        answer = _input()

        if answer in choices:
            return answer
        else:
            raise InvalidOptionException(answer, choices)


def confirm(msg: str):
    answer = c(message=msg, style=CUSTOM_STYLE).ask(kbi_msg="")
    return _return(answer)


def text(msg: str):
    answer = t(message=msg, qmark="●", style=CUSTOM_STYLE).ask(kbi_msg="")
    return _return(answer)


def _return(answer):
    return (
        answer.get("answer")
        if answer
        else raiser(
            ProcessCancelledException("Usuário cancelou o processamento!")
        )
    )


def _input():
    try:
        return input("● Qual opção você deseja?")
    except (KeyboardInterrupt, EOFError):
        return raiser(
            ProcessCancelledException("Usuário cancelou o processamento!")
        )
