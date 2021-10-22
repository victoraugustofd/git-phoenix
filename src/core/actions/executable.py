import sys
from src.core import read_input
from src.core import define_pattern


class Executable:
    def __init__(self, execution, action_execution):
        self.execution = execution
        self.action_execution = action_execution
        self.is_implemented = True

        if "parameters" in self.action_execution["do"]:
            self.action_parameters = self.action_execution["do"]["parameters"]
            self._parse_action_parameters()

        self._parse()

    def execute(self):
        pass

    def _parse(self):
        pass

    def _confirm_execution(self, cls, msg):
        answer = read_input(cls=cls, msg=msg + " [[y]es/[n]o]")

        yes = {"yes", "y"}

        if answer.lower() in yes:
            return True

        return False

    def _parse_action_parameters(self):
        for parameter, value in self.action_parameters.items():
            value = self.change_value(value)
            setattr(self, parameter, value)

    def search_value(self, value):
        value_split = value.split(".")

        if "commons" == value_split[0]:
            new_value = self.change_value(
                self.execution.commons[value[len("commons.") :]]
            )

            if "join" in value_split:
                new_value = "".join(new_value)

            return new_value
        else:
            print("Parameter search is available only for commons structure")

    def change_value(self, value):
        if isinstance(value, str):
            if value.startswith("#"):
                method_name = value[1:]

                try:
                    if method_name.startswith(
                        "phoenix_"
                    ) or method_name.startswith("git_"):
                        prefix = method_name.split("_")[0].title()
                        method_name = method_name[len(prefix) + 1 :]
                        cls = prefix + "Commons"
                        method = getattr(eval(cls), method_name.split("(")[0])

                        if self._has_parameters(method_name):
                            parameters = method_name.split("(")[1][:-1].split(
                                ", "
                            )

                            for i in range(len(parameters)):
                                parameters[i] = self.change_value(
                                    parameters[i]
                                )

                            value = method(parameters)
                        else:
                            value = method()
                    else:
                        value = getattr(self, method_name)()
                except AttributeError as e:
                    print(f"Method {method_name} not found!"),

            elif value.startswith("@"):
                value = self.search_value(value[1:])
        elif isinstance(value, list):
            for i in range(len(value)):
                value[i] = self.change_value(value[i])
        elif isinstance(value, dict):
            new_value = {}

            for parameter, value in value.items():
                new_value[parameter] = self.change_value(value)

            value = new_value

        if isinstance(value, list):
            if any(isinstance(vl, list) for vl in value):
                value = [item for sublist in value for item in sublist]

        return value

    def _has_parameters(self, method):
        return "(" in method

    @property
    def execution(self):
        return self._execution

    @execution.setter
    def execution(self, execution):
        self._execution = execution

    @property
    def is_implemented(self):
        return self._is_implemented

    @is_implemented.setter
    def is_implemented(self, is_implemented):
        self._is_implemented = is_implemented

    @property
    def action_execution(self):
        return self._action_execution

    @action_execution.setter
    def action_execution(self, action_execution):
        self._action_execution = action_execution

    @property
    def action_parameters(self):
        return self._action_parameters

    @action_parameters.setter
    def action_parameters(self, action_parameters):
        self._action_parameters = action_parameters
