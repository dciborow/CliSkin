from argparse import ArgumentParser
from contextlib import redirect_stderr
from enum import Enum
import io
import typing

class Argument:
    def __init__(self, name:typing.Any = None, destination:str = None, required:bool = True, typeklass = str, help:str = None):
        self.name = name
        self.destination = destination
        self.required = required
        self.klass = typeklass
        self.help = help

    def get_command(self) -> str:
        return self.name if isinstance(self.name, str) else self.name[0]

class CommandArgs:
    class ParseResult(Enum):
        OK = 1 # Parsed OK
        FAILED = 2 # Prelude correct, args incorrect
        INVALID = 3 # Prelude incorrect, wrong command

    def __init__(self, description:str, prelude:list):
        self.arguments = []
        self.prelude = prelude
        self.parser = ArgumentParser(description=description)
        self.parse_result = {}

    def add_argument(self, arg: Argument):
        self.arguments.append(arg)

        if isinstance(arg.name, list):
            for name in arg.name:
                self.__add_individual_argument(name, arg)
        else:
            self.__add_individual_argument(arg.name, arg)

    def __add_list_argument(self, arg:Argument):
        if arg.klass is None:
            # It's a flag
            if arg.destination:
                self.parser.add_argument(
                    *(arg.name),
                    dest=arg.destination,
                    action='store_true',
                    default=False,
                    help=arg.help
                )
            else:
                self.parser.add_argument(
                    *(arg.name),
                    action='store_true',
                    default=False,
                    help=arg.help
                )

        else:
            if arg.destination:
                self.parser.add_argument(
                    arg.name,
                    dest=arg.destination,
                    required=arg.required,
                    type = arg.klass,
                    help=arg.help
                )
            else:
                self.parser.add_argument(
                    arg.name,
                    dest=arg.destination,
                    required=arg.required,
                    type = arg.klass,
                    help=arg.help
                )

    def __add_individual_argument(self, name:str, arg:Argument):
        if arg.klass is None:
            # It's a flag
            if arg.destination:
                self.parser.add_argument(
                    name,
                    dest=arg.destination,
                    action='store_true',
                    default=False,
                    help=arg.help
                )
            else:
                self.parser.add_argument(
                    name,
                    action='store_true',
                    default=False,
                    help=arg.help
                )

        else:
            if arg.destination:
                self.parser.add_argument(
                    name,
                    dest=arg.destination,
                    required=arg.required,
                    type = arg.klass,
                    help=arg.help
                )
            else:
                self.parser.add_argument(
                    name,
                    required=arg.required,
                    type = arg.klass,
                    help=arg.help
                )

    def add_arguments(self, args: typing.List[Argument]):
        for arg in args:
            self.add_argument(arg)

    def find_argument(self, parameter_name:str) -> Argument:
        found_arg = [x for x in self.arguments if x.destination == parameter_name]

        if not len(found_arg):
            # Have to check them all except ones with destination
            found_arg = None
            name_to_find = parameter_name
            name_to_find = name_to_find.replace('_', '-')

            args_to_search = [x for x in self.arguments if x.destination is None]
            for arg in args_to_search:
                if found_arg:
                    break

                if isinstance(arg.name, list):
                    for name in arg.name:
                        if parameter_name in name:
                            found_arg  = arg
                            break
                elif parameter_name in arg.name:
                    found_arg  = arg

        else:
            found_arg = found_arg[0]

        return found_arg

    def parse(self, command:list) -> Enum:
        return_value = CommandArgs.ParseResult.OK

        # Prelude has to match up...then we remove it from the list
        usable_command = command[:]

        if len(usable_command) < len(self.prelude):
            return_value = CommandArgs.ParseResult.INVALID
        else:
            # Verify prelude is actually this command
            for idx in range(len(self.prelude)):
                if self.prelude[idx].lower() != usable_command[idx]: 
                    return_value = CommandArgs.ParseResult.INVALID
                    break

            if return_value == CommandArgs.ParseResult.OK:
                usable_command = usable_command[len(self.prelude):]

        if return_value == CommandArgs.ParseResult.OK: # and len(usable_command) > 0:
            redirect_io = io.StringIO()
            with redirect_stderr(redirect_io):  
                try:
                    parsed_values = self.parser.parse_args(usable_command)
                        
                    self.parse_result = {}
                    for val in dir(parsed_values):
                        if val.startswith('_') == False:
                            self.parse_result[val] = getattr(parsed_values, val)
                except:
                    # Attempt to see if ANY of the commands are correct                        
                    return_value = CommandArgs.ParseResult.FAILED
        
        return return_value.value

    def help(self) -> str:
        return_val = "Invalid Usage - Command Help:\n"
        return_val += "  {}\n".format(" ".join(self.prelude))
        for arg in self.arguments:
            return_val += "   [{}] {} - {}\n".format(
                ("R" if arg.required else "N"),
                arg.name, 
                arg.help)
        return return_val