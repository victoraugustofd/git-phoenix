from dataclasses import dataclass, field
from typing import List


class PhoenixException(Exception):
    message: str


class PhoenixWarningException(PhoenixException):
    message: str


@dataclass
class NotAGitRepoException(PhoenixException):
    message: str = "Not a git repo!"


@dataclass
class InvalidTemplateException(PhoenixException):
    message: str = "Invalid Phoenix template!"


@dataclass
class InvalidPatternException(PhoenixException):
    message: str = "Invalid pattern!"


@dataclass
class InvalidExecutionException(PhoenixException):
    message: str = "Invalid execution!"


@dataclass
class InvalidOptionException(PhoenixWarningException):
    option: str = ""
    options: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.message = (
            f"Invalid option: {self.option} | Valid options: "
            f"{'|'.join(self.options)}"
        )


@dataclass
class CommandNotFoundException(PhoenixException):
    command: str

    def __post_init__(self):
        self.message = f"Command {self.command} not found!"


@dataclass
class ActionNotFoundException(PhoenixException):
    action: str

    def __post_init__(self):
        self.message = f"Action {self.action} not found!"


@dataclass
class UnstagedFilesException(PhoenixException):
    message: str = (
        "You have unstaged files! Please commit them before proceeding."
    )


@dataclass
class BranchAheadException(PhoenixException):
    message: str = (
        "You are ahead of remote source! Please push your "
        "changes before proceeding."
    )


@dataclass
class ShowHelpException(PhoenixException):
    message: str


@dataclass
class InvalidVariableException(PhoenixException):
    message: str


@dataclass
class MethodNotImplementedException(PhoenixException):
    message: str


@dataclass
class BranchAlreadyExistsException(PhoenixException):
    message: str = "Branch already exists"


@dataclass
class ProcessCancelledException(PhoenixWarningException):
    message: str


@dataclass
class GitException(PhoenixException):
    message: str


@dataclass
class NonPassedArgumentsException(PhoenixException):
    message: str = "You must pass arguments for Phoenix to process!"
