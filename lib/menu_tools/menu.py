# lib/menu_tools/menu.py
from menu_tools.command import Command

class Menu:
    
    def __init__(self, command_list=[]):
        self.command_list = []
        
    def add_command(self, prompt, callback):
        self.command_list.append(
            Command(len(self.command_list), prompt, callback)
        )
        
    def display_commands(self):
        for command in self.command_list:
            print(repr(command))
        print()
        
    def execute_command(self, index):
        if index >= 0 and index < len(commands := self.command_list):
            commands[index].callback()
        else:
            print("Invalid choice")
            
    def get_command_by_callback(self, callback):
        for command in self.command_list:
            if (callback == command.callback):
                return command
        return None