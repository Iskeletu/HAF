"""Constant values definition file."""

#Native Modules:
import pathlib


#URL Declaration:
class URL:
    """Group of URL related global variables."""

    PORTAL_URL = 'https://prosegur-smartit.onbmc.com/smartit/app/#/'
    SMART_RECORDER_URL = 'https://prosegur-smartit.onbmc.com/smartit/app/#/create/smart-recorder'
    TICKED_ID_PREFIX = 'https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/'


#Menu related delays (seconds):
class Menu:
    """Group of Fenix ITSM javascript menu related global variables."""

    ANIMATION_DELAY = 0.4
    TICKET_LOAD_DELAY = 1
    USER_LOAD_DELAY = 2
    MENU_LOAD_DELAY = 7


class Paths:
    """
    Group of path related global variables.\n
    *Uses double undescore to specify private methods instead of the convenional single underscore.
    """
    

    __PROJECT_DIRECTORY = pathlib.Path(__file__).parent.resolve().parent.resolve()

    ATTACHMENTS_FOLDER_PATH = f'{__PROJECT_DIRECTORY}\\Autofill Dictionary\\Attachments\\'
    DICTIONARY_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Autofill Dictionary\\dictionary.json'
    CALL_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Call\\call.json'
    LOG_TXT_PATH = f'{__PROJECT_DIRECTORY}\\Log\\log.txt'
    PERSISTENT_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Log\\persistent.json'
    CHROME_PROFILE_PATH = f'{__PROJECT_DIRECTORY}\\Source\\Driver\\ChromeProfile'
    CONFIG_INI_PATH = f'{__PROJECT_DIRECTORY}\\Source\\config.ini'


class Types:
    """Group of ticket types global variables."""

    TICKET_CREATION = 1
    TICKET_CLOSING = 2
    TICKET_ESCALATION = 3


class CLI:
    """Group of global standard strings for console feedback and other CLI related variables."""

    AVAILABLE_COMMANDS = ['details', 'help', 'exit']

    INVALID_COMMAND = '"{Command}" is not a valid command!\nUse "help" for more information.\n'
    INVALID_SUBCOMMAND = 'Subcommand "{Subcommand}" is not valid.'
    TOO_MANY_ARGUMENTS = 'Too many arguments were given to "{Command}" command!\nUse "help" for more information.\n'
    


#This is not a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')