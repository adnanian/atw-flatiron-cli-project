# lib/menu_tools/menu.py
from menu_tools.command import Command

class Menu:
    all = {}
    
    def __init__(self, key_name, command_list=[]):
        """ Create a new instance of Menu

        Args:
            key_name (str): name of the key to store this menu object to the dictionary of menus.
            command_list (list, optional): A list of Command objects. Defaults to [].
        """
        self.command_list = []
        self.key_name = key_name
        type(self).all[key_name] = self
        
    def add_command(self, prompt, callback):
        """ Adds a new Command to the menu's command list.

        Args:
            prompt (str): the prompt.
            callback (function): the callback function.
        """
        self.command_list.append(
            Command(len(self.command_list), prompt, callback)
        )
        
    def display_commands(self):
        """ Prints the list of commands associated with the menu to the terminal.
        """
        for command in self.command_list:
            print(command.to_menu_option())
        print()
        
    def execute_command(self, index):
        """ Invoke the callback function of a command referenced at a given index.

        Args:
            index (int): the index that points to the command in the command list.
        """
        if index >= 0 and index < len(commands := self.command_list):
            print("\n", commands[index].prompt, "\n")
            commands[index].callback()
        else:
            print("Invalid choice")
            
    def get_command_by_callback(self, callback):
        """ Searchs in the command list for a command with a given callback function and returns that command if found.

        Args:
            callback (function): the callback function.

        Returns:
            _type_: returns the command object if found; None, otherwise.
        """
        for command in self.command_list:
            if (callback == command.callback):
                return command
        return None