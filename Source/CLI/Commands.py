"""TODO"""

#External Modules:
from selenium import webdriver

#Internal Modules:
from Constants import CLI
from Ticket.TicketHandler import TicketProcessor


class HelpCommand():
    """
    'help' command class.\n
    *Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
    - description: Command description.
    - subcommands: A list of available subcommands.
    """
    
    def execute(self, command_list:list) -> None:
        match self.__validate(command_list):
            case 1:
                TODO = True

            case 2:
                print(CLI.INVALID_SUBCOMMAND.format(Subcommand = command_list[1]))

            case 3:
                print(CLI.TOO_MANY_ARGUMENTS.format(Command = command_list[0]))

            case 4:
                TODO = True


    def __validate(self, command_list:list) -> int:
        """
        Private method: Validates the command and it's arguments (if existant).\n
        Return:
        - 1 if the command has a valid argument.
        - 2 if the subcommand is invalid.
        - 3 if too many arguments were given to the command.
        - 4 if the command has no argument.
        
        Arguments:
        - command_list: Formatted command list to be validated.
        """
        command_size = len(command_list)

        if command_size > 1:
            if command_size < 3:
                if command_list[1] in CLI.AVAILABLE_COMMANDS:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4


class ExitCommand():
    """
    'exit' command class.\n
    *Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
    - description: Command description.
    - subcommands: A list of available subcommands.
    
    Private Attributes:
    - __driver: A loaded Chrome webdriver object.
    """

    description = "Closes webdriver and finishes the program."
    subcomands = ["This command does not accept any subcommand."]

    def __init__(self, driver:webdriver.Chrome) -> None:
        """
        Initializes an instance of ExitCommand class.

        Arguments:
        - __driver: A loaded Chrome webdriver object.
        """

        self.__driver = driver


    def execute(self, command_list:list) -> bool:
        """
        Executes the 'exit' command.\n
        Returns a bool, true if sucessful, false otherwise.

        Dependencies:
        - :mod:`__validation()`: For command validation.
        
        Arguments:
        - command_list: A formatted list conatining the full command run by the user, 
        mainly to be passed to :mod:`__validation()` for command validation.
        """

        if self.__validate(command_list):
            self.__driver.quit()
            return True
        else:
            print(CLI.INVALID_SUBCOMMAND.format(Subcommand = command_list[1]))
            return False


    def __validate(self, command_list:list) -> bool:
        """
        Private method: Validates the command and it's arguments (if existant).\n
        Returns true if the command is valid, false otherwise.
        
        Arguments:
        - command_list: Formatted command list to be validated.
        """

        if len(command_list) == 1:
            return True
        else:
            return False


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')