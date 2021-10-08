# CliSkin

Skin on top of command line tools to mimic a cli


## Description
The cliapp.py uses the configuration.json file to find and load instances of interfaces for it to consume. 

|Setting|Value|
|----|----|
|desired_types|Interfaces that you want the application to load|
|interface_path|Full disk path to the folder containing the interface definitions that are identified in desired_types. This folder can be anywhere on your disk.|
|implementation_path|Full disk path to the folder containing the implementations of the interfaces that are defined in desired_types and found in interface_path. This folder can be anywhere on your disk.|


From this example, create new implementations that implement the ICommand interface such as:

```python
class AzAiAppCreate(ICommand):
    def __init__(self):
        self.commands = CommandArgs(
            # Name the command for help
            "First Command Arguments",
            # How you want your cli to represent the call
            ["az", "ai","app", "create"] 
        )

        # The underlying actual call to make
        self.actual_command = ["az", "managedapp", "create"]
     
        # Arguments for your call
        arguments = [
            # Use single string or list of strings for argument names
            Argument(["--name", "-n"], "name", True, str, "Application name"),
            Argument("--kind", "kind", True, str, "Kind"),
        ]

        # Add any other additional arguments your call can take
        filtered_args = [x for x in GenericCommandOptionalParameters.PARAMETERS if x.destination not in ["name"]]
        arguments.extend(filtered_args)

        # Add your own arguments to the base ICommand
        self.commands.add_arguments(arguments)


    def execute(self):
        """
        When your call sucsessfully gets entered with the required
        arguments this call will be executed. 

        The command line arguments are available and if written 
        correctly the full actual command line can be constructed
        for you.
        """
        cmd_line = self.get_command_line(self.commands.parse_result)
        output = CmdUtils.get_command_output(cmd_line)

        if CmdUtils.LAST_STD_ERR:
            # If there was an error, print it out...
            print(CmdUtils.LAST_STD_ERR)
        else:
            # Print out whatever the underlying call returned
            print(json.dumps(output, indent=4))
```