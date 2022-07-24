"""Defines and handles ConfigClass objects."""

#Native Modules:
import configparser

#Internal Modules:
from HAF.Constants import Paths, GUIConstants


class ConfigClass:
    """
    General user configuration class.
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Private Attributes:
        - __email: Microsoft e-mail.
        - __password: Microsoft account password (not hashed).
        - __counter: Number (integer) of logs registered.
        - __language: A string for GUI language selection.
        - __auto_open_flag: A bool indicating whether GUI should 
        automatically open when the program is executed or not.
    """

    def __init__(self) -> None:
        """Creates a new instace of ConfigClass."""

        #Reads 'config.ini' file.
        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        self.__email = str(configfile['Microsoft']['email'])
        self.__password = str(configfile['Microsoft']['password'])
        self.__counter = int(configfile['Log']['counter'])
        self.__language = str(configfile['GUI']['language'])
        self.__auto_open_flag = bool(int(configfile['GUI']['auto_open']))


    @property
    def GetEmail(self) -> str:
        """
        Returns Microsoft account email string from this instance.
        
        Usage:
            >>> email:str = config.GetEmail
        """

        return str(self.__email)


    @property
    def GetPassword(self) -> str:
        """
        Returns Microsoft account password (not hashed) string from this instance.
        
        Usage:
            >>> password:str = config.GetPassword
        """

        return str(self.__password)


    @property
    def GetCounter(self) -> int:
        """
        Returns the number of logs registered in log.txt file.
        
        Usage:
            >>> log_counter:int = config.GetCounter
        """

        return int(self.__counter)

    
    @property
    def GetLanguage(self) -> str:
        """
        Returns the string of the language selection for the GUI.
        
        Usage:
            >>> lang:str = config.GetLanguage
        """

        return str(self.__language)

    
    @property
    def AutoOpenStatus(self) -> bool:
        """
        Returns:
            - True if the GUI should auto open when the program starts.
            - False otherwise.
        
        Usage:
            >>> auto_open_flag:bool = config.AutoOpenStatus
        """

        return bool(int(self.__auto_open_flag))


    def UpdateCredentials(self, new_email:str, new_password:str) -> None:
        """
        Updates Microsoft credentials information in 'config.ini' file.

        Arguments:
            - new_email: A string for email section update in 'config.ini' file.
            - new_password: A string for password section update in 'config.ini' file.

        Dependencies:
            - :mod:`__Reload()`: For current data update.
            - :mod:`__SaveConfig()`: For 'config.ini' file update.
        """

        self.__Reload()
        self.__email = str(new_email)
        self.__password = str(new_password)
        self.__SaveConfig()


    def UpdateCounter(self) -> None:
        """
        Adds one to log counter and saves update to 'config.ini' file.

        Dependencies:
            - :mod:`__Reload()`: For current data update.
            - :mod:`__SaveConfig()`: For config.ini update.
        """
        
        self.__Reload()
        self.__counter += 1
        self.__SaveConfig()


    def UpdateLanguage(self, selected_lang:str) -> None:
        """
        Changes language selection in 'config.ini' file.

        Arguments:
            - selected_lang: A string for language selection update in 'config.ini' file.

        Dependencies:
            - :mod:`__Reload()`: For current data update.
            - :mod:`__SaveConfig()`: For 'config.ini' file update.
        """

        #Checks if passed string is valid.
        if str(selected_lang) in GUIConstants.VALID_LANGS:
            self.__Reload()
            self.__language = str(selected_lang)
            self.__SaveConfig()


    def UpdateAutoOpenFlag(self, auto_open_status:bool) -> None:
        """
        Changes auto_open flag in 'config.ini' file.

        Arguments:
            - auto_open_status: A boolean for auto_open flag update in 'config.ini' file.

        Dependencies:
            - :mod:`__Reload()`: For current data update.
            - :mod:`__SaveConfig()`: For 'config.ini' file update.
        """

        self.__Reload()
        self.__auto_open_flag = bool(int(auto_open_status))
        self.__SaveConfig()


    def __Reload(self) -> None:
        """Private method: Reloads data from file, should be used before calling a file update."""

        #Reads 'config.ini' file.
        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        self.__email = str(configfile['Microsoft']['email'])
        self.__password = str(configfile['Microsoft']['password'])
        self.__counter = int(configfile['Log']['counter'])
        self.__language = str(configfile['GUI']['language'])
        self.__auto_open_flag = bool(configfile['GUI']['auto_open'])

    
    def __SaveConfig(self) -> None:
        """Private method: Writes instace data to 'config.ini' file."""

        #Reads 'config.ini' file.
        configfile = configparser.ConfigParser()
        configfile.read(Paths.CONFIG_INI_PATH)

        #Updates data with this instance information.
        configfile['Microsoft']['email'] = self.__email
        configfile['Microsoft']['password'] = self.__password
        configfile['Log']['counter'] = str(self.__counter)
        configfile['GUI']['language'] = self.__language
        configfile['GUI']['auto_open'] = str(int(self.__auto_open_flag))

        #Saves information to file.
        with open(Paths.CONFIG_INI_PATH, 'w') as f:
            configfile.write(f)


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')