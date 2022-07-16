"""
Constant values definition file.
* None of these values should change during runtime.
"""

#Native Modules:
import pathlib


class URL:
    """Group of URL related global variables."""

    PORTAL_URL = 'https://prosegur-smartit.onbmc.com/smartit/app/#/'
    SMART_RECORDER_URL = 'https://prosegur-smartit.onbmc.com/smartit/app/#/create/smart-recorder'
    TICKED_ID_PREFIX = 'https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/'


class MicrosoftLogin:
    """Group of Microsoft login page global variables"""

    #All of the values are in seconds.
    ANIMATION_DELAY = 1


class Menu:
    """Group of Fenix ITSM javascript menu related global variables."""

    #All of the values are in seconds.
    GENERAL_ANIMATION_DELAY = 0.4

    USER_LOAD_DELAY = 2

    TICKETMENU_LOAD_DELAY = 8
    TICKETPAGE_LOAD_DELAY = 1
    TICKETEDITOR_LOAD_DELAY = 1

    DESIGNATION_LOAD_DELAY = 0.7
    DESIGNATIONMENU_LOAD_DELAY = 2
    DESIGNATIONMENU_TEAMLOAD_DELAY = 1


class Paths:
    """
    Group of path related global variables.
    * Uses double undescore to specify private methods instead of the convenional single underscore.
    """

    __PROJECT_DIRECTORY = pathlib.Path(__file__).parent.resolve().parent.resolve()

    ATTACHMENTS_FOLDER_PATH = f'{__PROJECT_DIRECTORY}\\Autofill Dictionary\\Attachments\\'
    DICTIONARY_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Autofill Dictionary\\dictionary.json'
    CALL_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Call\\call.json'
    LOG_TXT_PATH = f'{__PROJECT_DIRECTORY}\\Log\\log.txt'
    PERSISTENT_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Log\\persistent.json'
    CHROME_PROFILE_PATH = f'{__PROJECT_DIRECTORY}\\HAF\\Driver\\ChromeProfile'
    CONFIG_INI_PATH = f'{__PROJECT_DIRECTORY}\\HAF\\config.ini'


class LogConstants:
    """
    Group of LogClass related global variables.
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.
    """

    DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

    TICKET_CREATED = 1
    TICKET_CLOSED = 2
    TICKET_ESCALATED = 3
    TICKET_LOADPERSISTENT = 4
    PROCESS_TYPES = ['Created', 'Closed', 'Escalated', 'Invalid']

    LOG_DIVIDER = '----------------------------------------------------------------------'
    LOG_TEMPLATE = (
        '{Current_Time}\n'
        '{Process_Type} ticket number {Ticket_ID}, details:\n'
        '\t- Ticket Type: "{Ticket_Type}"\n'
        '\t- Attachments: {Ticket_Attachments}\n'
        '\t- Desginated Team: {Designated_Team}\n'
        '\t- Solution Type: {Ticket_Solution}\n\n'
        ''
        'User details:\n'
        '\t- User ID: {User_ID}\n'
        '\t- Contact Info: {User_Contact}\n'
        '\t- Hostname/IP: {User_Hostname}\n'
    )

    HOSTNAME_EXCEPTION_LIST = [
        'mfa',
        'prouser_activate',
        'prouser_unlock',
        'prouser_changepw'
    ]


class CLIConstants:
    """Group of CLI ralated global varialbes, mostly console logging templates."""

    AVAILABLE_COMMANDS = ['call', 'ticket', 'details', 'help', 'exit']

    INVALID_COMMAND = '"{Command}" is not a valid command!\nUse "help" for more information.\n'
    INVALID_SUBCOMMAND = 'Subcommand "{Subcommand}" is not valid for "{Command}" command.\n'
    TOO_MANY_ARGUMENTS = 'Too many arguments were given to "{Command}" command!\nUse "help {Command}" for more information.\n'
    TOO_FEW_ARGUMENTS = 'Missing arguments to "{Command}" command!\nUse "help {Command}" for more information.\n'

    HELP_COMMAND_NOARGS = (
        'For specific command information use: "help [command_name]"\n\n'
        'Commands:\n'
        '\t- call: {call_Description}\n'
        '\t- ticket: {ticket_Description}\n'
        '\t- details: {details_Description}\n'
        '\t- help: {help_Description}\n'
        '\t- exit: {exit_Description}\n'
    )
    HELP_COMMAND_VALIDARG = (
        '"{Command_Name}" command:\n'
        '\t{Command_Description}\n\n'
        'Subcommands:\n'
        '{Available_Subcommands}\n\n'
        'Usage:\n'
        '{Command_Usage}\n'
    )
    

#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')