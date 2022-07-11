"""Navigates Fenix ITSM portal and manages ticket creation, escalation and closing."""

#Native Modules.
import time

#External Modules.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

#Native Modules.
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

    #Changes focust to driver (menu navigation won't work minimized).
    try:
        driver.maximize_window()
    except WebDriverException:
        pass #Webdriver gives unknown eception if driver is minimezed for some reason...

    time.sleep(Menu.MENU_LOAD_DELAY)
    action = ActionChains(driver)

    #Ticket description.
    ticket_body = str(ticket_data['body']).format(hostname = call_data['hostname'], contact = call_data['contato'])
    action.send_keys(Keys.TAB + ticket_body)
    action.perform()

    match ticket_data['type']:
        case 'ticket':
            #Fills "How is this affecting you?" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)

            #Fills "Degree of affectation" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)

            #Fills "Application" field.
            action.send_keys(Keys.TAB + ticket_data['application'])
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)

            #Fills "Phone contact" field.
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + call_data['contato'])
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)

            #opens ticket
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB) #ADD SPACE
            action.perform()
            time.sleep(1)

        case 'mfa':
            #Opens ticket.
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(Menu.ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.TICKET_LOAD_DELAY)

    return driver.current_url.removeprefix('https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/')


def __OpenTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass:
    """
    Private function: Opens a ticket and based on call data and ticket template.
    Returns LogClass object with the ticket detail.
    
    Dependencies:
    - :mod:`__MenuNavigator()`: To navigate the javascript menu (Selenium 
    API has a hard time locating elements there).

    Arguments:
    - driver: A loaded Chrome webdriver object.
    - call_data: Dict with call data.
    - ticket_data: Dict with ticket data.
    """

    driver.get(URL.SMART_RECORDER_URL)

    main_bar = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/smart-recorder-input/div/div[2]')
    main_bar.send_keys('@' + call_data['matricula'])
    time.sleep(Menu.USER_LOAD_DELAY)
    main_bar.send_keys(Keys.ENTER + ticket_data['type'])

    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div/div/div[2]/rs/div/div[2]/rs-dwp-catalog/div/div/div/div[1]/i[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[3]/button[1]').click()

    ticket_ID = __MenuNavigator(driver, call_data, ticket_data)
    return LogClass(Types.TICKET_CREATION, ticket_ID)


def __CloseTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass: #TODO
    """
    Private function: Opens a ticket and based on call data and ticket template.
    Returns LogClass object with the ticket detail.
    
    Dependencies:
    - :mod:`__OpenTicket()`: To open and generate ticket ID.

    Arguments:
    - driver: A loaded Chrome webdriver object.
    - call_data: Dict with call data, mainly to be passed to :mod:`__OpenTicket()`:.
    - ticket_data: Dict with ticket data, mainly to be passed to :mod:`__OpenTicket()`:.
    """

    #Open_Ticket_Log = __OpenTicket(driver, call_data, ticket_data)
    Open_Ticket_Log = LogClass(1, '107493')
    driver.get(URL.TICKED_ID_PREFIX + Open_Ticket_Log.GetID)

    #Opend ticket editor.
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[4]/div/div/div/fulfillment-map/div/div[2]/div[2]/div/div[2]').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div').click()

    #Edits ticket title.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(ticket_data['title'])

    #Changes status to "ongoing".
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div/div[1]/label/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div/div[1]/label/div/ul/li[2]/a').click()

    #Sets standard ticket definition.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/div/label/div/div/div/ul/li[4]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div/label/div/div/div/ul/li[1]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div/div/label/div/div/div/ul/li[2]/a').click()

    #Changes ticket disgnation.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div/a').click()



def __EscalateTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass: #TODO
    """"""

    TODO = True


def TicketProcessor(driver:webdriver.Chrome, *args) -> LogClass:
    """
    Processes call data into a ticket and returns a log object with it's details.

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
            log = __CloseTicket(driver, call_data, ticket_data)

        case 'escalate':
            log = __EscalateTicket(driver, call_data, ticket_data)

    return log


#Not a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')