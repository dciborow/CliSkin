from abc import ABC
from cliutils.module_base import ModuleBase

class InterfaceLoader(ModuleBase):
    def __init__(self, insert_location:int, directory:str, module:str):
        super().__init__(insert_location, directory, module)
        self.interfaces = {}
        self.abc_derived = []

    def load(self):
        return_objects = []
        for attr in dir(self.module_actual):
            obj_def = getattr(self.module_actual, attr)
            obj_def_type = type(obj_def)
            # Has to be of type ABC
            if type(ABC) == obj_def_type:
                # Interface has 0 sub classes
                if len(obj_def.__subclasses__()) == 0:
                    return_objects.append(obj_def_type)
                    self.interfaces[obj_def.__name__] = obj_def_type
                else:
                    for sc in obj_def.__subclasses__():
                        self.abc_derived.append(sc.__name__)
        return return_objects

    @staticmethod
    def get_interfaces(directory:  str) -> list:
        interface_modules = ModuleBase.get_python_modules(directory)

        found_interfaces = []
        for mod in interface_modules:
            interface_loader = InterfaceLoader(1, directory, mod) 
            interface_loader.load()
            found_interfaces.extend(interface_loader.abc_derived)
        return found_interfaces        