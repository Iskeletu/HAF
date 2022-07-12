"""TODO"""

#External Modules:
from selenium import webdriver

#Internal Modules:
from Constants import CLI
from Ticket.TicketHandler import TicketProcessor


class CallCommand():
    Description = 'Registers call data as ticket.'
    Subcommands = {
        'register': 'register a ticket based on its dictonary type'
    }
    Usage = ['call [subcommand]']


    def __init__(self, driver:webdriver.Chrome) -> None:
        self.__driver = driver

    
    def execute(self, command_list:list[str]) -> None:
        match self.__validate(command_list):
            case 1:
                match command_list[1]:
                    case 'register':
                        TicketProcessor(self.__driver)

            case 2:
                print(CLI.INVALID_SUBCOMMAND.format(Command = command_list[0], Subcommand = command_list[1]))

            case 3:
                print(CLI.TOO_MANY_ARGUMENTS.format(Command = command_list[0]))

            case 4:
                print(CLI.TOO_FEW_ARGUMENTS.format(Command = command_list[0]))


    def __validate(self, command_list:list[str]) -> int:
        """
        Private method: Validates the command and it's arguments (if existant).\n
        Return:
        - 1 if the command has a valid argument.
        - 2 if the argument is invalid.
        - 3 if too many arguments were given to the command.
        - 4 if the command has no argument.
        
        Arguments:
        - command_list: Formatted command list to be validated.
        """

        command_size = len(command_list)

        if command_size > 1:
            if command_size < 3:
                if command_list[1] in self.Subcommands:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4


class HelpCommand():
    """
    'help' command class.\n
    *Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
    - Description: Command description.
    - Subcommands: A dict of available subcommands and their description, blank if no subcommand is available.
    - Usage: list off command usages.
    """

    Description = 'Provides information about available commands.'
    Subcommands = {
        'call': 'Shows "call" command information.',
        'ticket': 'Shows "ticket" command information.',
        'details': 'Shows "details" command information.',
        'help': 'Shows this screen.',
        'exit': 'Shows "exit" command information.'
    }
    Usage = [
        'help',
        'help [command_name]'
    ]
    
    def execute(self, command_list:list[str]) -> None:
        """
        Executes the 'help' command.\n

        Dependencies:
        - :mod:`__validation()`: For command validation, see it's documentation for return values.
        
        Arguments:
        - command_list: A formatted list conatining the full command run by the user, 
        mainly to be passed to :mod:`__validation()` for command validation.
        """

        match self.__validate(command_list):
            case 1:
                match command_list[1]:
                    case 'call':
                        Command_Description = CallCommand.Description
                        Available_Subcommands = CallCommand.Subcommands
                        Command_Usage = CallCommand.Usage

                    case 'ticket':
                        Command_Description = 'TODO'
                        Available_Subcommands = {}
                        Command_Usage = 'TODO'

                    case 'details':
                        Command_Description = 'TODO'
                        Available_Subcommands = {}
                        Command_Usage = 'TODO'

                    case 'help':
                        Command_Description = self.Description
                        Available_Subcommands = self.Subcommands
                        Command_Usage = self.Usage

                    case 'exit':
                        Command_Description = ExitCommand.Description
                        Available_Subcommands = ExitCommand.Subcommands
                        Command_Usage = ExitCommand.Usage
                        
                Formatted_Usage = self.__Usage_Formatter(Command_Usage)
                Formatted_Subcommands = self.__Subcommands_Formatter(Available_Subcommands)

                print(CLI.HELP_COMMAND_VALIDARG.format(
                    Command_Name = command_list[1],
                    Command_Description = Command_Description,
                    Available_Subcommands = Formatted_Subcommands,
                    Command_Usage = Formatted_Usage
                ))

            case 2:
                print(CLI.INVALID_SUBCOMMAND.format(Subcommand = command_list[1]).removesuffix('\n'))
                self.execute(['help'])

            case 3:
                print(CLI.TOO_MANY_ARGUMENTS.format(Command = command_list[0]))

            case 4:
                print(CLI.HELP_COMMAND_NOARGS.format(
                    call_Description = CallCommand.Description,
                    ticket_Description = 'TODO',
                    details_Description = 'TODO',
                    help_Description = self.Description,
                    exit_Description = ExitCommand.Description
                ))


    def __validate(self, command_list:list[str]) -> int:
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


    def __Subcommands_Formatter(self, Subcommads_Dict:dict) -> str:
        if Subcommads_Dict:
            Formatted_Subcommands = ''

            for i in Subcommads_Dict:
                Formatted_Subcommands = Formatted_Subcommands + '\t- ' + str(i) + ': ' + Subcommads_Dict[i] + '\n'

            return Formatted_Subcommands.removesuffix('\n')
        else:
            return '\tThis command does not accept any subcommands.'

    
    def __Usage_Formatter(self, Usage_List:list) -> str:
        Formatted_Usage = ''

        for i in Usage_List:
            Formatted_Usage = Formatted_Usage + '\t- HAF> ' + str(i) + '\n'

        return Formatted_Usage.removesuffix('\n')


class ExitCommand():
    """
    'exit' command class.\n
    *Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
    - Description: Command description.
    - Subcommands: A dict of available subcommands and their description, blank if no subcommand is available.
    - Usage: list off command usages.
    
    Private Attributes:
    - __driver: A loaded Chrome webdriver object.
    """

    Description = 'Closes webdriver and finishes the program.'
    Subcommands = {}
    Usage = ['exit']

    def __init__(self, driver:webdriver.Chrome) -> None:
        """
        Initializes an instance of ExitCommand class.

        Arguments:
        - __driver: A loaded Chrome webdriver object.
        """

        self.__driver = driver


    def execute(self, command_list:list[str]) -> bool:
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


    def __validate(self, command_list:list[str]) -> bool:
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