"""Navigates Fenix ITSM portal and manages ticket creation, escalation and closing."""

#Native Modules:
import time

#External Modules:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

#Internal Modules:
from HAF.FileHandler.Logger import LogClass
from HAF.FileHandler.JsonHandler import LoadJson
from HAF.Constants import Menu, Paths, URL, LogConstants


def __TicketMenuNavigator(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> str: #TODO ATTACHMENTS
    """
    Navigates javascrpit menu during ticket creation and returns the ticket ID as a string.\n
    Returns the ticket ID as a string.

    Arguments:
        - driver: A loaded Chrome webdriver object.
        - call_data: Dictionary with call data.
        - ticket_data: Dictionary with ticket data.
    """

    #Changes focust to driver (menu navigation won't work minimized).
    try:
        driver.maximize_window()
    except WebDriverException:
        pass #Webdriver gives unknown exception if driver is minimezed for some reason...

    time.sleep(Menu.TICKETMENU_LOAD_DELAY)
    action = ActionChains(driver)

    #Ticket description.
    action.send_keys(Keys.TAB + str(ticket_data['Body']).format(
        Contact = call_data['Required']['Contact'],
        Hostname = call_data['Required']['Hostname']
    ))
    action.perform()

    match ticket_data['Type']:
        case 'ticket':
            #Fills "How is this affecting you?" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)

            #Fills "Degree of affectation" field.
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.SPACE)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)

            #Fills "Application" field.
            action.send_keys(Keys.TAB + ticket_data['Application'])
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)

            #Fills "Phone contact" field.
            action.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + call_data['Required']['Contact'])
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)

            #opens ticket
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()

        case 'mfa':
            #Opens ticket.
            action.send_keys(Keys.TAB + Keys.TAB)
            action.perform()
            time.sleep(Menu.GENERAL_ANIMATION_DELAY)
            action.send_keys(Keys.TAB + Keys.TAB + Keys.SPACE)
            action.perform()

    time.sleep(Menu.TICKETPAGE_LOAD_DELAY)
    return driver.current_url.removeprefix('https://prosegur-smartit.onbmc.com/smartit/app/#/sberequest/')


def __OpenTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass:
    """
    Private function: Opens a ticket and based on the call data and its ticket template.\n
    Returns a LogClass object with the ticket details.
    
    Dependencies:
        - :mod:`__MenuNavigator()`: To navigate the javascript menu (Selenium 
        API has a hard time locating elements there).

    Arguments:
        - driver: A loaded Chrome webdriver object.
        - call_data: Dictionary with call data.
        - ticket_data: Dictionary with ticket data.
    """

    driver.refresh()
    driver.get(URL.SMART_RECORDER_URL)

    main_bar = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/smart-recorder-input/div/div[2]')
    main_bar.send_keys('@' + call_data['Required']['User_ID'])
    time.sleep(Menu.USER_LOAD_DELAY)
    main_bar.send_keys(Keys.ENTER + ticket_data['Type'])

    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div/div/div[2]/rs/div/div[2]/rs-dwp-catalog/div/div/div/div[1]/i[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[3]/button[1]').click()

    ticket_ID = __TicketMenuNavigator(driver, call_data, ticket_data)
    return LogClass(LogConstants.TICKET_CREATED, ticket_ID)


def __CloseTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass:
    """
    Private function: Closes a ticket and based on the call data and its ticket template.\n
    Returns a LogClass object with the ticket details.
    
    Dependencies:
        - :mod:`__OpenTicket()`: To open and generate ticket ID.

    Arguments:
        - driver: A loaded Chrome webdriver object.
        - call_data: Dictionary with call data, mainly to be passed to :mod:`__OpenTicket()`:.
        - ticket_data: Dictionary with ticket data, mainly to be passed to :mod:`__OpenTicket()`:.
    """

    #Calls for ticket creation.
    Ticket_Log = __OpenTicket(driver, call_data, ticket_data)
    driver.get(URL.TICKED_ID_PREFIX + Ticket_Log.GetTicketID)

    #Opens ticket editor.
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[4]/div/div/div/fulfillment-map/div/div[2]/div[2]/div/div[2]').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div').click()
    time.sleep(Menu.TICKETEDITOR_LOAD_DELAY)

    #Edits ticket title.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(ticket_data['Title'])

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

    #Changes ticket disignation to self and reopens ticket editor.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div/a').click()
    time.sleep(Menu.DESIGNATION_LOAD_DELAY)
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[2]/div/button[1]').click()
    time.sleep(Menu.TICKETEDITOR_LOAD_DELAY)
    driver.refresh()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[2]/div').click()
    time.sleep(Menu.TICKETEDITOR_LOAD_DELAY)

    #Changes status to "concluded" and status reason to "solution informed".
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div/div[1]/label/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div/div[1]/label/div/ul/li[4]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div[1]/div[2]/div/label/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div[1]/div[2]/div/label/div/ul/li[1]/a').click()

    #Edits ticket solution and saves changes.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[1]/div/div[2]/div/label/textarea').send_keys(ticket_data['Answer'][int(call_data['Optional']['Solution'])])
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[2]/div/button[1]').click()

    Ticket_Log.UpdateType(LogConstants.TICKET_CLOSED) #Updates ticket status to closed.
    return Ticket_Log


def __EscalateTicket(driver:webdriver.Chrome, call_data:dict, ticket_data:dict) -> LogClass:
    """
    Private function: Escalates a ticket and based on the call data and its ticket template.\n
    Returns a LogClass object with the ticket details.
    
    Dependencies:
        - :mod:`__OpenTicket()`: To open and generate ticket ID.

    Arguments:
        - driver: A loaded Chrome webdriver object.
        - call_data: Dictionary with call data, mainly to be passed to :mod:`__OpenTicket()`:.
        - ticket_data: Dictionary with ticket data, mainly to be passed to :mod:`__OpenTicket()`:.
    """

    #Calls for ticket creation.
    Ticket_Log = __OpenTicket(driver, call_data, ticket_data)
    driver.get(URL.TICKED_ID_PREFIX + Ticket_Log.GetTicketID)

    #Opens ticket editor.
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[4]/div/div/div/fulfillment-map/div/div[2]/div[2]/div/div[2]').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div').click()
    time.sleep(Menu.TICKETEDITOR_LOAD_DELAY)

    #Edits ticket title.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/title-bar/div[2]/div/div[1]/label/input').send_keys(ticket_data['Title'])
    
    #Sets standard ticket definition.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/div/label/div/div/div/ul/li[4]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div/label/div/div/div/ul/li[1]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div/div/label/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[5]/div/div/label/div/div/div/ul/li[2]/a').click()

    ## The following block works inside the ticket designation menu.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[3]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/label/span').click() #Opens ticket designation menu.

    #Changes focust to driver (menu navigation won't work minimized).
    try:
        driver.maximize_window()
    except WebDriverException:
        pass #Webdriver gives unknown exception if driver is minimezed for some reason...

    time.sleep(Menu.DESIGNATIONMENU_LOAD_DELAY)

    #Changes search group to all.
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[2]/div[3]/label/div/button').click()
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[2]/div[3]/label/div/ul/li[3]/a').click()

    #Selects team from ticket template.
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[2]/div[4]/label/div/button').click()
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[2]/div[4]/label/div/ul/li[1]/input').send_keys(ticket_data['Team'])
    time.sleep(Menu.DESIGNATIONMENU_TEAMLOAD_DELAY)
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[2]/div[4]/label/div/ul/li[1]/input').send_keys(Keys.ENTER)
    time.sleep(Menu.GENERAL_ANIMATION_DELAY)

    #Designates to selected team.
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/div[2]/div/div/assignee-chooser/div[3]/div[1]').click()
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div/button[1]').click()

    #Saves Changes.
    driver.find_element(By.XPATH, '//*[@id="ticket-record-summary"]/div[2]/div/button[1]').click()

    Ticket_Log.UpdateType(LogConstants.TICKET_ESCALATED) #Updates ticket status to escalated.
    return Ticket_Log


def TicketProcessor(driver:webdriver.Chrome) -> None: #!INCONPLETE
    """
    Processes call data into a ticket and returns a log object with it's details.

    Dependencies:
        - :mod:`__OpenTicket()`: For ticket creation.
        - :mod:`__CloseTicket()`: For ticket closing.
        - :mod:`__EscalateTicket()`: For ticket escalation.

    Arguments:
        - driver: A loaded Chrome webdriver object.
    """

    call_data = LoadJson(Paths.CALL_JSON_PATH)
    
    try:
        ticket_data = LoadJson(Paths.DICTIONARY_JSON_PATH)[call_data['Required']['Call_Type']]
    except KeyError:
        print("- ERROR 01: 'Invalid Ticket Type', check your call information.\n")
        return

    if ticket_data['Process-Type'] == 'close':
        if call_data['Optional']['Solution'] + 1 > len(ticket_data['Answer']) or call_data['Optional']['Solution'] < 0:
            print("- ERROR 02: 'Invalid Solution ID', check your optinal call paramaters.\n")
            return

    #TODO catch if variable is 'none' and there is a {variable} block on the template

    match ticket_data['Process-Type']:
        case 'open':
            log = __OpenTicket(driver, call_data, ticket_data)

        case 'close':
            log = __CloseTicket(driver, call_data, ticket_data)

        case 'escalate':
            log = __EscalateTicket(driver, call_data, ticket_data)

    log.Register()
    print('Done. Use "details" for more details.\n')


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')