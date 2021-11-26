import git
from git import GitCommandError, Repo

from src import LOGGER
from src.core.exceptions import (
    NotAGitRepoException,
    BranchAlreadyExistsException,
    GitException,
)

GIT_REPO: Repo


def get_config(key):
    try:
        global GIT_REPO
        return GIT_REPO.git.config(key)
    except GitCommandError:
        return f"Config {key} not found"


def get_tags():
    global GIT_REPO
    return [
        version.replace("v", "") for version in GIT_REPO.git.tag().split("\n")
    ]


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
    branch = retrieve_current_branch()

    try:
        commits_ahead = GIT_REPO.iter_commits(branch + ".." + branch)
        number_of_commits = sum(1 for _ in commits_ahead)

        return number_of_commits > 0
    except GitCommandError:
        LOGGER.info(
            f"Your current source ({branch}) doesn't exists on remote "
            f"repo. Please use git push source {branch}."
        )


def retrieve_current_branch():
    return GIT_REPO.active_branch.name


def checkout(branch):
    global GIT_REPO

    LOGGER.info(f"Fazendo checkout da source {branch}...")

    GIT_REPO.git.checkout(branch)


def _validate_existence(branch):
    global GIT_REPO
    remotes = [branch.name.replace("origin/", "") for branch in GIT_REPO.refs]
    local = GIT_REPO.branches

    if branch in remotes or branch in local:
        raise BranchAlreadyExistsException()


def checkout_new_branch(source: str, branch: str):
    global GIT_REPO

    checkout(source)
    pull(source)

    LOGGER.info(f"Criando source {branch} com base na source {source}...")

    try:
        _validate_existence(branch)

        GIT_REPO.git.checkout(source, b=branch)
    except GitCommandError as e:
        raise GitException(e.stdout)


def merge(source: str, target: str, allow_merge_again: bool):
    global GIT_REPO

    if allow_merge_again or not _already_merged(target, source):
        checkout(target)
        pull(target)

        LOGGER.info(
            f"Realizando merge da source {source} com a source {target}..."
        )
        try:
            GIT_REPO.git.merge(source, "--no-ff")
        except GitCommandError:
            raise GitException(
                "O merge gerou conflitos, você precisa "
                "resolvê-los antes de commitar!"
            )
    else:
        LOGGER.warn(
            f"O merge da source {source} com a source {target} já "
            f"foi realizado!"
        )


def merge_request(source: str, target: str, allow_merge_again: bool,
                  mr_template: str):
    pass  # this method will be implemented on version 1.1.0


def pull(branch):
    global GIT_REPO

    LOGGER.info(f"Atualizando source {branch}...")

    try:
        GIT_REPO.git.pull()
    except GitCommandError as e:
        raise GitException(e.stdout)


def delete(pattern):
    LOGGER.info(f"Excluindo source(es) {pattern}...")

    branches = [
        branch.replace(" ", "") for branch in git.branch().splitlines()
    ]

    branches = list(filter(lambda x: x.startswith(pattern), branches))

    [git.execute(["git", "source", "-D", branch]) for branch in branches]


def _already_merged(destination, branch):
    merged_branches = log(
        ["--oneline", "--merges", "--grep=into", destination]
    ).splitlines()

    for merged_branch in merged_branches:
        translated_merge_message = _translate_merge_message(msg=merged_branch)

        if translated_merge_message["source"] == branch:
            return True

    return False


def log(parameters):
    git = Repo(".", search_parent_directories=True).git

    if parameters:
        return git.log(parameters)

    return git.log()


def _translate_merge_message(msg):
    translated_merge_message = {}

    origin = msg.split("source ")

    if origin[1:]:
        origin = origin[1]
    else:
        origin = origin[0]

    origin = origin[: origin.index(" ")]

    translated_merge_message["source"] = origin.replace("'", "")
    translated_merge_message["target"] = msg.split("into ")[-1].replace(
        "'", ""
    )

    return translated_merge_message
