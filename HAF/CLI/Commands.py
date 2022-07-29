"""Defines command behavior."""

#External Modules:
from selenium import webdriver

#Internal Modules:
from HAF.GUI.GUIHandler import GUI
from HAF.FileHandler.Logger import LogClass
from HAF.FileHandler.Config import ConfigClass
from HAF.Constants import CLIConstants, LogConstants
from HAF.Ticket.TicketHandler import TicketProcessor


class GuiCommand():
    """
    'gui' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
        - Usage: list off command usages.

    Private Attributes:
        - __driver: A loaded Chrome webdriver object.
    """

    Description = 'Opens GUI (Graphical User Interface).'
    Subcommands = {}
    Usage = ['gui']


    def __init__(self, driver:webdriver.Chrome) -> None:
        """
        Initializes an instance of GuiCommand class.

        Arguments:
            - __driver: A loaded Chrome webdriver object.
        """
        
        self.__config = ConfigClass()
        self.__driver = driver


    def execute(self, command_list:list[str], print_message_flag:bool = True) -> bool:
        """
        Executes the 'gui' command.\n

        Return:
            - True if exit command should be run.
            - False otherwise.

        Dependencies:
            - :mod:`__validation()`: For command validation.
        
        Arguments:
            - command_list: A formatted list containing the full command run by the user.
        """

        if self.__validate(command_list): #Command is valid, executes the command.
            if print_message_flag:
                print('Running GUI!')

            exit_value = int(GUI(self.__config, self.__driver).Start())
            
            match exit_value:
                case 0: #User close the window.
                    print('\n', end = '')
                    return False

                case 1: #User called for exit.
                    print('\nHAF> exit')
                    return ExitCommand(self.__driver).execute(['exit'])

                case 2: #GUI needs reset.
                    print('Restarting GUI!')
                    return self.execute(command_list, False)
        else: #Command is invalid (has arguments), prints the standard invalid subcommand message.
            print(CLIConstants.INVALID_SUBCOMMAND.format(
                Command = command_list[0],
                Subcommand = command_list[1]
            ))
            return False


    def __validate(self, command_list:list[str]) -> bool:
        """
        Private method: Validates the command and its arguments (if existant).
        
        Return:
            - True if the command is valid.
            - False otherwise.
        
        Arguments:
            - command_list: Formatted command list to be validated.
        """

        if len(command_list) == 1:
            return True
        else:
            return False


class CallCommand():
    """
    'call' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
        - Usage: list off command usages.

    Private Attributes:
        - __driver: A loaded Chrome webdriver object.
    """

    Description = 'Registers call data as ticket.'
    Subcommands = {
        'register': 'register a ticket based on its dictonary type.'
    }
    Usage = ['call [subcommand]']


    def __init__(self, driver:webdriver.Chrome) -> None:
        """
        Initializes an instance of CallCommand class.

        Arguments:
            - __driver: A loaded Chrome webdriver object.
        """

        self.__driver = driver

    
    def execute(self, command_list:list[str]) -> None:
        """
        Executes the 'call' command.\n

        Dependencies:
            - :mod:`__validation()`: For command validation, see its documentation for return values.
        
        Arguments:
            - command_list: A formatted list conatining the full command run by the user.
        """

        match self.__validate(command_list):
            case 1: #Command has a valid subcommand, executes, the subcommand.
                match command_list[1]:
                    case 'register':
                        TicketProcessor(self.__driver)

            case 2: #Invalid was sent by the user, prints standard invalid subcommand message.
                print(CLIConstants.INVALID_SUBCOMMAND.format(Command = command_list[0], Subcommand = command_list[1]))

            case 3: #Too many arguments were sent by the user, prints standard too many arguments message.
                print(CLIConstants.TOO_MANY_ARGUMENTS.format(Command = command_list[0]))

            case 4: #No subcommand was sent by the user, prints standard too few arguments message.
                print(CLIConstants.TOO_FEW_ARGUMENTS.format(Command = command_list[0]))


    def __validate(self, command_list:list[str]) -> int:
        """
        Private method: Validates the command and its arguments (if existant).

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
                if command_list[1] in self.Subcommands:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4


class TicketCommand(): #TODO
    """
    'ticket' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
        - Usage: list off command usages.

    Private Attributes:
        - __driver: A loaded Chrome webdriver object.
    """

    Description = 'This command is on development.'
    Subcommands = {}
    Usage = ['ticket [subcommand] [args]']

    def __init__(self, driver:webdriver.Chrome) -> None:
        """
        Initializes an instance of TicketCommand class.

        Arguments:
            - __driver: A loaded Chrome webdriver object.
        """

        self.__driver = driver


    def execute(self, command_list:list[str]) -> None: #TODO
        TODO = True


class DetailsCommand():
    """
    'details' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
        - Usage: list off command usages.
    """

    Description = 'Gets details form the last log registered to file.'
    Subcommands = {}
    Usage = ['details']


    def __init__(self) -> None:
        """Initializes an instance of DetailsCommand class."""

        self.__config = ConfigClass()


    def execute(self, command_list:list[str]) -> None:
        """
        Executes the 'exit' command.\n

        Dependencies:
            - :mod:`__validation()`: For command validation.
        
        Arguments:
            - command_list: A formatted list containing the full command run by the user.
        """

        if self.__validate(command_list): #Command is valid, executes the command
            #Checks if there is a log registered to get details from.
            if self.__config.GetCounter > 0:
                print('Ticket Details:')
                print(LogClass(LogConstants.TICKET_LOADPERSISTENT).ConvertToString())
            else:
                print("- ERROR 03: 'No Previous logs registered', there is no log to import data from.\n")
        else: #Command is invalid (has arguments), prints the standard invalid subcommand message.
            print(CLIConstants.INVALID_SUBCOMMAND.format(
                Command = command_list[0],
                Subcommand = command_list[1]
            ))


    def __validate(self, command_list:list[str]) -> bool:
        """
        Private method: Validates the command and its arguments (if existant).
        
        Return:
            - True if the command is valid.
            - False otherwise.
        
        Arguments:
            - command_list: Formatted command list to be validated.
        """

        if len(command_list) == 1:
            return True
        else:
            return False


class HelpCommand():
    """
    'exit' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
        - Usage: list off command usages.
    """

    Description = 'Provides information about available commands.'
    Subcommands = {
        'gui': 'Shows "gui" command information.',
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
            - :mod:`__validation()`: For command validation, see its documentation for return values.
            - :mod:`__Subcommands_Formatter()`: For subcommand dictionary to string conversion.
            - :mod:`__Usage_Formatter()`: For usage list to string conversion.
        
        Arguments:
            - command_list: A formatted list conatining the full command run by the user.
        """

        match self.__validate(command_list):
            case 1: #Prints help command for subcommand sent by the user.
                #Gets class information based on subcommand sent by the user.
                match command_list[1]:
                    case 'gui':
                        Command_Description = GuiCommand.Description
                        Available_Subcommands = GuiCommand.Subcommands
                        Command_Usage = GuiCommand.Usage

                    case 'call':
                        Command_Description = CallCommand.Description
                        Available_Subcommands = CallCommand.Subcommands
                        Command_Usage = CallCommand.Usage

                    case 'ticket':
                        Command_Description = TicketCommand.Description
                        Available_Subcommands = TicketCommand.Subcommands
                        Command_Usage = TicketCommand.Usage

                    case 'details':
                        Command_Description = DetailsCommand.Description
                        Available_Subcommands = DetailsCommand.Subcommands
                        Command_Usage = DetailsCommand.Usage

                    case 'help':
                        Command_Description = self.Description
                        Available_Subcommands = self.Subcommands
                        Command_Usage = self.Usage

                    case 'exit':
                        Command_Description = ExitCommand.Description
                        Available_Subcommands = ExitCommand.Subcommands
                        Command_Usage = ExitCommand.Usage
                
                Formatted_Subcommands = self.__Subcommands_Formatter(Available_Subcommands)
                Formatted_Usage = self.__Usage_Formatter(Command_Usage)

                print(CLIConstants.HELP_COMMAND_VALIDARG.format(
                    Command_Name = command_list[1],
                    Command_Description = Command_Description,
                    Available_Subcommands = Formatted_Subcommands,
                    Command_Usage = Formatted_Usage
                ))

            case 2: #Invalid subcommand was sent by the user, prints standard invalid subcommand message followed by the help command without arguments.
                print(CLIConstants.INVALID_SUBCOMMAND.format(
                    Command = command_list[0],
                    Subcommand = command_list[1]
                ).removesuffix('\n'))
                self.execute(['help'])

            case 3: #Too many arguments were sent by the user, prints standard too many arguments message.
                print(CLIConstants.TOO_MANY_ARGUMENTS.format(Command = command_list[0]))

            case 4: #Prints help command without arguments.
                print(CLIConstants.HELP_COMMAND_NOARGS.format(
                    gui_Description = GuiCommand.Description,
                    call_Description = CallCommand.Description,
                    ticket_Description = TicketCommand.Description,
                    details_Description = DetailsCommand.Description,
                    help_Description = self.Description,
                    exit_Description = ExitCommand.Description
                ))


    def __validate(self, command_list:list[str]) -> int:
        """
        Private method: Validates the command and its arguments (if existant).

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
                if command_list[1] in CLIConstants.AVAILABLE_COMMANDS:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4


    def __Subcommands_Formatter(self, Subcommads_Dict:dict) -> str:
        """
        Subcommands dictionary formatter.

        Return:
            - 'This command does not accept any subcommands.' if the dictionary im empty.
            - A formatted string of subcommands and their description otherwise.

        Arguments:
            - Subcommads_Dict: A dictionary of subcommands of the selected command class.
        """

        Formatted_Subcommands = ''

        if Subcommads_Dict:
            for i in Subcommads_Dict:
                Formatted_Subcommands = Formatted_Subcommands + '\t- ' + str(i) + ': ' + Subcommads_Dict[i] + '\n'
            Formatted_Subcommands = Formatted_Subcommands.removesuffix('\n')
        else:
            Formatted_Subcommands = '\tThis command does not accept any subcommands.'
        
        return Formatted_Subcommands

    
    def __Usage_Formatter(self, Usage_List:list) -> str:
        """
        Usage list formatter.\n
        Returns a formatted string with the selected command class usage.

        Arguments:
            - Usage_List: A list of usage of the selected command class.
        """

        Formatted_Usage = ''

        for i in Usage_List:
            Formatted_Usage = Formatted_Usage + '\t- HAF> ' + str(i) + '\n'

        return Formatted_Usage.removesuffix('\n')


class ExitCommand():
    """
    'exit' command class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Attributes:
        - Description: Command description.
        - Subcommands: A dictionary of available subcommands and their description, blank 
        if no subcommand is available.
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

        Return:
            - True if sucessful.
            - False otherwise.

        Dependencies:
            - :mod:`__validation()`: For command validation.
        
        Arguments:
            - command_list: A formatted list containing the full command run by the user.
        """

        if self.__validate(command_list): #Command is valid, executes the command.
            print('- Closing HAF...')
            self.__driver.quit()
            return True
        else: #Command is invalid (has arguments), prints the standard invalid subcommand message.
            print(CLIConstants.INVALID_SUBCOMMAND.format(
                Command = command_list[0],
                Subcommand = command_list[1]
            ))
            return False


    def __validate(self, command_list:list[str]) -> bool:
        """
        Private method: Validates the command and its arguments (if existant).
        
        Return:
            - True if the command is valid.
            - False otherwise.
        
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