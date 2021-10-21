from enum import Enum


class Action(Enum):
    CREATE_BRANCH = "createBranch"
    DELETE_BRANCH = "deleteBranch"
    MERGE = "merge"
    MERGE_REQUEST = "merge_request"
    TAG = "tag"


class TagReference(Enum):
    BRANCH = "branch"
    TAG = "tag"


class TagIncrement(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
