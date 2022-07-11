"""Defines and handles LogClass objects."""

#Native Modules:
from datetime import datetime

#Internal Modules:
from FileHandler.JsonHandler import *
from FileHandler.Config import ConfigClass
from Constants import Paths


class LogClass:
    """
    Handles ticket data for logging.\n
    *Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Private Attributes:
    - _register_type: Specifies what kind of log the object is (1 = Creation, 2 = Closing, 3 = Escalation) 
    - _register_ID: Is the ticket ID vinculated to the log object.
    - _attachment_ID: Attachment file ID's vinculated with the log (if existent).
    - _time: Is the time (dd/mm/yyyy hh:mm:ss) of object register to log file.
    - _CallJson: Loaded dict of the call information vinculated to the object.
    - _config: Loaded ConfigClass object with data from config.ini file.
    """

    def __init__(self, register_type:int, register_ID:str, attachment_ID:list = []) -> None:
        """
        Creates a new instace of LogClass:

        Arguments:
        - register_type: Specifies what kind of log the object is (1 = Creation, 2 = Closing, 3 = Escalation) 
        - register_ID: Is the ticket ID vinculated to the log object.

        Opitional argument:
        - attachment_ID: Attachment file ID's vinculated with the log.
        """

        self._register_type = int(register_type)
        self._register_ID = str(register_ID)
        self._attachment_ID = dict(attachment_ID)
        self._time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self._CallJson = LoadJson(Paths.CALL_JSON_PATH)
        self._config = ConfigClass()

    
    @property
    def GetID(self) -> str:
        """
        Gets ticket ID from this instace.

        Usage:
            >>> ID:str = log.GetID
        """

        return self._register_ID


    def LogRegister(self) -> None:
        """Converts LogClass object to string and appends it to log file."""

        divider_string = '----------------------------------------\n'
        open_ticket_string = '{current_time}\nOpened ticket: {ticket_ID}!\nDetails:\n- User ID: {user_ID}\n- Ticket type: {call_type}\n- Contact: {user_contact}\n- Hostname: {user_hostname}\n- Attachments: {attachment}\n'
        close_ticket_string = '{current_time}\nClosed ticket: {ticket_ID}!\nDetails:\n- Ticket type: {call_type}\n- Solution type: {solution_type}\n'
        escalate_ticket_string = '{current_time}\nEscalated ticket: {ticket_ID}!\nDetails:\n- Ticket type: {call_type}\n- Escalated team: {escalated_team}\n- Attachments: {attachment}\n'

        self._time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        LogFile = open(Paths.LOG_TXT_PATH, 'a')

        match self._register_type:
            case 1:
                LogFile.write(divider_string)
                LogFile.write(open_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID, user_ID = self._CallJson['data']['matricula'], call_type = self._CallJson['data']['tipo'], user_contact = self._CallJson['data']['contato'], user_hostname = self._CallJson['data']['hostname'], attachment = self._attachment_ID))
                LogFile.write(divider_string + '\n')

            case 2: 
                LogFile.write(divider_string)
                LogFile.write(close_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID))
                LogFile.write(divider_string + '\n')

            case 3:
                LogFile.write(divider_string)
                LogFile.write(escalate_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID))
                LogFile.write(divider_string + '\n')

        self._config.UpdateInfo('counter')
        
        LogFile.close()
        self.__SaveLog()


    def PrintLog(self) -> None:
        """Converts LogClass object to string and prints it to terminal."""

        attachments = self._attachment_ID
        if len(attachments) == 0:
            attachments = 'None'

        open_ticket_string = '{current_time}\nOpened ticket: {ticket_ID}!\nDetails:\n- User ID: {user_ID}\n- Ticket type: {call_type}\n- Contact: {user_contact}\n- Hostname: {user_hostname}\n- Attachments: {attachment}\n'
        close_ticket_string = '{current_time}\nClosed ticket: {ticket_ID}!\nDetails:\n- Ticket type: {call_type}\n- Solution type: {solution_type}\n'
        escalate_ticket_string = '{current_time}\nEscalated ticket: {ticket_ID}!\nDetails:\n- Ticket type: {call_type}\n- Escalated team: {escalated_team}\n- Attachments: {attachment}\n'

        match self._register_type:
            case 1:
                print(open_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID, user_ID = self._CallJson['data']['matricula'], call_type = self._CallJson['data']['tipo'], user_contact = self._CallJson['data']['contato'], user_hostname = self._CallJson['data']['hostname'], attachment = attachments))

            case 2: 
                print(close_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID))

            case 3:
                print(escalate_ticket_string.format(current_time = self._time, ticket_ID = self._register_ID))


    def LoadLog(self) -> bool:
        """
        If available, will set the object to the state of the last register.\n
        Works by reading data from persistent.json file updated by :mod:`__SaveLog()` method.

        Return:
        - True: The object was successfully loaded to the previous state.
        - False: No log was available to load the state from.
        """
        if self._config.GetCounter > 0:
            PersistentJson = LoadJson(Paths.PERSISTENT_JSON_PATH)

            self._register_type = int(PersistentJson['Lastest_Log']['type'])
            self._register_ID = str(PersistentJson['Lastest_Log']['id'])
            self._attachment_ID = list(PersistentJson['Lastest_Log']['attachment'])
            self._time = str(PersistentJson['Lastest_Log']['time'])
            self._CallJson = PersistentJson

            return True
        else:
            return False

    
    def __SaveLog(self) -> None:
        """
        Saves the current state as the lastest register for future use.\n
        Works by saving current state to persistent.json which is read by :mod:`LoadLog()` method.
        """

        Log_dict = {'Lastest_Log': {'type': '', 'id': '', 'attachment': '', 'time': ''}}
        Log_dict['Lastest_Log']['type'] = self._register_type
        Log_dict['Lastest_Log']['id'] = self._register_ID
        Log_dict['Lastest_Log']['attachment'] = self._attachment_ID
        Log_dict['Lastest_Log']['time'] = self._time

        Log_dict['data'] = self._CallJson['data']

        SaveJson(Log_dict, Paths.PERSISTENT_JSON_PATH)


def CreateEmptyLog() -> LogClass:
    """Creates blank LogClass object."""

    return LogClass(0, None)


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')