from src.core import has_unstaged_files
from src.core import is_ahead
from src.core import UnstagedFilesException
from src.core import BranchAheadException
from src.core import actions


def fire_rules(execution):
    if has_unstaged_files():
        raise UnstagedFilesException()

    if is_ahead():
        raise BranchAheadException()

    actions = []

    for action_execution in execution.action.get("execution"):
        action_from_template = action_execution.get("do").get("action")

        print(f"Validating method {action_from_template}...")

        action_class = eval(
            action_from_template[:1].upper() + action_from_template[1:]
        )

        action = action_class(execution, action_execution)

        if action.is_implemented:
            if not action.confirm_execution():
                Logger.warn(cls=Checkout, msg="Execution stopped by user")
                sys.exit()

            actions.append(action)

    all_actions = [
        action.action_execution.get("do").get("action")
        for action in actions.values()
    ]

    for action in actions.values():
        Logger.info(
            cls=Rules,
            msg=(
                (
                    "Executing method "
                    + PythonCommons.LIGHT_GREEN
                    + "{}"
                    + PythonCommons.NC
                    + "..."
                ).format(action.action_execution["do"]["action"])
            ),
        )
        try:
            all_actions.pop(0)
            action.execute()
        except ExecutionException:
            if len(all_actions) > 0:
                Logger.error(
                    cls=Rules,
                    msg=(
                        "An error has ocurred while processing! "
                        + "The following action(s) couldn't be executed:"
                        + PythonCommons.LIGHT_CYAN
                        + " {}"
                        + PythonCommons.NC
                        + "!"
                    ).format(", ".join(all_actions)),
                )
