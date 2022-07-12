"""
Command Line Interface Module

TODO = Add command descriptions
"""

#External Modules:
from selenium import webdriver

#Internal Modules:
from CLI.Commands import *
from Constants import CLI


def CommandLineInterface(driver:webdriver.Chrome) -> bool:
    """
    Command Line Interface (CLI) main function.

    Handles and formats user input for command execution.

    Arguments:
    - driver: A loaded Chrome webdriver object, mainly to 
    be passed as method to commands.
    """

    exit_flag = False

    print('HAF> ', end = '')
    user_input = input()

    #Fomarts user input as a string list.
    command_list = user_input.split(' ')
    command_list = [i for i in command_list if i]

    if command_list:
        match command_list[0]:
            case 'call':
                CallCommand(driver).execute(command_list)

            case 'help':
                HelpCommand().execute(command_list)

            case 'exit':
                exit_flag = ExitCommand(driver).execute(command_list)

            case _:
                print(CLI.INVALID_COMMAND.format(Command = command_list[0]))

    return exit_flag


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')