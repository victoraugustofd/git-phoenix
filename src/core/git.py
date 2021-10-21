import git
from git import GitCommandError, Repo

from src.core import NotAGitRepoException

GIT_REPO: Repo


def get_config(key):
    try:
        return GIT_REPO.git.config(key)
    except GitCommandError:
        return "Config not found"


def require_git_repo():
    if not _is_git_repo():
        raise NotAGitRepoException()


def _is_git_repo():
    try:
        global GIT_REPO
        GIT_REPO = Repo(".", search_parent_directories=True)
        return True
    except git.exc.InvalidGitRepositoryError:
        return False
