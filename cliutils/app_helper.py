from cliutils.load_interfaces import InterfaceLoader
from cliutils.load_instances import InstanceLoader


class CliAppHelpers:
    @staticmethod
    def load_instances(interface_name:str, interface_path:str, implementation_path:str):
        # Ensure that the interface defs are available when loading instances
        found_interfaces = InterfaceLoader.get_interfaces(interface_path)

        # Load up instalces
        icommand_instances = []
        if interface_name in found_interfaces: 
            result = InstanceLoader.get_all_instances(interface_name, implementation_path)
            if len(result):
                icommand_instances.extend(result)

        return icommand_instances
