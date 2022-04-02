#from azure.identity import AzureCliCredential
from implementations import CmdUtils

class UserContext:
    def __init__(self):
        self.subscription_id = None
        self.subscription = None
        self.user = None
        self.token = None

class Defaults:

    CONTEXT:UserContext = None

    @staticmethod
    def get_user_context() -> UserContext:
        if Defaults.CONTEXT:
            return Defaults.CONTEXT

        Defaults.CONTEXT = UserContext()

        if current := Defaults._get_current_account():
            Defaults.CONTEXT.subscription = current["name"]
            Defaults.CONTEXT.subscription_id = current["id"]
            Defaults.CONTEXT.user = current["user"]["name"]
            Defaults.CONTEXT.token = Defaults._get_management_access_key_for_user()

        return Defaults.CONTEXT

    @staticmethod
    def _get_current_account():
        command = "az account show"
        result = CmdUtils.get_command_output(command.split(" "))

        if isinstance(result, dict):
            return result
        
        return None

    @staticmethod 
    def _get_management_access_key_for_user():
        """
        Create a Auth Client for interacting with azure managment API's
        This is determined by the scope of managment.core.windows.net, other scopes
        are used for other purposes. 
        """
        #working_credential = AzureCliCredential()
        #token_obj = working_credential.get_token("https://management.core.windows.net/")
        #return token_obj.token