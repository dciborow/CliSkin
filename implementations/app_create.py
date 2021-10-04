from interfaces.command import ICommand, Argument, CommandArgs
from implementations.optionalparameters import GenericCommandOptionalParameters, ManagedAppCreateOptionalParameters
import json

class AzAiAppCreate(ICommand):
    def __init__(self):
        self.commands = CommandArgs(
            "First Command Arguments",
            ["az", "ai","app", "create"]
        )
        self.actual_command = ["az", "managedapp", "create"]
     
        arguments = [
            Argument(["--name"], "name", True, str, "Application name"),
            Argument("--kind", "kind", True, str, "Kind"),
            Argument("--managed-rg-id", "managed_group", True, str, "RG id for mgd")
        ]

        filtered_args = [x for x in GenericCommandOptionalParameters.PARAMETERS if x.destination not in ["name"]]
        arguments.extend(filtered_args)

        arguments.extend(ManagedAppCreateOptionalParameters.PARAMETERS)
        self.commands.add_arguments(arguments)


    def execute(self):
        print(self.__class__.__name__)
        print(json.dumps(self.commands.parse_result, indent=4))

        cmd_line = self.get_command_line(self.commands.parse_result)
        print(json.dumps(cmd_line, indent=4))