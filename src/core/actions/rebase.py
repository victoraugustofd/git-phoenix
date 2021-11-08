from src import LOGGER
from src.core.models import ActionExecution
from src.core.actions.executable import Executable


class Rebase(Executable):

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)

    def execute(self):
        LOGGER.warn("Not implemented yet!")
