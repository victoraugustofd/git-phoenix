from src.core.exceptions import UnstagedFilesException, BranchAheadException
from src.core.git import has_unstaged_files, is_ahead
from src.core.models import Execution, ActionExecution
from src.core.phoenix import capitalize_first_letter
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

        print(f"Validating method {action_from_template}...")

        action_class = eval(capitalize_first_letter(action_from_template))

        action = action_class(
            ActionExecution(
                execution.variables, do.get("parameters"), execution.arguments
            )
        )

        # if action.is_implemented:
        #     if not action.confirm_execution():
        #         Logger.warn(self=Checkout, msg="Execution stopped by user")
        #         sys.exit()

        actions.append(action)

    # all_actions = [
    #     action.action_execution.get("do").get("action")
    #     for action in actions.values()
    # ]

    for action in actions:
        # Logger.info(
        #     self=Rules,
        #     msg=(
        #         (
        #             "Executing method "
        #             + PythonCommons.LIGHT_GREEN
        #             + "{}"
        #             + PythonCommons.NC
        #             + "..."
        #         ).format(action.action_execution["do"]["action"])
        #     ),
        # )
        # try:
        action.execute()
        # except ExecutionException:
        #     if len(all_actions) > 0:
        #         Logger.error(
        #             self=Rules,
        #             msg=(
        #                 "An error has ocurred while processing! "
        #                 + "The following action(s) couldn't be executed:"
        #                 + PythonCommons.LIGHT_CYAN
        #                 + " {}"
        #                 + PythonCommons.NC
        #                 + "!"
        #             ).format(", ".join(all_actions)),
        #         )
