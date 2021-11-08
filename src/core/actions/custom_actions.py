from src.core.models import ActionExecution
from src.core.actions.executable import Executable


class CustomActions(Executable):

    def __init__(self, action_execution: ActionExecution):
        super().__init__(action_execution)

    def execute(self):
        pass

    def _parse(self):
        pass
