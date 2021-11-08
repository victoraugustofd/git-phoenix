import git
from git import GitCommandError, Repo

from src.core.exceptions import (
    NotAGitRepoException,
    BranchAlreadyExistsException,
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
    try:
        branch = retrieve_current_branch()

        commits_ahead = GIT_REPO.iter_commits(
            "source/" + branch + ".." + branch
        )
        number_of_commits = sum(1 for c in commits_ahead)

        return number_of_commits > 0
    except GitCommandError:
        print(
            f"Your current branch ({branch}) doesn't exists on remote "
            f"repo. Please use git push source {branch}."
        )


def retrieve_current_branch():
    return GIT_REPO.active_branch.name


def checkout(branch):
    # Logger.info(
    #     self=GitCommons,
    #     msg=(
    #         "Checking out branch"
    #         + PythonCommons.LIGHT_CYAN
    #         + " {}"
    #         + PythonCommons.NC
    #         + "..."
    #     ).format(branch),
    # )

    GIT_REPO.git.checkout(branch)


def _validate_existence(branch):
    global GIT_REPO
    remotes = [branch.name.replace("origin/", "") for branch in GIT_REPO.refs]
    local = GIT_REPO.branches

    if branch in remotes or branch in local:
        raise BranchAlreadyExistsException()


def checkout_new_branch(source, branch):
    checkout(source)
    pull(source)
    # Logger.info(
    #     self=GitCommons,
    #     msg=(
    #         "Creating branch"
    #         + PythonCommons.LIGHT_CYAN
    #         + " {} "
    #         + PythonCommons.NC
    #         + "based on"
    #         + PythonCommons.LIGHT_CYAN
    #         + " {}"
    #         + PythonCommons.NC
    #         + "..."
    #     ).format(branch, source),
    # )
    try:
        _validate_existence(branch)

        GIT_REPO.git.checkout(source, b=branch)
    except GitCommandError:
        pass
        # Logger.error(
        #     self=GitCommons,
        #     msg=(
        #         "Branch"
        #         + PythonCommons.LIGHT_CYAN
        #         + " {} "
        #         + PythonCommons.NC
        #         + "already exists!"
        #     ).format(branch),
        # )


def merge(branch, target, allow_merge_again):
    git = Repo(".", search_parent_directories=True).git

    if allow_merge_again or not _already_merged(target, branch):
        checkout(target)
        pull(target)
        Logger.info(
            cls=GitCommons,
            msg=(
                "Merging branch"
                + PythonCommons.LIGHT_CYAN
                + " {} "
                + PythonCommons.NC
                + "into"
                + PythonCommons.LIGHT_CYAN
                + " {}"
                + PythonCommons.NC
                + "..."
            ).format(branch, target),
        )

        try:
            git.merge(branch, "--no-ff")
        except:
            Logger.warn(
                cls=GitCommons,
                msg="You have conflicts on your working tree! Resolve them before commiting!",
            )
            raise ExecutionException()
    else:
        Logger.warn(
            cls=GitCommons,
            msg=(
                "Branch"
                + PythonCommons.LIGHT_CYAN
                + " {} "
                + PythonCommons.NC
                + "already merged into"
                + PythonCommons.LIGHT_CYAN
                + " {}"
                + PythonCommons.NC
                + "!"
            ).format(branch, target),
        )


def pull(branch):
    # Logger.info(
    #     self=GitCommons,
    #     msg=(
    #         "Updating branch "
    #         + PythonCommons.LIGHT_CYAN
    #         + "{}"
    #         + PythonCommons.NC
    #         + "..."
    #     ).format(branch),
    # )
    try:
        GIT_REPO.git.pull()
    except GitCommandError:
        pass


def delete(pattern):
    git = Repo(".", search_parent_directories=True).git
    Logger.info(
        cls=GitCommons,
        msg=(
            "Deleting branch(es) "
            + PythonCommons.LIGHT_CYAN
            + "{}"
            + PythonCommons.NC
            + "..."
        ).format(pattern),
    )

    branches = [
        branch.replace(" ", "") for branch in git.branch().splitlines()
    ]
    branches = list(filter(lambda x: x.startswith(pattern), branches))
    [git.execute(["git", "branch", "-D", branch]) for branch in branches]


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

    origin = msg.split("branch ")

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
