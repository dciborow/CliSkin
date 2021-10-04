from interfaces.command import Argument

"""
If an argument is required DO NOT USE A LIST use only one option

If not required, you can use as many as you like in a list
"""

class GenericCommandOptionalParameters:
    # For some reason we can't combine some of these....gives an arg
    # parse error so just keep them separated
    PARAMETERS = [
        Argument(["--name", "-n"], "name", False, str, "Application name"),
        Argument(["--subscription", "-s"], "subscription", False, str, "Azure Subscription"),
        Argument(["--resource-group", "-g"], "resource_group", False, str, "Resource Group"),
    ]

class ManagedAppCreateOptionalParameters:
    PARAMETERS = [
        Argument(["--location" "-l"], None, False, str, "Azure Region"),
        Argument("--managedapp-definition-id", None, False, str, "app definition id"),
        Argument("--parameters", None, False, str, "parameters"),
        Argument("--plan-name", None, False, str, "plan name"),
        Argument("--plan-product", None, False, str, "plan product"),
        Argument("--plan-publisher", None, False, str, "plan publisher"),
        Argument("--plan-version", None, False, str, "plan version"),
        Argument("--tags", None, False, str, "tags to apply")
    ]

