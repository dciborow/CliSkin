import typing
from abc import ABC, abstractmethod
from interfaces.commandargs import CommandArgs, Argument

class ICommand(ABC):
    def __init__(self):
        # Description of command
        self.description:str = None
        # Command line arguments
        self.commands:CommandArgs = None
        # Underlying actual command line to execute - with args
        self.actual_command:typing.List[str] = None

    def help(self):
        print(self.commands.help())

    def overview(self):
        print("  ", " ".join(self.commands.prelude))

    def validate_command(self, user_command: str) -> CommandArgs.ParseResult:
        commands = user_command.split()
        if '"' in user_command:
            latest_commands  = []
            in_quote = False
            temp_buffer = []
            for cmd in commands:
                if in_quote:
                    temp_buffer.append(cmd)

                    if '"' in cmd:
                        latest_commands.append(" ".join(temp_buffer))
                        temp_buffer = []
                        in_quote = False 
                elif '"' in cmd:
                    in_quote = True
                    temp_buffer.append(cmd)
                else:
                    latest_commands.append(cmd)
            commands = latest_commands

        return self.commands.parse(commands)

    def get_command_line(self, incoming_parameters: dict) -> typing.List[str]:
        command_line = []
        command_line.extend(self.actual_command)

        arguments = []
        for parameter in incoming_parameters:
            # Only check for something with an actual value
            if incoming_parameters[parameter] is not None:
                arg = self.commands.find_argument(parameter)

                if arg.klass is None and not incoming_parameters[parameter]:
                    # it's a flag and it's false, i.e. don't use. it
                    continue 
                if arg:
                    arguments.append( (arg, incoming_parameters[parameter]) )

        flags = []
        for arg in arguments:
            if arg[0].klass:
                command_line.append(arg[0].get_command())
                command_line.append(arg[1])
            else:
                flags.append(arg[0].get_command())

        if len(flags) > 0:
            command_line.extend(flags)

        return command_line

    # Do the actual work
    @abstractmethod
    def execute(self) -> None:
        pass

