import re
import ast
from .executable import Executable
from commons.git import GitCommons
from src.core import Logger
from commons.phoenix import PhoenixCommons
from commons.python import PythonCommons
from exception.custom_exceptions import ExecutionException


class Merge(Executable):

    def __init__(self, execution, action_execution):
        super().__init__(execution, action_execution)

    def execute(self):
        if hasattr(self, "origin_pattern"):
            pattern = re.compile(self.origin_pattern)

            if not pattern.match(self.origin):
                pattern_msg = None

                if hasattr(self, "origin_pattern_example"):
                    pattern_msg = self.origin_pattern_example
                else:
                    pattern_msg = self.origin_pattern

                Logger.warn(cls=Merge, msg=("You are merging branch" +
                                            PythonCommons.LIGHT_CYAN +
                                            " {}" +
                                            PythonCommons.NC +
                                            ". Merge a branch with this name pattern: " +
                                            PythonCommons.LIGHT_CYAN +
                                            "{}" +
                                            PythonCommons.NC).format(self.origin, pattern_msg))
                Logger.error(cls=Merge, msg="Invalid origin! Please execute the command with a valid origin branch!")

        all_destinations = self.destination[:]

        for destination in self.destination:
            try:
                all_destinations.pop(0)
                GitCommons.merge(self.origin, destination, self.allow_merge_again)
            except ExecutionException:
                if len(all_destinations) > 0:
                    Logger.warn(cls=Merge, msg=("Due to the conflict, the branch" +
                                                PythonCommons.LIGHT_CYAN +
                                                " {} " +
                                                PythonCommons.NC +
                                                "couldn't be merged with branch(es)" +
                                                PythonCommons.LIGHT_CYAN +
                                                " {}" +
                                                PythonCommons.NC +
                                                "!").format(self.origin, ", ".join(all_destinations)))

                raise ExecutionException()

    def _parse(self):
        if not hasattr(self, "origin"):
            if [] == self.execution.args[0:]:
                self.origin = PythonCommons.read_input(cls=Merge, msg="Inform the origin branch name:")
            else:
                self.origin = self.execution.args[0]

        if hasattr(self, "origin_pattern"):
            self.origin_pattern = PhoenixCommons.determine_pattern(self.origin_pattern)

        if not hasattr(self, "destination"):
            if not hasattr(self, "destination_strategy"):
                if [] == self.execution.args[1:]:
                    self.destination = PythonCommons.read_input(cls=Merge, msg="Inform the destination branch(es):").split(" ")
                else:
                    self.destination = [self.execution.args[1]]
            else:
                strategy = self.destination_strategy["strategy"]

                if strategy == "search_pattern":
                    pattern = self.destination_strategy["pattern"]

                    for i in range(len(pattern)):
                        pattern[i] = self.change_value(pattern[i])

                    index_to_search = self.destination_strategy["index"]
                    pattern_to_search = PythonCommons.define_pattern(pattern[index_to_search], False, False)

                    pattern_found = re.search(pattern_to_search, self.origin).group(0)
                    pattern[index_to_search] = pattern_found

                    self.destination = [PhoenixCommons.determine_prefix(pattern)]
                else:
                    Logger.error(cls=Merge, msg=("Strategy" +
                                                 PythonCommons.LIGHT_PURPLE +
                                                 " {} " +
                                                 PythonCommons.NC +
                                                 "not implemented yet!").format(strategy))
        if hasattr(self, "allow_merge_again"):
            self.allow_merge_again = self.allow_merge_again
        else:
            self.allow_merge_again = False

    def confirm_execution(self):
        destination = ", ".join(self.destination)

        return super()._confirm_execution(cls=Merge, msg=("Confirm merging branch" +
                                                             PythonCommons.LIGHT_CYAN +
                                                             " {} " +
                                                             PythonCommons.NC +
                                                             "into" +
                                                             PythonCommons.LIGHT_CYAN +
                                                             " {}" +
                                                             PythonCommons.NC +
                                                             "?").format(self.origin, destination))
