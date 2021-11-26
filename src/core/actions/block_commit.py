from src import LOGGER
from src.core.actions.executable import Executable
from src.core.models import ActionExecution


class BlockCommit(Executable):
    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        self.is_implemented = False

    def execute(self):
        LOGGER.debug("Not implemented yet!")
