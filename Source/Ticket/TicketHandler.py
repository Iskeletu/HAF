"""Navigates Fenix ITSM portal and manages ticket creation, escalation and closing."""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#Files.
from FileHandler.JsonHandler import LoadJson
from FileHandler.Logger import LogClass
from Constants import *


def __MenuNavigator(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> str: #TODO ATTACHMENTS
    """
    Navigates javascrpit menu during ticket creation and returns the ticket ID as a string.

    Arguments:
    - driver: A loaded Chrome webdriver object.
    - call_data: Dict with call data.
    - ticket_data: Dict with ticket data.
    """

    action = ActionChains(driver)
    delay = 0.3 #Menu animation delay.

    #Ticket description.
    ticket_body = str(ticket_data['body']).format(hostname = call_data['hostname'], contact = call_data['contato'])
    action.send_keys(Keys.TAB + ticket_body)
    action.perform()

    match ticket_data['type']:
        case 'ticket':
            #Fills "How is this affecting you?" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(delay)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(delay)

            #Fills "Degree of affectation" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(delay)
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(delay)

            #Fills "Application" field.
            action.send_keys(Keys.TAB + ticket_data['application'])
            action.perform()
            time.sleep(delay)

            #Fills "Phone contact" field.
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + call_data['contato'])
            action.perform()
            time.sleep(delay)

            #opens ticket
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(delay)
            action.send_keys(Keys.TAB + Keys.TAB) #ADD SPACE
            action.perform()
            time.sleep(1)

        case 'mfa':
            #Opens ticket.
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(delay)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(1)

    return driver.current_url.removeprefix('https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/')


def __OpenTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass:
    """
    Open a ticket and returns a LogClass object with it's details.
    
    Dependencies:
    - :mod:`__MenuNavigator()`: To navigate the javascript menu (Selenium 
    API has a hard time locating elements there).

    Arguments:
    - driver: A loaded Chrome webdriver object.
    - call_data: Dict with call data.
    - ticket_data: Dict with ticket data.
    """

    driver.get('https://prosegur-smartit.onbmc.com/smartit/app/#/create/smart-recorder')

    main_bar = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/smart-recorder-input/div/div[2]')
    main_bar.send_keys('@' + call_data['matricula'])
    time.sleep(2)
    main_bar.send_keys(Keys.ENTER + ticket_data['type'])

    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div/div/div[2]/rs/div/div[2]/rs-dwp-catalog/div/div/div/div[1]/i[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[3]/button[1]').click()
    time.sleep(7)

    ticket_ID = __MenuNavigator(driver, call_data, ticket_data)
    return LogClass(1, ticket_ID)


def __CloseTicket(ticket_ID, driver:webdriver.Chrome) -> LogClass: #TODO
    """"""

    TODO = True


def __EscalateTicket() -> LogClass: #TODO
    """"""

    TODO = True


def TicketProcessor(driver:webdriver.Chrome, *args) -> LogClass:
    """
    Processes call data into a ticket and returns a log object with it's deatils.

    Dependencies:
    - :mod:`__OpenTicket()`: For ticket creation.
    - :mod:`__CloseTicket()`: For ticket closing.
    - :mod:`__EscalateTicket()`: For ticket escalation.

    Arguments:
    - driver: A loaded Chrome webdriver object.
    - *args: 
    """

    call_data = LoadJson(Paths.CALL_JSON_PATH)['data']
    ticket_data = LoadJson(Paths.DICTIONARY_JSON_PATH)[call_data['tipo']]

    match ticket_data['process-type']:
        case 'open':
            log = __OpenTicket(driver, call_data, ticket_data)

        case 'close':
            log = __CloseTicket()

        case 'escalate':
            log = __EscalateTicket()

    return log


#Not a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')