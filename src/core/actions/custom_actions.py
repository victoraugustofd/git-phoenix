from src.core.actions.executable import Executable
from src.core.logger import Logger


class CustomActions(Executable):

    def __init__(self, execution):
        super().__init__(execution)

    def execute(self):
        pass

    def _parse(self):
        pass
