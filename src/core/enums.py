from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class Action(BaseEnum):
    CREATE_BRANCH = "createBranch"
    DELETE_BRANCH = "deleteBranch"
    MERGE = "merge"
    MERGE_REQUEST = "merge_request"
    TAG = "tag"


class TagReference(BaseEnum):
    BRANCH = "source"
    TAG = "tag"


class TagIncrement(BaseEnum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
