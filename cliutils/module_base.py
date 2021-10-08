import os
import sys
import importlib

class ModuleBase:
    PATH_INSERTS = []

    def __init__(self, insert_location:int, directory:str, module:str):
        self.path = directory
        self.interface_module = module
        self.module_actual = None

        if directory not in ModuleBase.PATH_INSERTS:
            ModuleBase.PATH_INSERTS.append(directory)
            sys.path.insert(insert_location, directory)
        
        try:
            self.module_actual = importlib.import_module(self.interface_module)
        except Exception as ex:
            print("FAILED X",insert_location, "Y", directory, "Z", self.interface_module)
            print(str(ex))


    @staticmethod
    def get_python_modules(path:str):
        PYTHON_FILTER = ".py"
        return_modules = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if root == path:
                    name = name.lower()
                    if name[-3:] == PYTHON_FILTER and name != "__init__.py":
                        return_modules.append(name[:-3])
        return return_modules