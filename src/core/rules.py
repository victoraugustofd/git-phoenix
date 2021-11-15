from src import LOGGER
from src.core.exceptions import UnstagedFilesException, BranchAheadException
from src.core.px_git import has_unstaged_files, is_ahead
from src.core.models import Execution, ActionExecution
from src.core.utils import capitalize_first_letter
from src.core.actions.block_commit import BlockCommit
from src.core.actions.create_branch import CreateBranch
from src.core.actions.custom_actions import CustomActions
from src.core.actions.delete_branch import DeleteBranch
from src.core.actions.merge import Merge
from src.core.actions.merge import MergeRequest
from src.core.actions.rebase import Rebase
from src.core.actions.tag import Tag


def fire_rules(execution: Execution):
    if has_unstaged_files():
        raise UnstagedFilesException()

    if is_ahead():
        raise BranchAheadException()

    actions = []

    for action_execution in execution.action.get("execution"):
        do = action_execution.get("do")
        action_from_template = do.get("action")

        LOGGER.info(f"Validando método {action_from_template}...")

        action_class = eval(capitalize_first_letter(action_from_template))

        action = action_class(
            ActionExecution(
                execution.variables, do.get("parameters"), execution.arguments
            )
        )

        if not action.is_implemented:
            LOGGER.warn("Método não implementado, favor revisar seu template!")
        else:
            actions.append(action)

    # TODO implementar informativo quando a ação não puder ser executada por
    #  determinado motivo

    for action in actions:
        action.execute()
