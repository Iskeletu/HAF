"""Does most interactions with Selenium API."""

#Native Modules:
import time

#External Modules:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

#Internal Modules:
from HAF.FileHandler.Config import ConfigClass
from HAF.Constants import URL, MicrosoftLogin, Paths


def __MicrosoftLogin(driver:webdriver.Chrome) -> None:
    """
    Private function: Tries to log into Microsoft account, will stop 
    for manual insertion of confirmation code if MFA is requested.

    Arguments:
        - driver: A loaded Chrome webdriver object.
    """

    config = ConfigClass()
    time.sleep(MicrosoftLogin.ANIMATION_DELAY)

    #Checks if current URL is not Microsoft login page.
    if driver.current_url.startswith('https://login.microsoftonline.com/'):
        driver.implicitly_wait(MicrosoftLogin.ANIMATION_DELAY)

        #Checks if Microsoft is asking for profile selection.
        try:
            driver.find_element(By.XPATH, '//*[@id="tilesHolder"]/div[1]/div/div[1]/div/div[2]/div').click()

            if driver.current_url.endswith('/login') == False: #TODO: confirm if this is always true.
                driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(config.GetPassword + Keys.ENTER)
        except NoSuchElementException:
            driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(config.GetEmail + Keys.ENTER)
            time.sleep(MicrosoftLogin.ANIMATION_DELAY)
            driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(config.GetPassword + Keys.ENTER)
        time.sleep(MicrosoftLogin.ANIMATION_DELAY)

        #Checks if MFA is being requested.
        if driver.current_url.endswith('/login'):
            try:
                driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
                driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
                MFA_flag = False
            except NoSuchElementException:
                print('- MFA Confirmation Requested.')

                try: #Checks 14 day MFA timeout if available.
                    driver.find_element(By.XPATH, '//*[@id="idChkBx_SAOTCAS_TD"]').click()
                except NoSuchElementException:
                    pass

                MFA_flag = True

            while MFA_flag:
                if driver.current_url == 'https://login.microsoftonline.com/common/SAS/ProcessAuth':
                    driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
                    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

                    MFA_flag = False

                time.sleep(MicrosoftLogin.ANIMATION_DELAY)

        driver.implicitly_wait(10)

    print('- Logged in.\n')


def LoadDriver() -> webdriver.Chrome:
    """
    Configures and loads a Chrome webdriver instance.\n
    Returns the Chrome webdriver instace when the Fenix page is loaded.

    Dependencies:
        - :mod:`MicrosoftLogin()`: For microsoft log-in if needed.
    """

    #Loads browser profile and sets driver preferences.
    options = Options()
    options.add_argument('start-maximized')
    options.add_argument(f'user-data-dir={Paths.CHROME_PROFILE_PATH}')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    driver.implicitly_wait(10)

    #Closes default tabs and opens a blank one.
    driver.switch_to.new_window()
    handle = driver.window_handles
    driver.switch_to.window(handle[0]); driver.close()
    driver.switch_to.window(handle[1]); driver.close()
    driver.switch_to.window(handle[2])

    #Loads Fenix ISTM portal.
    driver.get(URL.PORTAL_URL)
    print('- Driver Loaded.')

    #Checks if Microsoft log-in is begin requested.
    __MicrosoftLogin(driver)

    print('- Use "help" for command information.')
    return driver


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')