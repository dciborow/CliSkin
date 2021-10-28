from cliutils import Configuration, CliAppHelpers

config_settings = Configuration("./configuration.json")

"""
The application only needs to know a few things
- The folder defining the interfaces you want
- The folder with interface implementations (seperate)
- Understand the structure of the interface, thanks to duck typing
  in python we don't actually NEED the interface. 
"""
interface_instances = CliAppHelpers.load_instances(
    config_settings.desired_types[0], 
    config_settings.interface_path, 
    config_settings.implementation_path
    )

while True:
    user_input = input("> ")

    if user_input in ["q", "Q", "quit"]:
        break
    
    command_found = False
    for instance in interface_instances:
        parse_val = instance.validate_command(user_input)

        try:
            if parse_val == 1: # OK
                command_found = True
                instance.execute()
                break
            elif parse_val == 2: # Failed
                command_found = True
                instance.help()
                break
            """
            Else - Invalid -  it's not a command tied to this based on prelude
            """
        except Exception as ex:
            print("Exception:", str(ex) )

    if not command_found:
        if user_input not in ["-h", "--help", "help", "-h", "?"]:
            print("Command not found: ", user_input)
        print("Available Commands")
        for instance in interface_instances:
            instance.overview()
        continue
