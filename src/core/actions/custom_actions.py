from src import LOGGER
from src.core.actions.executable import Executable
from src.core.models import ActionExecution


class CustomActions(Executable):
    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)
        self.is_implemented = False

    def execute(self):
        LOGGER.warn("Not implemented yet!")
