"""Defines and handles ConfigClass objects."""

import configparser

#Files:
from Constants import Paths


class ConfigClass:
    """
    General user configuration object.\n
    *Uses double undescore to specify private methods instead of the convenional single underscore.

    Private Attributes:
    - _email: Microsoft e-mail.
    - _password: Microsoft account password (not hashed).
    - _counter: Number of logs registered.
    - _attachments: Number of attachments registered.
    """

    def __init__(self) -> None:
        """
        Creates a new instace of ConfigClass.
        """

        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        self._email = str(configfile['Microsoft']['email'])
        self._password = str(configfile['Microsoft']['password'])
        self._counter = int(configfile['Log']['counter'])
        self._attachments = int(configfile['Log']['attachments'])


    @property
    def GetEmail(self) -> str:
        """
        Returns user Microsoft account email string.
        
        Usage:
            >>> email:str = config.GetEmail
        """

        return self._email


    @property
    def GetPassword(self) -> str:
        """
        Returns user Microcroft account password string (not hashed).
        
        Usage:
            >>> password:str = config.GetPassword
        """

        return self._password


    @property
    def GetCounter(self) -> int:
        """
        Returns the number of logs registered.
        
        Usage:
            >>> log_counter:int = config.GetCounter
        """

        return self._counter


    @property
    def GetAttachments(self) -> int:
        """
        Returns the number of attachments registered.
        
        Usage:
            >>> attachment_counter:int = config.GetAttachemnts
        """

        return self._attachments


    def UpdateCounter(self) -> None:
        """
        Adds one to log counter.\n
        Calls :mod:`__SaveConfig()` for file information update.
        """
        
        self._counter + 1
        self.__SaveConfig()


    def UpdateAttachments(self) -> None:
        """
        Adds one to attachment counter.\n
        Calls :mod:`__SaveConfig()` for file information update.
        """

        self._attachments + 1
        self.__SaveConfig()

    
    def __SaveConfig(self) -> None:
        """Writes object data to 'config.ini' file."""

        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        configfile['Microsoft']['email'] = self._email
        configfile['Microsoft']['password'] = self._password
        configfile['Log']['counter'] = self._counter
        configfile['Log']['attachment'] = self._attachments

        with open(Paths.CONFIG_INI_PATH, 'w') as f:
            configfile.write(f)


#This is NOT a script file.
if __name__ == '__main__':
    todo = True
    #exit('ERROR: Not a script file!')