"""Does most interactions with Selenium API."""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

#Files.
from FileHandler.Config import ConfigClass
from Constants import URL
from Constants import Paths


def __MicrosoftLogin(driver:webdriver.Chrome) -> None:
    """
    Private function: Tries to log into Microsoft account, will stop 
    for manual insertion of confirmation code if MFA is requested.

    Function :mod:`LoadDriver()` is dependant on this function.

    Arguments:
    - driver: A loaded Chrome webdriver object.
    """

    config = ConfigClass()

    #Does nothing if current URL is not microsoft login page.
    if driver.current_url.startswith('https://login.microsoftonline.com/') == True:
        driver.implicitly_wait(1)

        #Checks if microsoft is asking for profile selection.
        try:
            driver.find_element(By.XPATH, '//*[@id="tilesHolder"]/div[1]/div/div[1]/div/div[2]/div').click()

            if driver.current_url.endswith('/login') == False: #Confirm if this is always true.
                driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(config.GetPassword + Keys.ENTER)
        except NoSuchElementException:
            driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(config.GetEmail + Keys.ENTER)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(config.GetPassword + Keys.ENTER)

        time.sleep(1)

        #Checks if MFA is being requested.
        if driver.current_url.endswith('/login'):
            try:
                driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
                driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
                MFA_flag = False
            except NoSuchElementException:
                print('- MFA Confirmation Requested.')
                driver.find_element(By.XPATH, '//*[@id="idChkBx_SAOTCAS_TD"]').click()
                MFA_flag = True

            while MFA_flag:
                if driver.current_url == 'https://login.microsoftonline.com/common/SAS/ProcessAuth':
                    driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
                    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

                    MFA_flag = False

                time.sleep(1)

        driver.implicitly_wait(10)

    print('- Logged in.\n')


def LoadDriver() -> webdriver.Chrome:
    """
    Loads a chromedriver instace and sets it's configuration arguments\n
    Returns the Chrome webdriver object when Helix page is loaded.

    Depends on :mod:`MicrosoftLogin()` function to long into Microsoft account if needed.
    """

    #Loads browser profile and sets driver preferences.
    options = Options()
    options.add_argument('start-maximized')
    options.add_argument(f'user-data-dir={Paths.CHROME_PROFILE_PATH}')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    driver.implicitly_wait(10)

    #Opens new tab and closes default tabs.
    driver.switch_to.new_window()
    handle = driver.window_handles
    driver.switch_to.window(handle[0])
    driver.close()
    driver.switch_to.window(handle[1])
    driver.close()
    driver.switch_to.window(handle[2])

    driver.get(URL.PORTAL_URL)
    print('- Driver Loaded.')

    time.sleep(1)
    __MicrosoftLogin(driver)

    return driver


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')