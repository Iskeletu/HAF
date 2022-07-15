"""Command Line Interface Module."""

#External Modules:
from selenium import webdriver

#Internal Modules:
from Constants import CLIConstants
from CLI.Commands import *


def CommandLineInterface(driver:webdriver.Chrome) -> bool:
    """
    Command Line Interface (CLI) main function.\n
    Handles and formats user input for command execution.\n
    Returns a bool indicating whether the program should end 
    or not.

    Arguments:
        - driver: A loaded Chrome webdriver object, mainly to 
    be passed as method to commands.
    """

    #Gets user input.
    print('HAF> ', end = '')
    user_input = input()

    #Fomarts user input as a string list.
    command_list = user_input.split(' ')
    command_list = [i for i in command_list if i]

    #Calls for command execution.
    if command_list: #Does nothing if command is blank.
        match command_list[0]:
            case 'call':
                CallCommand(driver).execute(command_list)

            case 'ticket':
                TicketCommand(driver).execute(command_list)

            case 'details':
                DetailsCommand().execute(command_list)

            case 'help':
                HelpCommand().execute(command_list)

            case 'exit':
                return ExitCommand(driver).execute(command_list)

            case _:
                print(CLIConstants.INVALID_COMMAND.format(Command = command_list[0]))

    return False


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')