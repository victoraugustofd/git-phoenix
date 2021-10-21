from dataclasses import dataclass


class PhoenixException(BaseException):
    message: str = None


@dataclass
class NotAGitRepoException(PhoenixException):
    message: str = "Not a git repo!"


@dataclass
class InvalidTemplateException(PhoenixException):
    message: str = "Invalid Phoenix template!"
