from cliutils.module_base import ModuleBase

class InstanceLoader(ModuleBase):
    def __init__(self, insert_location:int, directory:str, module:str):
        super().__init__(insert_location, directory, module)

    def get_instances(self, interface_type: str):
        loaded_instances = []
        for attr_name in dir(self.module_actual):
            attr = getattr(self.module_actual, attr_name)
            
            try:
                attr_actual = attr()
                for bc in attr_actual.__class__.__bases__:
                    if bc.__name__ == interface_type:
                        loaded_instances.append(attr_actual)
            except TypeError as ex:
                pass
            except Exception as ex:
                print(ex)

        return loaded_instances

    @staticmethod
    def get_all_instances(desired_type:str, directory:  str) -> list:
        instance_modules = ModuleBase.get_python_modules(directory)

        found_instances = []
        for mod in instance_modules:
            instance_loader = InstanceLoader(2, directory, mod) 
            found = instance_loader.get_instances(desired_type)
            if len(found):
                found_instances.extend(found)
        return found_instances
