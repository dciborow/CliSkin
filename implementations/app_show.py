from interfaces.command import ICommand, Argument, CommandArgs
from implementations.optionalparameters import GenericCommandOptionalParameters
from implementations import CmdUtils
import json

class AzAiAppShow(ICommand):
    def __init__(self):
        self.commands = CommandArgs(
            "First Command Arguments",
            ["az", "ai","app", "show"]
        )
        self.actual_command = ["az", "managedapp", "show"]

        arguments = [
            Argument(["--ids", "-i"], "resource_ids", False, str, "Resource ID's")
        ]
        arguments.extend(GenericCommandOptionalParameters.PARAMETERS)

        self.commands.add_arguments( arguments )

    def execute(self):
        cmd_line = self.get_command_line(self.commands.parse_result)
        print(json.dumps(cmd_line, indent=4))
        #output = CmdUtils.get_command_output(cmd_line)
        #print(json.dumps(output, indent=4))

        # Just to see.....
        #print(CmdUtils.LAST_STD_ERR)
