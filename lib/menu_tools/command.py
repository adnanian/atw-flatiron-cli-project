# lib/menu_tools/command.py
import types

class Command:
    
    def __init__(self, index, prompt, callback):
        """ Create a new instance of command.

        Args:
            index (int): the number associated with the command.
            prompt (str): the message displayed to the user.
            callback (function): the function that is to be invoked.
        """
        self.index = index
        self.prompt = prompt
        self.callback = callback
    
    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index):
        if type(index) is int and index >= 0:
            self._index = index
        else:
            raise ValueError("Command index must be a non-negative integer")
    
    
    @property
    def prompt(self):
        return self._prompt
    
    @prompt.setter
    def prompt(self, prompt):
        if isinstance(prompt, str) and len(prompt):
            self._prompt = prompt
        else:
            raise ValueError("Prompt must be a non-empty string")
    
    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self, callback):
        if isinstance(callback, types.FunctionType):
            self._callback = callback
        else:
            raise ValueError("Callback must be a declared function")
        
    def __repr__(self) -> str:
        return f"{self.index}. {self.prompt}"
    
    def to_menu_option(self):
        """ Returns a string representation of a command using its index and prompt attributes.

        Returns:
            str: a string in the format: [index]. [prompt]
        """
        return f"{self.index}. {self.prompt}"