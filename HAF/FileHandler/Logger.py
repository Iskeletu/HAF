"""Defines and handles LogClass objects."""

#Native Modules:
from datetime import datetime

#Internal Modules:
from HAF.FileHandler.JsonHandler import *
from HAF.Constants import Paths, LogConstants
from HAF.FileHandler.Config import ConfigClass


class LogClass():
    """
    Handles ticket data for logging.
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.
    
    Private Attributes:
        - __log_type: Integer indicating log type (1- Created | 2- Closed | 3- Escalated | 4- Persistent).
        - __ticket_ID: String of the ticket ID returned from its creation process.
        - __call_data: Loaded call data dictionary.
        - __time: String indication date and hour of object creation or log time.
        - __ticket_data: A loaded dictionary selected from the ticket dictionary
        - __config: A loaded ConfigClass object.
    """

    def __init__(self, log_type:int, ticket_ID:str = '') -> None:
        """
        Creates a new instance of LogClass.

        Arguments:
            - log_type: A integer value indicating what type of log this is, assigned to __log_type. 
            Check LogConstants class in Constants module for valid values.

        Optional Arguments:
            - ticket_ID: String witht he ticket ID to be assigned to __ticket_ID (should be passed if 
            log_type is not 4).

        Dependencies:
            - :mod:`__LoadPersistent()`: For persistent file loading.
        """

        #Checks whether data should be load from persistent or standard files.
        if log_type == 4:
            self.__LoadPersistent()
        else:
            self.__log_type = int(log_type)
            self.__ticket_ID = str(ticket_ID)

            self.__call_data = LoadJson(Paths.CALL_JSON_PATH)

            self.__time = datetime.now().strftime(LogConstants.DATE_FORMAT)

        self.__ticket_data:dict = LoadJson(Paths.DICTIONARY_JSON_PATH)[self.__call_data['Required']['Call_Type']]

        self.__config = ConfigClass()


    @property
    def GetTicketID(self) -> str:
        """
        Property: Gets __ticke_ID string from this instace.

        Usage:
            >>> value:ticket_ID = LogClass.GetTicketID
        """

        return self.__ticket_ID


    def UpdateType(self, log_type:int) -> None:
        """
        Changes log type.
        * Cannot be used for persistent loading.
        """

        self.__log_type = int(log_type)

    
    def ConvertToString(self) -> str:
        """
        Converts this instance to a string for logging and/or printing.
        
        Dependencies:
            - :mod:`__AttachmentsFormatter()`: For attachment list conversion to string.
            - :mod:`__GetDesignation()`: For team designation string if existent.
            - :mod:`__GetSolution()`: For solution value as a string if it applies to this log type.
            - :mod:`__GetHostname()`: For hostname string if it applies to this log type.
        """

        return LogConstants.LOG_TEMPLATE.format(
            Current_Time = self.__time,
            Process_Type = LogConstants.PROCESS_TYPES[self.__log_type - 1],
            Ticket_ID = self.__ticket_ID,
            Ticket_Type = self.__call_data['Required']['Call_Type'],
            Ticket_Attachments = self.__AttachmentsFormatter(),
            Designated_Team = self.__GetDesignation(),
            Ticket_Solution = self.__GetSolution(),
            User_ID = self.__call_data['Required']['User_ID'],
            User_Contact = self.__call_data['Required']['Contact'],
            User_Hostname = self.__GetHostname()
        )


    def Register(self) -> None:
        """
        Logs this intance to file and calls for persistent file update.

        Dependencies:
            - :mod:`__ConvertToString()`: For instance to string convertion.
            - :mod:`__SavePersistent()`: For persistent file update.
        """

        with open(Paths.LOG_TXT_PATH, 'a') as logfile:
            logfile.write(
                LogConstants.LOG_DIVIDER + '\n' +
                self.ConvertToString() + 
                LogConstants.LOG_DIVIDER + '\n\n\n'
            )

        self.__config.UpdateCounter()
        self.__SavePersistent()


    def __SavePersistent(self) -> None:
        """Updates persistent file with this instance data."""

        data = {
            'Lastest_Log': {
                'Ticket_Data': {
                    'Time': self.__time,
                    'Process_Type': self.__log_type,
                    'ID': self.__ticket_ID,
                    'Ticket_Type': self.__call_data['Required']['Call_Type'],
                    'Solution': self.__call_data['Optional']['Solution']
                },
                'User_Data': {
                    'User_ID': self.__call_data['Required']['User_ID'],
                    'Contact': self.__call_data['Required']['Contact'],
                    'Hostname': self.__call_data['Required']['Hostname']
                }
            }
        }

        SaveJson(data, Paths.PERSISTENT_JSON_PATH)


    def __LoadPersistent(self) -> None:
        """Updates current instace infomation with persistent file data."""

        persistent_json = LoadJson(Paths.PERSISTENT_JSON_PATH)

        self.__log_type = int(persistent_json['Lastest_Log']['Ticket_Data']['Process_Type'])
        self.__ticket_ID = str(persistent_json['Lastest_Log']['Ticket_Data']['ID'])

        self.__call_data = {
            'Required': {
                'User_ID': persistent_json['Lastest_Log']['User_Data']['User_ID'],
                'Contact': persistent_json['Lastest_Log']['User_Data']['Contact'],
                'Hostname': persistent_json['Lastest_Log']['User_Data']['Hostname'],
                'Call_Type': persistent_json['Lastest_Log']['Ticket_Data']['Ticket_Type']
            },
            'Optional': {
                'Solution': int(persistent_json['Lastest_Log']['Ticket_Data']['Solution']),
                'Variable': 'None' #TODO
            }
        }
        
        self.__time = persistent_json['Lastest_Log']['Ticket_Data']['Time']

    
    def __AttachmentsFormatter(self) -> str:
        """
        Attachment list to string conversor.

        Return:
            - 'None' if the list is empty.
            - A formatted string of attachments divided by commas otherwise.
        """

        try:
            unformatted_attachments = self.__ticket_data['Attachment']

            formatted_attachments = ''
            for i in unformatted_attachments:
                formatted_attachments = formatted_attachments + str(i) + ', '
            formatted_attachments = formatted_attachments.removesuffix(', ')
        except KeyError:
            formatted_attachments = 'None'

        return formatted_attachments
            

    def __GetDesignation(self) -> str:
        """
        Gets the designated team string.

        Return:
            - Ticket template designation if specified.
            - 'VE.INFRA.BR.SERVICE DESK' (default designation) otherwise.
        """

        try:
            designated_team = str(self.__ticket_data['Team'])
        except KeyError:
            designated_team = 'VE.INFRA.BR.SERVICE DESK'
        return designated_team

    
    def __GetSolution(self) -> str:
        """
        Gets the solution selection and coverts it to string.

        Return:
            - User solution (as a string) selection if ticket log is 2 (closed).
            - 'Does not apply' otherwise.
        """

        if self.__log_type == 2:
            solution = str(self.__call_data['Optional']['Solution'])
        else:
            solution = 'Does not apply'
        return solution


    def __GetHostname(self) -> str:
        """
        Gets hostname string from __call_data.

        Return:
            - 'Does not apply' if the call type is in the hostname exception list.
            - __call_data['Required']['Hostname'] value otherwise.
        """

        if self.__call_data['Required']['Call_Type'] in LogConstants.HOSTNAME_EXCEPTION_LIST:
            hostname = 'Does not apply'
        else:
            hostname = str(self.__call_data['Required']['Hostname'])
        return hostname


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')