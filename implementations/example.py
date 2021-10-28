import json
from implementations import CmdUtils
from interfaces.command import ICommand, Argument, CommandArgs

class ExampleCommand(ICommand):
    def __init__(self):
        self.commands = CommandArgs(
            "Example Command",
            ["azdc", "ai", "list"]
        )
        # Actual command to pass through
        self.actual_command = ["az", "managedapp", "list"]

        arguments = [
            # Actual params supply a type
            Argument(["--ids", "-i"], "resource_ids", False, str, "Resource ID's"),
            # Flags don't provide a type
            Argument("--no-wait", "wait", False, None, "Do not wait")
        ]

        self.commands.add_arguments(arguments)

    def execute(self):
        print("Example Command Execute....")
        print(self.commands.parse_result)

        cmd_line = self.get_command_line(self.commands.parse_result)
        print("CMD LIINE:", cmd_line)
        """
        output = CmdUtils.get_command_output(cmd_line)

        if CmdUtils.LAST_STD_ERR:
            print(CmdUtils.LAST_STD_ERR)
        else:
            print(json.dumps(output, indent=4))
        """
