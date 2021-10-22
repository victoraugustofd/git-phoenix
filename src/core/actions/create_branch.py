import regex
import sys
from .executable import Executable
from commons.git import GitCommons
from src.core import Logger
from commons.phoenix import PhoenixCommons
from commons.python import PythonCommons


class CreateBranch(Executable):

    def __init__(self, execution, action_execution):
        super().__init__(execution, action_execution)

    def execute(self):

        if hasattr(self, "origin_pattern"):
            pattern = regex.compile(self.origin_pattern)

            if not pattern.match(self.origin):
                pattern_msg = None

                if hasattr(self, "origin_pattern_example"):
                    pattern_msg = self.origin_pattern_example
                else:
                    pattern_msg = self.origin_pattern

                Logger.warn(cls=Checkout, msg=("You are on branch" +
                                            PythonCommons.LIGHT_CYAN +
                                            " {}" +
                                            PythonCommons.NC +
                                            ". Checkout a branch with this name pattern: " +
                                            PythonCommons.LIGHT_CYAN +
                                            "{}" +
                                            PythonCommons.NC).format(self.origin, pattern_msg))
                Logger.error(cls=Checkout, msg="Invalid origin! Please execute the command with a valid origin branch!")

        if hasattr(self, "pattern"):
            pattern = regex.compile(self.pattern)

            if not pattern.match(self.name):
                pattern_msg = None

                if hasattr(self, "pattern_example"):
                    pattern_msg = self.pattern_example
                else:
                    pattern_msg = self.pattern

                Logger.warn(cls=Checkout, msg=("Use this name pattern: " +
                                               PythonCommons.LIGHT_CYAN +
                                               "{}" +
                                               PythonCommons.NC).format(pattern_msg))
                Logger.error(cls=Checkout, msg=("Invalid name (" +
                                                PythonCommons.LIGHT_CYAN +
                                                "{}" +
                                                PythonCommons.NC +
                                                ")! Please enter a valid branch name!").format(self.name))

            if hasattr(self, "prefix"):
                self.name = self.prefix + "/" + self.name

        GitCommons.checkout_new_branch(origin=self.origin, branch=self.name)

    def _parse(self):

        if not hasattr(self, "name"):
            if [] == self.execution.args[1:]:
                self.name = PythonCommons.read_input(cls=Checkout, msg="Inform the branch name:")
            else:
                self.origin = self.execution.args[1]
        else:
            self.name = "".join(self.name)

        # Check if origin was parsed on the execution
        if not hasattr(self, "origin"):
            if [] == self.execution.args[1:]:
                self.origin = PythonCommons.read_input(cls=Checkout, msg="Inform the origin branch name:")
            else:
                self.origin = self.execution.args[1]

        if hasattr(self, "origin_pattern"):
            self.origin_pattern = PhoenixCommons.determine_pattern(self.origin_pattern)

        if hasattr(self, "prefix"):
            self.prefix = PhoenixCommons.determine_prefix(self.prefix)

        if hasattr(self, "pattern"):
            self.pattern = PhoenixCommons.determine_pattern(self.pattern)

    def confirm_execution(self):
        name = self.name

        if hasattr(self, "prefix"):
            name = self.prefix + "/" + self.name

        return super()._confirm_execution(cls=Checkout, msg=("Confirm creating branch" +
                                                             PythonCommons.LIGHT_CYAN +
                                                             " {} " +
                                                             PythonCommons.NC +
                                                             "based on" +
                                                             PythonCommons.LIGHT_CYAN +
                                                             " {}" +
                                                             PythonCommons.NC +
                                                             "?").format(name, self.origin))
