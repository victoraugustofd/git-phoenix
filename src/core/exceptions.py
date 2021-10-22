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
    message: str = "You have unstaged files! Please commit them before proceeding."



@dataclass
class BranchAheadException(PhoenixException):
    message: str = "You are ahead of remote branch! Please push your changes before proceeding."

