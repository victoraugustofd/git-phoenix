import git
from git import GitCommandError, Repo

from src.core import NotAGitRepoException

GIT_REPO: Repo


def get_config(key):
    try:
        return GIT_REPO.git.config(key)
    except GitCommandError:
        return f"Config {key} not found"


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


def has_unstaged_files():
    unstaged_files = GIT_REPO.git.status("--porcelain")

    if not unstaged_files:
        return False

    return True


def is_ahead():
    try:
        branch = retrieve_current_branch()

        commits_ahead = GIT_REPO.iter_commits(
            "origin/" + branch + ".." + branch
        )
        number_of_commits = sum(1 for c in commits_ahead)

        return number_of_commits > 0
    except GitCommandError:
        print(
            f"Your current branch ({branch}) doesn't exists on remote "
            f"repo. Please use git push origin {branch}."
        )


def retrieve_current_branch():
    return GIT_REPO.active_branch.name
