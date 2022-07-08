"""Constant values definition file."""

import pathlib


#URL Declaration:
class URL:
    """Group of URL related global variables."""

    PORTAL_URL = 'https://prosegur-smartit.onbmc.com/smartit/app/#/'
    TICKED_ID_PREFIX = 'https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/'


#Menu related delays (seconds):
class Menu:
    """Group of Fenix ITSM javascript menu related global variables."""

    ANIMATION_DELAY = 0.3
    TICKET_LOAD_DELAY = 1


class Paths:
    """Group of path related global variables."""

    __PROJECT_DIRECTORY = pathlib.Path(__file__).parent.resolve().parent.resolve()

    DICTIONARY_JSON_PATH = f'{__PROJECT_DIRECTORY}\\'
    CALL_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Call\\call.json'
    LOG_TXT_PATH = f'{__PROJECT_DIRECTORY}\\Log\\log.txt'
    PERSISTENT_JSON_PATH = f'{__PROJECT_DIRECTORY}\\Log\\persistent.json'
    CHROME_PROFILE_PATH = f'{__PROJECT_DIRECTORY}\\Source\\Driver\\ChromeProfile'
    CONFIG_INI_PATH = f'{__PROJECT_DIRECTORY}\\Source\\config.ini'


#This is not a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')