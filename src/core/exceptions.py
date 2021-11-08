from dataclasses import dataclass


class PhoenixException(BaseException):
    message: str = None


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
class CommandNotFoundException(PhoenixException):
    command: str = None

    def __post_init__(self):
        self.message = f"Command {self.command} not found!"


@dataclass
class ActionNotFoundException(PhoenixException):
    action: str = None

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
        "You are ahead of remote branch! Please push your "
        "changes before proceeding."
    )


@dataclass
class ShowHelpException(PhoenixException):
    message: str = None


@dataclass
class InvalidVariableException(PhoenixException):
    message: str = None


@dataclass
class MethodNotImplementedException(PhoenixException):
    message: str = None


@dataclass
class BranchAlreadyExistsException(PhoenixException):
    message: str = "Branch already exists"


@dataclass
class ProcessCancelledException(PhoenixException):
    message: str = None
