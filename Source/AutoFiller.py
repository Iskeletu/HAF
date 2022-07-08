"""
Fenix ITSM navigator Bot.\n
Main script File.

Uses Python Selenium to navigate through Helix ITSM and manage tickets,
it is currently capable of opening, closing and escalating ticket with
data from incoming calls using a ticket dictionary (can be safely edited).

- For usage see 'Readme.md'.
- See 'LICENSE' for more infomation.

Fábio Gandini - 28/06/2022
"""

from typing import NoReturn

from selenium import webdriver

#Files.
from Driver.DriverHandler import LoadDriver
from FileHandler.Logger import *
from CLI.CommandLineInterface import *
from Ticket.TicketHandler import TicketProcessor


def Start(driver:webdriver.Chrome, Lastest_Ticket:LogClass) -> NoReturn:
    """Main AutoFiller Function."""

    #Main loop.
    exit_flag = False
    while exit_flag == False:
        print('> ', end = '')
        command = input()

        match command:
            case 'call.register':
                Lastest_Ticket = TicketProcessor(driver)
                print('- Done! Type "details" for more details.')

            case 'details':
                if Lastest_Ticket.LoadLog() == True:
                    Lastest_Ticket.PrintLog()
                else:
                    print('ERROR: No previous logs registered!\n')
            
            case 'exit':
                exit_flag = True

            case _:
                print('Invalid command\n')

    driver.quit()
    exit()


#Script file.
if __name__ == "__main__":
    Start(LoadDriver(), CreateEmptyLog())