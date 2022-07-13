"""Defines and handles ConfigClass objects."""

#Native Modules:
import configparser

#Internal Modules:
from Constants import Paths


class ConfigClass:
    """
    General user configuration class.
    * Uses double undescore to specify private methods instead of the convenional single underscore.

    Private Attributes:
        - __email: Microsoft e-mail.
        - __password: Microsoft account password (not hashed).
        - __counter: Number of logs registered.
    """

    def __init__(self) -> None:
        """Creates a new instace of ConfigClass."""

        #Reads 'config.ini' file.
        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        self.__email = str(configfile['Microsoft']['email'])
        self.__password = str(configfile['Microsoft']['password'])
        self.__counter = int(configfile['Log']['counter'])


    @property
    def GetEmail(self) -> str:
        """
        Returns Microsoft account email string from this instance.
        
        Usage:
            >>> email:str = config.GetEmail
        """

        return self.__email


    @property
    def GetPassword(self) -> str:
        """
        Returns Microsoft account password (not hashed) string from this instance.
        
        Usage:
            >>> password:str = config.GetPassword
        """

        return self.__password


    @property
    def GetCounter(self) -> int:
        """
        Returns the number of logs registered in log.txt file.
        
        Usage:
            >>> log_counter:int = config.GetCounter
        """

        return int(self.__counter)


    def UpdateCounter(self) -> None:
        """
        Adds one to log counter and saves update to 'config.ini' file.

        Dependencies:
            - :mod:`__SaveConfig()`: For file update.
        """
        
        self.__counter += 1
        self.__SaveConfig()

    
    def __SaveConfig(self) -> None:
        """Writes instace data to 'config.ini' file."""

        #Reads 'config.ini' file.
        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        #Updates data with this instance information.
        configfile['Microsoft']['email'] = self.__email
        configfile['Microsoft']['password'] = self.__password
        configfile['Log']['counter'] = self.__counter

        #Saves information to file.
        with open(Paths.CONFIG_INI_PATH, 'w') as f:
            configfile.write(f)


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')