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

#Native Modules:
from typing import NoReturn

#External Modules:
from selenium import webdriver

#Internal Modules:
from Driver.DriverHandler import LoadDriver
from CLI.CommandLineInterface import CommandLineInterface


def Start(driver:webdriver.Chrome, exit_flag:bool) -> NoReturn:
    """
    Main HAF (Helix AutoFiller) Function.
    
    Arguments:
    - driver: A loaded Chrome webdriver object, mainly to be 
    passed to CLI for command execution.
    - exit_flag: A bool indicating whether or not the main loop 
    should finish.

    Dependencies:
    - :mod:`CommandLineInterface()`: To handle user input and 
    execute commands.
    """

    #Main loop.
    while not exit_flag:
        exit_flag = CommandLineInterface(driver)

    exit()


#Script file.
if __name__ == "__main__":
    Start(LoadDriver(), False)