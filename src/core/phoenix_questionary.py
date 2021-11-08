from typing import List

from questionary import form as f, select as s, confirm as c, text as t

from src import CUSTOM_STYLE
from src.core.utils import raiser
from src.core.exceptions import ProcessCancelledException


def select(msg: str = None, choices: List[str] = None):
    answer = f(
        answer=s(
            msg,
            choices=choices,
            style=CUSTOM_STYLE,
        )
    ).ask(kbi_msg="")

    return _return(answer)


def confirm(msg: str = None):
    answer = c(message=msg, style=CUSTOM_STYLE).ask(kbi_msg="")
    return _return(answer)


def text(msg: str = None):
    answer = t(message=msg, qmark="●", style=CUSTOM_STYLE).ask(kbi_msg="")
    return _return(answer)


def _return(answer):
    return (
        answer
        if answer
        else raiser(
            ProcessCancelledException("Usuário cancelou o processamento!")
        )
    )
