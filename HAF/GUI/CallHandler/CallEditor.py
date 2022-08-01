"""This file handles call data registering for GUI."""

#External Modules:
from selenium import webdriver

#Internal Modules:
from HAF.Ticket.TicketHandler import TicketProcessor
from HAF.FileHandler.JsonHandler import SaveJson
from HAF.Constants import Paths


def __ClearCall() -> None:
    """Private Function: Sets call.json to default state."""

    blank_call = {
        'Required': {
            'User_ID': '',
            'Contact': '',
            'Hostname': '',
            'Call_Type': ''
        },
        'Optional': {
            'Solution': 0,
            'Variable': ''
        }
    }

    SaveJson(blank_call, Paths.CALL_JSON_PATH)


def NewCall(
    driver:webdriver.Chrome,
    user_ID:str,
    contact:str,
    hostname:str,
    call_type:str,
    solution:int,
    variable:str
) -> None: 
    """
    This function creates a new call data dictionary and saves to file.
    
    Arguments:
        - user_ID: A string for user ID value.
        - contact: A string for user contact value.
        - hostname: A string for hostname/IP value.
        - call_type: A string indicating call type.
        - solution: A integer indicating solution type.
        - variable: A string for variable content for ticket template.

    Dependencies:
        - :mod:`__ClearCall()`: To set call.json to default state after register.
    """

    new_call = {
        'Required': {
            'User_ID': str(user_ID),
            'Contact': str(contact),
            'Hostname': str(hostname),
            'Call_Type': str(call_type)
        },
        'Optional': {
            'Solution': int(solution),
            'Variable': str(variable)
        }
    }

    SaveJson(new_call, Paths.CALL_JSON_PATH)

    TicketProcessor(driver)

    __ClearCall()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')