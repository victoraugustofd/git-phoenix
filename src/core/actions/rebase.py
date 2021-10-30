from src.core.actions.executable import Executable
from src.core.logger import Logger


class Rebase(Executable):

    def __init__(self, execution):
        super().__init__(execution)

    def execute(self):
        Logger.warn(cls=Rebase, msg="Not implemented yet!")

    def _parse(self):
        pass
