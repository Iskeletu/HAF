"""Defines and handles LogClass objects."""

#Native Modules:
from datetime import datetime

#Internal Modules:
from Constants import Paths, LogConstants
from FileHandler.JsonHandler import *
from FileHandler.Config import ConfigClass


class LogClass(object):
    """
    Handles ticket data for logging.
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.
    """

    def __init__(self, log_type:int, ticketID:str):
        self.__log_type = int(log_type)
        self.__ticket_ID = str(ticketID)

        self.__call_data = LoadJson(Paths.CALL_JSON_PATH)
        self.__ticket_data = LoadJson(Paths.DICTIONARY_JSON_PATH)[self.__call_data['obrigatório']['tipo']]

        self.__config = ConfigClass()

        self.__time = datetime.now().strftime(LogConstants.DATE_FORMAT)


    @property
    def GetTicketID(self) -> str:
        return self.__ticket_ID


    def UpdateType(self, log_type:int) -> None:
        self.__log_type = int(log_type)

    
    def ConvertToString(self):
        return LogConstants.LOG_TEMPLATE.format(
                Current_Time = self.__time,
                Process_Type = LogConstants.PROCESS_TYPES[self.__log_type - 1],
                Ticket_ID = self.__ticket_ID,
                Ticket_Type = self.__call_data['obrigatório']['tipo'],
                Ticket_Attachments = self.__AttachmentsFormatter(),
                Designated_Team = self.__GetDesignation(),
                Ticket_Solution = self.__GetSolution(),
                User_ID = self.__call_data['obrigatório']['matrícula'],
                User_Contact = self.__call_data['obrigatório']['contato'],
                User_Hostname = self.__call_data['obrigatório']['hostname'],
        )


    def Register(self):
        with open(Paths.LOG_TXT_PATH, 'a') as logfile:
            logfile.write(
                LogConstants.LOG_DIVIDER + '\n' +
                self.ConvertToString() + 
                LogConstants.LOG_DIVIDER + '\n\n\n'
                )

        self.__config.UpdateCounter()
        self.__SavePersistent()


    def __SavePersistent(self):
        TODO = True

    
    def __AttachmentsFormatter(self) -> str:
        unformatted_attachments = self.__ticket_data['attachment']

        if not unformatted_attachments:
            return 'None'
        else:
            formatted_attachments = ''

            for i in unformatted_attachments:
                formatted_attachments = formatted_attachments + str(i) + ', '

            return formatted_attachments.removesuffix(', ')

    
    def __GetDesignation(self) -> str:
        if self.__log_type == 3:
            return str(self.__ticket_data['team'])
        else:
            return 'VE.INFRA.BR.SERVICE DESK'

    
    def __GetSolution(self) -> str:
        if self.__log_type == 2:
            return str(self.__call_data['opicional']['solução'])
        else:
            return 'Does not apply'



#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')